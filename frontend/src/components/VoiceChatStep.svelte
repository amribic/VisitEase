<script lang="ts">
    import VoiceChat from './VoiceChat.svelte';
</script>

<div class="voice-chat-step">
    <h2>Voice Chat with AI Assistant</h2>
    <p>Have a conversation with our AI assistant to discuss your health concerns and get personalized advice.</p>
    
    <div class="chat-container">
        <div class="chat-wrapper">
            <VoiceChat />
        </div>
    </div>
</div>

<style>
    .voice-chat-step {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        padding: 2rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        min-height: 600px;
    }

    h2 {
        color: #333;
        margin: 0;
        font-size: 1.5rem;
    }

    p {
        color: #666;
        margin: 0;
        line-height: 1.5;
    }

    .chat-container {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
    }

    .chat-wrapper {
        width: 100%;
        max-width: 800px;
        height: 100%;
    }
</style> 