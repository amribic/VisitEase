<script lang="ts">
  import Login from './components/Login.svelte';
  import Signup from './components/Signup.svelte';
  import Success from './components/Success.svelte';
  
  let currentPage = 'login';

  function goToSignup() {
    currentPage = 'signup';
  }

  function goToLogin() {
    currentPage = 'login';
  }

  function goToSuccess() {
    currentPage = 'success';
  }
</script>

<main>
  <div class="container">
    {#if currentPage === 'signup'}
      <Signup on:back={goToLogin} />
    {:else if currentPage === 'success'}
      <Success />
    {:else}
      <Login on:signup={goToSignup} on:success={goToSuccess} />
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