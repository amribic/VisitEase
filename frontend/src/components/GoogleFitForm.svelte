<script lang="ts">
  import { createEventDispatcher, onMount } from 'svelte';
  import googleFitLogo from '../assets/google-fit-logo.png';
  const dispatch = createEventDispatcher();

  let isConnected = false;
  let isLoading = false;
  let error = '';
  let successMessage = '';

  onMount(async () => {
    // Check if we're coming back from Google Fit auth
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('success') === 'true') {
      isConnected = true;
      successMessage = 'Successfully connected to Google Fit! Your data has been imported.';
      // Remove the success parameter from the URL
      window.history.replaceState({}, '', '/google-fit');
    } else {
      // Check if already connected
      try {
        const response = await fetch('http://localhost:8080/fitness', {
          credentials: 'include',
          method: 'HEAD'
        });
        isConnected = response.ok;
        console.log('Google Fit connection status:', isConnected);
      } catch (e) {
        console.error('Error checking Google Fit connection:', e);
        isConnected = false;
      }
    }
  });

  async function connectGoogleFit() {
    isLoading = true;
    error = '';
    successMessage = '';
    
    try {
      const response = await fetch('http://localhost:8080/authorize', {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Authorization response:', data);
        if (data.url) {
          window.location.href = data.url;
        } else {
          error = 'No authorization URL received';
        }
      } else {
        const errorData = await response.json();
        error = errorData.error || 'Failed to connect to Google Fit. Please try again.';
        console.error('Authorization error:', error);
      }
    } catch (e) {
      error = 'An error occurred. Please try again.';
      console.error('Connection error:', e);
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

  {#if successMessage}
    <div class="success-message">
      {successMessage}
    </div>
  {/if}

  <div class="content">
    <div class="google-fit-icon">
      <img src={googleFitLogo} alt="Google Fit logo" width="48" height="48" style="filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));" />
    </div>
    
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
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 100%;
    width: 100%;
    margin: 0 auto;
    max-height: 100vh;
    overflow-y: auto;
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

  .google-fit-icon {
    margin-bottom: 1.5rem;
  }

  .google-fit-icon img {
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
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

  .success-message {
    background-color: #e8f5e9;
    color: #2e7d32;
    padding: 0.75rem;
    border-radius: 4px;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
  }

  @media (max-width: 480px) {
    .form-container {
      padding: 1rem;
    }

    h1 {
      font-size: 1.5rem;
    }

    button {
      padding: 0.5rem;
    }
  }

  @media (max-width: 600px) {
    .form-container {
      width: 100vw;
      max-width: 100vw;
      border-radius: 0;
      box-shadow: none;
      padding: 0.5rem;
    }
  }
</style> 