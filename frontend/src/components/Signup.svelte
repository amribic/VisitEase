<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  let email = '';
  let password = '';
  let confirmPassword = '';
  let error = '';
  let loading = false;

  async function handleSubmit() {
    loading = true;
    error = '';
    
    // Validate passwords match
    if (password !== confirmPassword) {
      error = 'Passwords do not match';
      loading = false;
      return;
    }

    try {
      const response = await fetch('http://localhost:8080/signup', {
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
        window.location.href = '/';
      } else {
        error = data.message || 'Signup failed. Please try again.';
      }
    } catch (e) {
      error = 'An error occurred. Please try again.';
    } finally {
      loading = false;
    }
  }

  function handleBackClick() {
    dispatch('back');
  }
</script>

<div class="signup-container">
  <h1>Sign Up</h1>
  
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
        minlength="6"
      />
    </div>

    <div class="form-group">
      <label for="confirmPassword">Confirm Password</label>
      <input
        type="password"
        id="confirmPassword"
        bind:value={confirmPassword}
        required
        placeholder="Confirm your password"
        minlength="6"
      />
    </div>

    <button type="submit" disabled={loading}>
      {loading ? 'Creating Account...' : 'Sign Up'}
    </button>
  </form>

  <p class="login-link">
    Already have an account? <button class="link-button" on:click={handleBackClick}>Login</button>
  </p>
</div>

<style>
  .signup-container {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    width: 100%;
    margin: 0 auto;
    position: relative;
  }

  h1 {
    color: #6a00ff;
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
    -webkit-appearance: none;
    appearance: none;
  }

  input:focus {
    outline: none;
    border-color: #6a00ff;
    box-shadow: 0 0 0 2px rgba(106, 0, 255, 0.1);
  }

  button {
    width: 100%;
    padding: 0.75rem;
    background-color: #6a00ff;
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
    background-color: #7c1fff;
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

  .login-link {
    margin-top: 1.5rem;
    color: #666;
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
  }

  .link-button:hover, .link-button:active {
    text-decoration: underline;
    background: none;
  }

  @media (max-width: 480px) {
    .signup-container {
      padding: 1.5rem;
      margin: 0.5rem;
      border-radius: 0;
      box-shadow: none;
      background: transparent;
    }

    h1 {
      font-size: 1.75rem;
      margin-bottom: 1.5rem;
    }

    .form-group {
      margin-bottom: 1.25rem;
    }

    input {
      padding: 0.875rem;
      font-size: 16px; /* Prevents iOS zoom on focus */
    }

    button {
      padding: 0.875rem;
      font-size: 1rem;
    }

    .error-message {
      padding: 0.875rem;
      margin-bottom: 1.25rem;
    }

    .login-link {
      margin-top: 1.25rem;
    }
  }

  @media (max-height: 600px) {
    .signup-container {
      padding: 1rem;
    }

    h1 {
      margin-bottom: 1rem;
    }

    .form-group {
      margin-bottom: 1rem;
    }
  }
</style> 