import { defineConfig } from 'vitest/config';
import { resolve } from 'node:path';
export default defineConfig({ test: { include: ['lib/**/*.test.ts', 'scripts/**/*.test.mjs'] }, resolve: { alias: { '@': resolve(__dirname) } } });
