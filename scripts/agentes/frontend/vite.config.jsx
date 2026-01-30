import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  root: ".",          // ← ESTO ES CLAVE
  publicDir: "public",
});
