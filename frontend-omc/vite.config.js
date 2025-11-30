import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [
    react({
      jsxRuntime: 'automatic', // ensures React import isn't required in JSX
    }),
    tailwindcss(), // separate plugin
  ],
});
