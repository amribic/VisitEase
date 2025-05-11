<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { API_URL } from '../config';
  const dispatch = createEventDispatcher();

  let email = '';
  let password = '';
  let error = '';
  let loading = false;

  async function handleSubmit() {
    loading = true;
    error = '';
    
    try {
      const response = await fetch(`${API_URL}/login`, {
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
  <div class="logo-container">
    <div class="logo">
      <span class="logo-text">Visit</span>
      <span class="logo-text-accent">Ease</span>
    </div>
    <div class="tagline">Your Healthcare Journey, Simplified</div>
  </div>
  
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
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

  .login-container {
    background: white;
    padding: 2.5rem;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    max-width: 420px;
    width: 100%;
    margin: 2rem auto;
    position: relative;
    font-family: 'Poppins', sans-serif;
  }

  .logo-container {
    text-align: center;
    margin-bottom: 2.5rem;
  }

  .logo {
    margin-bottom: 0.5rem;
  }

  .logo-text {
    font-size: 2.5rem;
    font-weight: 700;
    color: #333;
    letter-spacing: -0.5px;
  }

  .logo-text-accent {
    font-size: 2.5rem;
    font-weight: 700;
    color: #6a00ff;
    letter-spacing: -0.5px;
  }

  .tagline {
    color: #666;
    font-size: 1rem;
    font-weight: 400;
    margin-top: 0.5rem;
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
    font-size: 0.95rem;
  }

  input {
    width: 100%;
    padding: 0.875rem;
    border: 2px solid #eee;
    border-radius: 8px;
    font-size: 1rem;
    box-sizing: border-box;
    -webkit-appearance: none;
    appearance: none;
    transition: all 0.2s ease;
    font-family: 'Poppins', sans-serif;
  }

  input:focus {
    outline: none;
    border-color: #6a00ff;
    box-shadow: 0 0 0 4px rgba(106, 0, 255, 0.1);
  }

  button {
    width: 100%;
    padding: 0.875rem;
    background-color: #6a00ff;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
    font-family: 'Poppins', sans-serif;
  }

  button:hover, button:active {
    background-color: #7c1fff;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(106, 0, 255, 0.2);
  }

  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }

  .error-message {
    background-color: #ffebee;
    color: #c62828;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    font-size: 0.9rem;
    border: 1px solid #ffcdd2;
  }

  .signup-link {
    margin-top: 1.5rem;
    color: #666;
    font-size: 0.95rem;
  }

  .link-button {
    background: none;
    border: none;
    color: #6a00ff;
    padding: 0;
    font: inherit;
    cursor: pointer;
    text-decoration: none;
    display: inline;
    -webkit-tap-highlight-color: transparent;
    width: auto;
    font-weight: 500;
  }

  .link-button:hover, .link-button:active {
    text-decoration: underline;
    background: none;
  }

  @media (max-width: 480px) {
    .login-container {
      padding: 2rem 1.5rem;
      margin: 1rem;
      border-radius: 12px;
    }

    .logo-text, .logo-text-accent {
      font-size: 2rem;
    }

    .tagline {
      font-size: 0.9rem;
    }

    .form-group {
      margin-bottom: 1.25rem;
    }

    input {
      padding: 0.875rem;
      font-size: 16px;
    }

    button {
      padding: 0.875rem;
    }
  }

  @media (max-height: 600px) {
    .login-container {
      padding: 1.5rem;
      margin: 0.5rem auto;
    }

    .logo-container {
      margin-bottom: 1.5rem;
    }

    .form-group {
      margin-bottom: 1rem;
    }
  }
</style> 