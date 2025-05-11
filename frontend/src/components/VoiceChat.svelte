<script lang="ts">
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';

    let messages: { role: 'user' | 'assistant', content: string, id: number }[] = [];
    let userInput = '';
    let isRecording = false;
    let isProcessing = false;
    let recognition: any = null;
    let messageId = 0;
    let finalTranscript = '';
    let mediaRecorder: MediaRecorder | null = null;
    let audioChunks: Blob[] = [];
    let isFirefox = false;

    onMount(() => {
        // Check if browser is Firefox
        isFirefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;

        // Initialize messages with a welcome message
        messages = [
            {
                role: 'assistant',
                content: 'Hello! I\'m your medical assistant. How can I help you today?',
                id: messageId++
            }
        ];

        // Initialize speech recognition for non-Firefox browsers
        if (!isFirefox && 'webkitSpeechRecognition' in window) {
            recognition = new (window as any).webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                console.log('Recognition started');
                finalTranscript = '';
                userInput = '';
            };

            recognition.onresult = (event: any) => {
                let interimTranscript = '';
                
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript;
                    } else {
                        interimTranscript += transcript;
                    }
                }

                userInput = finalTranscript || interimTranscript;
                console.log('Final transcript:', finalTranscript);
                console.log('Interim transcript:', interimTranscript);
            };

            recognition.onerror = (event: any) => {
                console.error('Speech recognition error:', event.error);
                isRecording = false;
                isProcessing = false;
            };

            recognition.onend = () => {
                console.log('Recognition ended');
                isRecording = false;
                if (finalTranscript.trim()) {
                    userInput = finalTranscript;
                    handleSubmit();
                }
            };
        }
    });

    async function startRecording() {
        if (isProcessing) return;
        
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            if (isFirefox) {
                // Firefox: Use MediaRecorder
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    await processAudio(audioBlob);
                };

                mediaRecorder.start();
                isRecording = true;
                console.log('Started recording in Firefox');
            } else if (recognition) {
                // Chrome/Edge: Use Web Speech API
                userInput = '';
                finalTranscript = '';
                recognition.start();
                isRecording = true;
                console.log('Started recording with Web Speech API');
            }
        } catch (error) {
            console.error('Error accessing microphone:', error);
            alert('Could not access microphone. Please make sure you have granted microphone permissions.');
        }
    }

    function stopRecording() {
        console.log('Stopping recording');
        if (isFirefox && mediaRecorder && isRecording) {
            mediaRecorder.stop();
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
            isRecording = false;
        } else if (recognition && isRecording) {
            recognition.stop();
        }
    }

    async function processAudio(audioBlob: Blob) {
        isProcessing = true;
        try {
            // Convert audio to text using OpenAI's Whisper API
            const formData = new FormData();
            formData.append('file', audioBlob, 'audio.wav');
            formData.append('model', 'whisper-1');

            const response = await fetch('/api/transcribe', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            userInput = data.text;
            await handleSubmit();
        } catch (error) {
            console.error('Error processing audio:', error);
            messages = [...messages, 
                { role: 'assistant', content: 'I apologize, but I encountered an error processing your voice. Please try typing your message instead.', id: messageId++ }
            ];
        } finally {
            isProcessing = false;
        }
    }

    async function handleSubmit() {
        if (!userInput.trim() || isProcessing) {
            console.log('No input to process or already processing');
            return;
        }
        
        isProcessing = true;
        try {
            console.log('Sending message:', userInput);
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userInput
                })
            });

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            messages = [...messages, 
                { role: 'user', content: userInput, id: messageId++ },
                { role: 'assistant', content: data.response, id: messageId++ }
            ];
            
            userInput = '';
            finalTranscript = '';
        } catch (error) {
            console.error('Error sending message:', error);
            messages = [...messages, 
                { role: 'assistant', content: 'I apologize, but I encountered an error. Please try again.', id: messageId++ }
            ];
        } finally {
            isProcessing = false;
        }
    }
</script>

<div class="voice-chat-container">
    <div class="messages-container">
        {#each messages as message (message.id)}
            <div 
                class="message {message.role}" 
                in:fade={{ duration: 200 }}
            >
                {message.content}
            </div>
        {/each}
    </div>

    <div class="input-container">
        <div class="input-wrapper">
            <button 
                class="record-button {isRecording ? 'recording' : ''}"
                on:click={isRecording ? stopRecording : startRecording}
                disabled={isProcessing}
                title={isRecording ? 'Stop recording' : 'Start recording'}
            >
                {#if isRecording}
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <rect x="9" y="9" width="6" height="6"></rect>
                    </svg>
                {:else}
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                        <line x1="12" y1="19" x2="12" y2="23"></line>
                        <line x1="8" y1="23" x2="16" y2="23"></line>
                    </svg>
                {/if}
            </button>

            <button 
                class="send-button"
                on:click={handleSubmit}
                disabled={isProcessing || !userInput.trim()}
                title="Send message"
            >
                <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="22" y1="2" x2="11" y2="13"></line>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
            </button>

            <input
                type="text"
                bind:value={userInput}
                placeholder="Type your message..."
                on:keydown={(e) => e.key === 'Enter' && handleSubmit()}
                disabled={isProcessing}
            />
        </div>
    </div>
</div>

<style>
    .voice-chat-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        width: 100%;
        max-width: 100%;
        margin: 0 auto;
        padding: 1rem;
        box-sizing: border-box;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .messages-container {
        flex-grow: 1;
        overflow-y: auto;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 1rem;
        max-height: 400px;
        scroll-behavior: smooth;
    }

    .message {
        margin: 0.5rem 0;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        animation: messageAppear 0.3s ease-out;
    }

    @keyframes messageAppear {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .user {
        background: #6a00ff;
        color: white;
        margin-left: auto;
    }

    .assistant {
        background: white;
        color: #333;
        margin-right: auto;
        border: 1px solid #e9ecef;
    }

    .input-container {
        display: flex;
        width: 100%;
        padding: 0;
        margin: 0;
    }

    .input-wrapper {
        display: flex;
        flex: 1;
        gap: 0.5rem;
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        align-items: center;
        width: 100%;
        box-sizing: border-box;
    }

    input {
        flex: 1;
        min-width: 0;
        padding: 0.75rem;
        border: none;
        border-radius: 4px;
        font-size: 1rem;
        background: transparent;
        outline: none;
        width: 100%;
        box-sizing: border-box;
    }

    input:focus {
        outline: none;
    }

    button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.5rem;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
        background: #f8f9fa;
        color: #6a00ff;
        width: 36px;
        height: 36px;
        flex-shrink: 0;
    }

    button:hover:not(:disabled) {
        background: #e9ecef;
        transform: translateY(-1px);
    }

    button:active:not(:disabled) {
        transform: translateY(0);
    }

    button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .record-button {
        background: #f8f9fa;
        color: #dc3545;
        cursor: pointer;
        opacity: 1;
    }

    .record-button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .record-button.recording {
        background: #dc3545;
        color: white;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.4);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(220, 53, 69, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(220, 53, 69, 0);
        }
    }

    .send-button {
        background: #6a00ff;
        color: white;
    }

    .send-button:hover:not(:disabled) {
        background: #7c1fff;
    }

    .icon {
        width: 16px;
        height: 16px;
        display: block;
        flex-shrink: 0;
    }

    @media (max-width: 480px) {
        .input-container {
            flex-direction: column;
        }

        .input-wrapper {
            width: 100%;
        }

        input {
            width: 100%;
        }

        button {
            width: 36px;
            height: 36px;
        }
    }
</style> 