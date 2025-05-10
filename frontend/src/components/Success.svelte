<script lang="ts">
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  let message = 'Setup Complete!';
  let redirectTimer: number;

  onMount(() => {
    redirectTimer = window.setTimeout(() => {
      window.location.href = '/';
    }, 3000);
  });

  function handleContinue() {
    clearTimeout(redirectTimer);
    window.location.href = '/';
  }
</script>

<div class="success-container">
  <h1>{message}</h1>
  <p>You're all set! Redirecting to home page...</p>
  <button on:click={handleContinue}>Continue Now</button>
</div>

<style>
  .success-container {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    width: 100%;
    margin: 0 auto;
    text-align: center;
    position: relative;
  }

  h1 {
    color: #4CAF50;
    font-size: 2rem;
    font-weight: 100;
    margin: 0 0 1rem 0;
    line-height: 1.2;
  }

  p {
    color: #666;
    margin-bottom: 1.5rem;
    line-height: 1.5;
  }

  button {
    padding: 0.875rem 1.5rem;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
  }

  button:hover, button:active {
    background-color: #45a049;
  }

  @media (max-width: 480px) {
    .success-container {
      padding: 1.5rem;
      margin: 0.5rem;
      border-radius: 0;
      box-shadow: none;
      background: transparent;
    }

    h1 {
      font-size: 1.75rem;
      margin-bottom: 0.875rem;
    }

    p {
      margin-bottom: 1.25rem;
      font-size: 0.95rem;
    }

    button {
      padding: 1rem 1.5rem;
      width: 100%;
      font-size: 1rem;
    }
  }

  @media (max-height: 600px) {
    .success-container {
      padding: 1rem;
    }

    h1 {
      margin-bottom: 0.75rem;
    }

    p {
      margin-bottom: 1rem;
    }
  }
</style> 