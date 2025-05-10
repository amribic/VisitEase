<script>
  import { onMount } from 'svelte';

  let message = 'Setup Complete!';

  onMount(() => {
    setTimeout(() => {
      window.location.href = '/';
    }, 3000);
  });

  function handleContinue() {
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
  }

  h1 {
    color: #4CAF50;
    font-size: 2rem;
    margin: 0 0 1rem 0;
  }

  p {
    color: #666;
    margin-bottom: 1.5rem;
  }

  button {
    padding: 0.875rem 1.5rem;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
  }

  button:hover {
    background-color: #45a049;
  }
</style> 