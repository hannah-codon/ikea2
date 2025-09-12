import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import checker from 'vite-plugin-checker'

export default defineConfig({
  plugins: [react(),
  checker({
    typescript: true,
  })
  ],
  base: "/",
  build: {
    outDir: 'build'
  },
  server: {
    port: 3000,
  },
});
