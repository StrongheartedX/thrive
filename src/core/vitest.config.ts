import { defineConfig } from "vitest/config";

export default defineConfig({
  resolve: {
    alias: {
      "#/core": "./jupiter/core",
    },
  },
  test: {
    environment: "node",
    include: ["jupiter/core/**/*.test.ts"],
  },
});
