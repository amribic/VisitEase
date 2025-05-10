<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function handleYes() {
    dispatch('hasNewInfo');
  }

  function handleNo() {
    dispatch('noNewInfo');
  }
</script>

<div class="check-container">
  <h1>Welcome Back!</h1>
  <p>Do you have any new information to upload?</p>
  <p class="subtext">This could be a new insurance card, doctor's report, or other medical documents.</p>
  
  <div class="buttons">
    <button class="yes-button" on:click={handleYes}>Yes, I have new information</button>
    <button class="no-button" on:click={handleNo}>No, continue to dashboard</button>
  </div>
</div>

<style>
  .check-container {
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
    color: #6a00ff;
    font-size: 2rem;
    margin: 0 0 1rem 0;
  }

  p {
    color: #666;
    margin-bottom: 1rem;
    font-size: 1.1rem;
  }

  .subtext {
    color: #888;
    font-size: 0.9rem;
    margin-bottom: 2rem;
  }

  .buttons {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  button {
    width: 100%;
    padding: 0.875rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .yes-button {
    background-color: #6a00ff;
    color: white;
  }

  .yes-button:hover {
    background-color: #7c1fff;
  }

  .no-button {
    background-color: #f5f5f5;
    color: #666;
  }

  .no-button:hover {
    background-color: #e0e0e0;
  }
</style> 