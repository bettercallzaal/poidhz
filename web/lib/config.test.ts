import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

describe('channel is config', () => {
  it('the layout header does not hardcode a channel', () => {
    const src = readFileSync(join(__dirname, '..', 'app', 'layout.tsx'), 'utf8');
    expect(src).not.toMatch(/channel\/zao|>\/zao</);
    expect(src).toContain('sources.channel');
  });
});
