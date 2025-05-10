<script lang="ts">
  import Login from './components/Login.svelte';
  import Signup from './components/Signup.svelte';
  import Success from './components/Success.svelte';
  import GoogleFitForm from './components/GoogleFitForm.svelte';
  import { onMount } from 'svelte';
  
  let currentPage = 'login';

  onMount(() => {
    // Check if we're coming back from Google Fit auth
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('success') === 'true') {
      currentPage = 'google-fit';
    }
  });

  function goToSignup() {
    currentPage = 'signup';
  }

  function goToLogin() {
    currentPage = 'login';
  }

  function goToSuccess() {
    currentPage = 'success';
  }

  function goToGoogleFit() {
    currentPage = 'google-fit';
  }

  function handleGoogleFitSkip() {
    goToSuccess();
  }

  function handleGoogleFitContinue() {
    goToSuccess();
  }
</script>

<main>
  <div class="container">
    {#if currentPage === 'signup'}
      <Signup on:back={goToLogin} />
    {:else if currentPage === 'success'}
      <Success />
    {:else if currentPage === 'google-fit'}
      <GoogleFitForm 
        on:skip={handleGoogleFitSkip} 
        on:continue={handleGoogleFitContinue} 
      />
    {:else}
      <Login on:signup={goToSignup} on:success={goToGoogleFit} />
    {/if}
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: #f5f5f5;
    overflow-x: hidden;
  }

  main {
    text-align: center;
    padding: 1rem;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-sizing: border-box;
    width: 100%;
  }

  .container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }
</style> 