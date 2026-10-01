import { describe, it, expect } from 'vitest';
import { extractDraft, linkParts } from './draft';

const md = `# Daily 08 - internal header (DRAFT, NOT CAST)

- **Title field:** \`ZAOstock Round 8 - Cut The Radio Session For Instagram\`
- **Reward field, suggested:** 0.0019 ETH. Fund the wallet first.

<!-- PASTE BELOW THIS LINE -->

CUT THE RADIO SESSION.

Live at https://zaostock.com/live. More: https://zaostock.com/brand

<!-- PASTE ABOVE THIS LINE -->
trailing operator notes
`;

describe('extractDraft', () => {
  const d = extractDraft(md)!;
  it('takes the title from the Title field', () => expect(d.title).toBe('ZAOstock Round 8 - Cut The Radio Session For Instagram'));
  it('returns only what is between the paste lines', () => {
    expect(d.body.startsWith('CUT THE RADIO SESSION.')).toBe(true);
    expect(d.body.endsWith('https://zaostock.com/brand')).toBe(true);
  });
  it('never leaks the operator header or footer', () => {
    expect(d.body).not.toContain('Fund the wallet');
    expect(d.body).not.toContain('trailing operator notes');
  });
  it('a file with no paste lines is not a draft', () => expect(extractDraft('# just notes')).toBeNull());
  it('says whether the file marks itself cast', () => {
    expect(d.cast).toBe(false);
    expect(extractDraft(md.replace('(DRAFT, NOT CAST)', '(CAST)'))!.cast).toBe(true);
  });
});

describe('linkParts', () => {
  it('splits text into plain and link parts', () => expect(linkParts('See https://zaostock.com/brand now')).toEqual([
    { text: 'See ' }, { text: 'https://zaostock.com/brand', href: 'https://zaostock.com/brand' }, { text: ' now' }]));
  it('keeps a sentence-ending full stop out of the link', () => expect(linkParts('Live at https://zaostock.com/live.')).toEqual([
    { text: 'Live at ' }, { text: 'https://zaostock.com/live', href: 'https://zaostock.com/live' }, { text: '.' }]));
  it('only http and https become links', () => expect(linkParts('javascript:alert(1) ftp://x')).toEqual([{ text: 'javascript:alert(1) ftp://x' }]));
});

import { isHeading } from './draft';
describe('isHeading', () => {
  it('an all-caps line is a heading', () => expect(isHeading('WHAT EARNS WEIGHT')).toBe(true));
  it('a bracketed note in lower case does not stop it', () => expect(isHeading('THE BAR (these are requirements, not preferences)')).toBe(true));
  it('a sentence is not', () => expect(isHeading('Winner takes the whole pot.')).toBe(false));
  it('a list item is not', () => expect(isHeading('- VIDEO - THE LOGO')).toBe(false));
  it('a multi-line block is not', () => expect(isHeading('DEADLINE\nmore')).toBe(false));
});

describe('extractDraft with the marker quoted in the header', () => {
  it('uses the closing marker that comes after the opening one', () => {
    const d = extractDraft('# R (CAST)\nnote quoting <!-- PASTE ABOVE THIS LINE --> in passing\n<!-- PASTE BELOW THIS LINE -->\nBODY TEXT\n<!-- PASTE ABOVE THIS LINE -->\n');
    expect(d?.body).toBe('BODY TEXT');
  });
});
