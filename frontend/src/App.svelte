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
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

  :global(html), :global(body) {
    width: 100vw;
    min-height: 100vh;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    background-color: #f8fff9;
    overflow-x: hidden;
    min-height: 100vh;
    width: 100%;
    font-family: 'DM Sans', sans-serif;
    color: #222;
  }

  :global(html) {
    font-size: 16px;
  }

  :global(*) {
    box-sizing: border-box;
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
    position: relative;
  }

  .container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  @media (max-width: 480px) {
    :global(html) {
      font-size: 14px;
    }

    main {
      padding: 0.5rem;
    }

    .container {
      padding: 0 0.5rem;
    }
  }
</style> 