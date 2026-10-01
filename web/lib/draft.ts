// A round's bounty text, lifted out of its description.md for a page someone can be sent.
// Only what sits between the paste lines is shown: the operator notes above and below
// (wallet funding, suggested reward) are not for readers.
const START = '<!-- PASTE BELOW THIS LINE -->';
const END = '<!-- PASTE ABOVE THIS LINE -->';

export type Draft = { title: string; body: string; cast: boolean };

export function extractDraft(md: string): Draft | null {
  const a = md.indexOf(START);
  // The closing marker is the first one AFTER the opening marker; a header may quote it.
  const b = a < 0 ? -1 : md.indexOf(END, a + START.length);
  if (a < 0 || b < 0) return null;
  const body = md.slice(a + START.length, b).trim();
  if (!body) return null;
  const heading = md.split('\n')[0] ?? '';
  const title = md.match(/\*\*Title field:\*\*\s*`([^`]+)`/)?.[1] ?? body.split('\n')[0];
  return { title, body, cast: /\(CAST\)/.test(heading) };
}

export type Part = { text: string; href?: string };

export function linkParts(text: string): Part[] {
  const out: Part[] = [];
  let last = 0;
  for (const m of text.matchAll(/https?:\/\/[^\s)<>]+/g)) {
    let url = m[0];
    const trail = url.match(/[.,;:!?]+$/)?.[0] ?? '';
    if (trail) url = url.slice(0, -trail.length);
    const i = m.index!;
    if (i > last) out.push({ text: text.slice(last, i) });
    out.push({ text: url, href: url });
    last = i + url.length;
  }
  if (last < text.length) out.push({ text: text.slice(last) });
  return out;
}

// Bounty text marks sections with a line in capitals, sometimes followed by a note in brackets.
export function isHeading(block: string): boolean {
  if (block.includes('\n') || block.startsWith('-')) return false;
  const core = block.replace(/\s*\([^)]*\)\s*$/, '');
  return core.length > 0 && core.length < 80 && /[A-Z]/.test(core) && core === core.toUpperCase();
}
