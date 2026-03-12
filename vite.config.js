import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  base: '/vocab-agent/',
  server: {
    port: 3001,
    open: true,
  },
  build: mode === 'lib' ? {
    outDir: 'dist-lib',
    lib: {
      entry: 'src/VocabAgent.jsx',
      name: 'VocabAgent',
      formats: ['es', 'umd'],
      fileName: (format) => `vocab-agent.${format}.js`,
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
  } : {
    outDir: 'dist',
  },
}));
