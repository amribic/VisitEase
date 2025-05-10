<script lang="ts">
  // Component logic goes here
</script>

<main>
  <div class="container">
    <h1>Hello World</h1>
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

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 2rem;
    font-weight: 100;
    margin: 0;
    padding: 0;
    line-height: 1.2;
    word-wrap: break-word;
    overflow-wrap: break-word;
  }

  /* Small phones */
  @media (max-width: 360px) {
    h1 {
      font-size: 1.75rem;
    }
  }

  /* Larger phones */
  @media (min-width: 361px) and (max-width: 767px) {
    h1 {
      font-size: 2.25rem;
    }
  }

  /* Tablet and larger screens */
  @media (min-width: 768px) {
    .container {
      padding: 0 2rem;
    }
    h1 {
      font-size: 3rem;
    }
  }

  /* Desktop screens */
  @media (min-width: 1024px) {
    .container {
      padding: 0 3rem;
    }
    h1 {
      font-size: 3.5rem;
    }
  }

  /* Large desktop screens */
  @media (min-width: 1440px) {
    h1 {
      font-size: 4rem;
    }
  }

  /* Print styles */
  @media print {
    main {
      min-height: auto;
    }
    h1 {
      color: #000;
    }
  }
</style> 