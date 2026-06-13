import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from "@tailwindcss/vite"
export default defineConfig({
  server: {
    port: 5173, // laisse Vite sur son port par défaut
    proxy: {
      '/api': 'http://127.0.0.1:5000' // redirige les appels vers ton backend
    }
  },
  plugins: [
    react(),
    tailwindcss(),
  ]
})
