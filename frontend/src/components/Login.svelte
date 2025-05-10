<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  let email = '';
  let password = '';
  let error = '';
  let loading = false;

  async function handleSubmit() {
    loading = true;
    error = '';
    
    try {
      const response = await fetch('http://localhost:8080/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          email,
          password
        }),
        credentials: 'include'
      });

      const data = await response.json();
      
      if (response.ok) {
        dispatch('success');
      } else {
        error = data.message || 'Login failed. Please try again.';
      }
    } catch (e) {
      error = 'An error occurred. Please try again.';
    } finally {
      loading = false;
    }
  }

  function handleSignupClick() {
    dispatch('signup');
  }
</script>

<div class="login-container">
  <h1>Login</h1>
  
  {#if error}
    <div class="error-message">
      {error}
    </div>
  {/if}

  <form on:submit|preventDefault={handleSubmit}>
    <div class="form-group">
      <label for="email">Email</label>
      <input
        type="email"
        id="email"
        bind:value={email}
        required
        placeholder="Enter your email"
      />
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <input
        type="password"
        id="password"
        bind:value={password}
        required
        placeholder="Enter your password"
      />
    </div>

    <button type="submit" disabled={loading}>
      {loading ? 'Logging in...' : 'Login'}
    </button>
  </form>

  <p class="signup-link">
    Don't have an account? <button class="link-button" on:click={handleSignupClick}>Sign up</button>
  </p>
</div>

<style>
  .login-container {
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

  .form-group {
    margin-bottom: 1.5rem;
    text-align: left;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #333;
    font-weight: 500;
  }

  input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    box-sizing: border-box;
  }

  input:focus {
    outline: none;
    border-color: #ff3e00;
    box-shadow: 0 0 0 2px rgba(255, 62, 0, 0.1);
  }

  button {
    width: 100%;
    padding: 0.75rem;
    background-color: #ff3e00;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  button:hover {
    background-color: #ff5722;
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

  .signup-link {
    margin-top: 1.5rem;
    color: #666;
  }

  .link-button {
    background: none;
    border: none;
    color: #ff3e00;
    padding: 0;
    font: inherit;
    cursor: pointer;
    text-decoration: none;
    display: inline;
  }

  .link-button:hover {
    text-decoration: underline;
  }

  @media (max-width: 480px) {
    .login-container {
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
    .login-container {
      width: 100vw;
      max-width: 100vw;
      border-radius: 0;
      box-shadow: none;
      padding: 0.5rem;
    }
  }
</style> 