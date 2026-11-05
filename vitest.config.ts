import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vitest/config';

// The spike checks its output with the editor's own rules, imported from its source.
export default defineConfig({
  resolve: { alias: { xaif: fileURLToPath(new URL('../xAIF/src/lib', import.meta.url)) } },
});
