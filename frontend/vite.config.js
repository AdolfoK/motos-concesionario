import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// En desarrollo (vite dev) se hace proxy de /api y /media hacia el backend.
// En produccion (nginx) ese proxy lo realiza nginx.conf.
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      "/api": "http://localhost:8000",
      "/media": "http://localhost:8000",
    },
  },
});
