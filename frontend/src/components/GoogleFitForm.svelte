<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';
  const dispatch = createEventDispatcher();

  let isConnected = false;
  let isLoading = false;
  let error = '';

  onMount(async () => {
    // Check if we're coming back from Google Fit auth
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('success') === 'true') {
      isConnected = true;
    } else {
      // Check if already connected
      try {
        const response = await fetch('http://localhost:8080/fitness', {
          credentials: 'include'
        });
        isConnected = response.ok;
      } catch (e) {
        console.error('Error checking Google Fit connection:', e);
      }
    }
  });

  async function connectGoogleFit() {
    isLoading = true;
    error = '';
    
    try {
      const response = await fetch('http://localhost:8080/authorize', {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.url) {
          window.location.href = data.url;
        }
      } else {
        error = 'Failed to connect to Google Fit. Please try again.';
      }
    } catch (e) {
      error = 'An error occurred. Please try again.';
    } finally {
      isLoading = false;
    }
  }

  function handleSkip() {
    dispatch('skip');
  }

  function handleContinue() {
    dispatch('continue');
  }
</script>

<div class="form-container">
  <h1>Connect Your Fitness Data</h1>
  
  {#if error}
    <div class="error-message">
      {error}
    </div>
  {/if}

  <div class="content">
    <p>Would you like to connect your Google Fit data to enhance your experience?</p>
    
    <div class="buttons">
      <button 
        class="connect-button" 
        on:click={connectGoogleFit} 
        disabled={isLoading || isConnected}
      >
        {#if isLoading}
          Connecting...
        {:else if isConnected}
          Connected to Google Fit
        {:else}
          Connect Google Fit
        {/if}
      </button>

      <button 
        class="skip-button" 
        on:click={handleSkip}
        disabled={isLoading}
      >
        Skip for Now
      </button>

      <button 
        class="continue-button" 
        on:click={handleContinue}
        disabled={!isConnected}
      >
        Continue
      </button>
    </div>
  </div>
</div>

<style>
  .form-container {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 500px;
    width: 100%;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 2rem;
    font-weight: 100;
    margin: 0 0 2rem 0;
    padding: 0;
    line-height: 1.2;
  }

  .content {
    text-align: center;
  }

  p {
    color: #666;
    margin-bottom: 2rem;
    font-size: 1.1rem;
  }

  .buttons {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  button {
    width: 100%;
    padding: 0.75rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .connect-button {
    background-color: #4285f4;
    color: white;
  }

  .connect-button:hover:not(:disabled) {
    background-color: #357abd;
  }

  .skip-button {
    background-color: #f5f5f5;
    color: #666;
  }

  .skip-button:hover:not(:disabled) {
    background-color: #e0e0e0;
  }

  .continue-button {
    background-color: #4CAF50;
    color: white;
  }

  .continue-button:hover:not(:disabled) {
    background-color: #45a049;
  }

  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }

  .error-message {
    background-color: #ffebee;
    color: #c62828;
    padding: 0.75rem;
    border-radius: 4px;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
  }

  @media (max-width: 480px) {
    .form-container {
      padding: 1.5rem;
    }

    h1 {
      font-size: 1.75rem;
    }
  }
</style> 