<script lang="ts">
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';
    import { API_URL } from '../config';

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
    let isSpeaking = false;
    let speechSynthesis = window.speechSynthesis;
    let showUserBubble = false;
    let showAssistantBubble = false;
    let isIOS = false;

    onMount(() => {
        // Check browser compatibility
        const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
        const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
        isIOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);
        const hasSpeechRecognition = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
        const hasMediaRecorder = 'MediaRecorder' in window;
        
        // Special handling for Safari on iOS
        if (isIOS && isSafari) {
            console.log('Detected Safari on iOS');
            // Use MediaRecorder as fallback for iOS Safari
            if (!hasMediaRecorder) {
                console.error('MediaRecorder not supported on this device');
                messages = [{
                    role: 'assistant',
                    content: 'Voice input is not supported in Safari on iOS. Please try using Chrome on Android or a desktop browser.',
                    id: messageId++
                }];
                return;
            }
        } else if (!hasSpeechRecognition && !hasMediaRecorder) {
            console.error('Speech recognition not supported in this browser');
            messages = [{
                role: 'assistant',
                content: 'Speech recognition is not supported in your browser. Please try using Chrome or Safari on desktop.',
                id: messageId++
            }];
            return;
        }

        // Check if browser is Firefox
        isFirefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;

        // Initialize messages with an empty array - the first message will come from the backend
        messages = [];

        // Initialize speech synthesis voices
        if (speechSynthesis) {
            // Wait for voices to be loaded
            if (speechSynthesis.getVoices().length === 0) {
                speechSynthesis.onvoiceschanged = () => {
                    initializeChat();
                };
            } else {
                initializeChat();
            }
        }

        // Initialize speech recognition for non-Firefox and non-iOS browsers
        if (!isFirefox && !isIOS && hasSpeechRecognition) {
            recognition = new (window as any).webkitSpeechRecognition() || new (window as any).SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                console.log('Recognition started');
                finalTranscript = '';
                userInput = '';
                showUserBubble = true;
                isProcessing = false;
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
                console.log('Current transcript:', userInput);
            };

            recognition.onerror = (event: any) => {
                console.error('Speech recognition error:', event.error);
                isRecording = false;
                isProcessing = false;
                showUserBubble = false;
            };

            recognition.onend = () => {
                console.log('Recognition ended');
                isRecording = false;
                showUserBubble = false;
                if (finalTranscript.trim()) {
                    console.log('Final transcript:', finalTranscript);
                    userInput = finalTranscript;
                    handleSubmit().catch(error => {
                        console.error('Error in onend handler:', error);
                        isProcessing = false;
                    });
                } else {
                    console.log('No final transcript to send');
                    isProcessing = false;
                }
            };
        }
    });

    async function initializeChat() {
        try {
            const response = await fetch(`${API_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: 'start' }),
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            if (data.response) {
                messages = [{
                    role: 'assistant',
                    content: data.response,
                    id: messageId++
                }];
                speakMessage(data.response);
            }
        } catch (error) {
            console.error('Error getting initial message:', error);
            messages = [{
                role: 'assistant',
                content: 'I apologize, but I encountered an error. Please try refreshing the page.',
                id: messageId++
            }];
        }
    }

    async function speakMessage(text: string) {
        try {
            console.log('Starting speech synthesis for:', text);
            showAssistantBubble = true;
            isSpeaking = true;

            // Call our backend endpoint for text-to-speech
            const response = await fetch(`${API_URL}/api/text-to-speech`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Failed to generate speech');
            }

            // Get the audio blob
            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            
            // Create and play audio
            const audio = new Audio(audioUrl);
            
            audio.onended = () => {
                console.log('Speech ended');
                isSpeaking = false;
                showAssistantBubble = false;
                URL.revokeObjectURL(audioUrl);
            };

            audio.onerror = (error) => {
                console.error('Speech synthesis error:', error);
                isSpeaking = false;
                showAssistantBubble = false;
                URL.revokeObjectURL(audioUrl);
            };

            console.log('Playing audio...');
            await audio.play();
        } catch (error) {
            console.error('Error in speech synthesis:', error);
            isSpeaking = false;
            showAssistantBubble = false;
        }
    }

    async function startRecording() {
        if (isProcessing || isSpeaking) return;
        
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // Use MediaRecorder for Firefox, iOS Safari, or when SpeechRecognition is not available
            if (isFirefox || isIOS || !('webkitSpeechRecognition' in window)) {
                if (!('MediaRecorder' in window)) {
                    throw new Error('MediaRecorder not supported');
                }
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                showUserBubble = true;

                mediaRecorder.ondataavailable = (event) => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    showUserBubble = false;
                    await processAudio(audioBlob);
                };

                // For iOS Safari, we need to request data more frequently
                if (isIOS) {
                    mediaRecorder.start(1000); // Request data every second
                } else {
                    mediaRecorder.start();
                }
                isRecording = true;
            } else if (recognition) {
                userInput = '';
                finalTranscript = '';
                recognition.start();
                isRecording = true;
            }
        } catch (error) {
            console.error('Error accessing microphone:', error);
            messages = [...messages, {
                role: 'assistant',
                content: 'Could not access microphone. Please make sure you have granted microphone permissions.',
                id: messageId++
            }];
        }
    }

    function stopRecording() {
        console.log('Stopping recording...');
        if (isFirefox && mediaRecorder && isRecording) {
            mediaRecorder.stop();
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
            isRecording = false;
        } else if (recognition && isRecording) {
            recognition.stop();
        }
    }

    async function processAudio(audioBlob: Blob) {
        try {
            console.log('Processing audio...');
            // Convert audio to text using OpenAI's Whisper API
            const formData = new FormData();
            formData.append('file', audioBlob, 'audio.wav');
            formData.append('model', 'whisper-1');

            const response = await fetch(`${API_URL}/api/transcribe`, {
                method: 'POST',
                body: formData,
                credentials: 'include'
            });

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            console.log('Transcribed text:', data.text);
            userInput = data.text;
            
            if (userInput.trim()) {
                console.log('Sending transcribed message...');
                await handleSubmit();
            } else {
                console.log('No text to send after transcription');
            }
        } catch (error) {
            console.error('Error processing audio:', error);
            messages = [...messages, 
                { role: 'assistant', content: 'I apologize, but I encountered an error processing your voice. Please try again.', id: messageId++ }
            ];
            speakMessage('I apologize, but I encountered an error processing your voice. Please try again.');
        } finally {
            isProcessing = false;
        }
    }

    async function handleSubmit() {
        if (!userInput.trim()) {
            console.log('No input to process');
            return;
        }

        console.log('Starting to process message:', userInput);
        
        try {
            console.log('Sending message:', userInput);
            const response = await fetch(`${API_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userInput
                }),
                credentials: 'include'
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Received response data:', data);
            
            if (!data.response) {
                throw new Error('No response from assistant');
            }
            
            const assistantMessage = data.response;
            console.log('Assistant message:', assistantMessage);
            
            // Add user message first
            messages = [...messages, 
                { role: 'user', content: userInput, id: messageId++ }
            ];
            
            // Then add and speak assistant's response
            messages = [...messages, 
                { role: 'assistant', content: assistantMessage, id: messageId++ }
            ];
            
            // Clear input before speaking
            userInput = '';
            finalTranscript = '';
            
            // Speak the assistant's response
            console.log('Speaking assistant response...');
            speakMessage(assistantMessage);
            
        } catch (error) {
            console.error('Error in handleSubmit:', error);
            const errorMessage = 'I apologize, but I encountered an error. Please try again.';
            messages = [...messages, 
                { role: 'assistant', content: errorMessage, id: messageId++ }
            ];
            speakMessage(errorMessage);
        }
    }
</script>

<div class="voice-chat-container">
    <div class="bubbles-container">
        {#if showUserBubble}
            <div class="voice-bubble user" in:fade={{ duration: 200 }}>
                <div class="bubble-dots">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>
        {/if}
        {#if showAssistantBubble}
            <div class="voice-bubble assistant" in:fade={{ duration: 200 }}>
                <div class="bubble-dots">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>
        {/if}
    </div>

    <div class="input-container">
        <button 
            class="record-button {isRecording ? 'recording' : ''}"
            on:click={isRecording ? stopRecording : startRecording}
            disabled={isProcessing || isSpeaking}
            title={isRecording ? 'Stop recording' : 'Start recording'}
        >
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                <line x1="12" y1="19" x2="12" y2="23"></line>
                <line x1="8" y1="23" x2="16" y2="23"></line>
            </svg>
        </button>
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

    .bubbles-container {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        padding: 2rem;
    }

    .voice-bubble {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: pulse 2s infinite;
    }

    .voice-bubble.user {
        background: #6a00ff;
    }

    .voice-bubble.assistant {
        background: #dc3545;
    }

    .bubble-dots {
        display: flex;
        gap: 4px;
    }

    .dot {
        width: 8px;
        height: 8px;
        background: white;
        border-radius: 50%;
        animation: dotPulse 1.4s infinite;
    }

    .dot:nth-child(2) {
        animation-delay: 0.2s;
    }

    .dot:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes pulse {
        0% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(106, 0, 255, 0.4);
        }
        70% {
            transform: scale(1.05);
            box-shadow: 0 0 0 20px rgba(106, 0, 255, 0);
        }
        100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(106, 0, 255, 0);
        }
    }

    @keyframes dotPulse {
        0%, 100% {
            transform: scale(1);
            opacity: 0.5;
        }
        50% {
            transform: scale(1.2);
            opacity: 1;
        }
    }

    .input-container {
        display: flex;
        width: 100%;
        justify-content: center;
        padding: 1rem;
    }

    .record-button {
        background: #f8f9fa;
        color: #dc3545;
        cursor: pointer;
        opacity: 1;
        width: 64px;
        height: 64px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .record-button:hover:not(:disabled) {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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

    .icon {
        width: 32px;
        height: 32px;
    }
</style> 