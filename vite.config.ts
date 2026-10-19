// Frontend (React) radi na http://localhost:5173.
// Zahtjeve na /api Vite prosljeđuje backendu (Hono, server/index.ts) na portu 3000.
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: { "/api": "http://127.0.0.1:3000" },
  },
});
