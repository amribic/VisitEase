import App from './App.svelte'

console.log('Starting app initialization...');

// Add error handling
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error);
  console.error('Error details:', {
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    error: event.error
  });
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
});

let app;

// Initialize the app
try {
  console.log('Creating App instance...');
  const target = document.getElementById('app');
  console.log('Target element:', target);
  
  if (!target) {
    throw new Error('Could not find #app element');
  }

  app = new App({
    target,
  });
  console.log('App instance created successfully');
} catch (error) {
  console.error('Failed to initialize app:', error);
  const appElement = document.getElementById('app');
  if (appElement) {
    appElement.innerHTML = `
      <div style="color: red; padding: 20px; text-align: center;">
        <h1>Something went wrong</h1>
        <p>Please try refreshing the page. If the problem persists, contact support.</p>
        <pre style="text-align: left; margin-top: 20px; padding: 10px; background: #f5f5f5; border-radius: 4px;">
          ${error instanceof Error ? error.stack : String(error)}
        </pre>
      </div>
    `;
  }
}

export default app; 