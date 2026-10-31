import {defineConfig} from "vitest/config";
import react from "@vitejs/plugin-react";
import {viteSingleFile} from "vite-plugin-singlefile";

// One self-contained dist/index.html: the server sends one file and the UI test opens it from disk.
export default defineConfig({
  plugins: [react(), viteSingleFile()],
  server: {proxy: {"/api": {target: "http://127.0.0.1:7980", changeOrigin: true}}},  // the server checks Host
  test: {environment: "node", include: ["src/**/*.test.ts"]},
});
