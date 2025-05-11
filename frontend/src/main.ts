import App from './App.svelte'

// Add error handling
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
});

let app;

// Initialize the app
try {
  app = new App({
    target: document.getElementById('app')!,
  });
} catch (error) {
  console.error('Failed to initialize app:', error);
  document.getElementById('app')!.innerHTML = `
    <div style="color: red; padding: 20px; text-align: center;">
      <h1>Something went wrong</h1>
      <p>Please try refreshing the page. If the problem persists, contact support.</p>
    </div>
  `;
}

export default app; 