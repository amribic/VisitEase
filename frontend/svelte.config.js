import preprocess from 'svelte-preprocess';

/** @type {import('@sveltejs/vite-plugin-svelte').Options} */
const config = {
  compilerOptions: {
    dev: false
  },
  preprocess: preprocess({
    typescript: true
  })
};

export default config; 