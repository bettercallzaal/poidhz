// The repo's .vercelignore keeps unsent outbound copy off poidhz.com. The app serves copies of
// rounds/ and docs/, so it must honour the same file or it republishes what that file withholds.
export function parseIgnore(text) {
  return text.split('\n').map((l) => l.trim()).filter((l) => l && !l.startsWith('#')).map((p) => {
    const dir = p.endsWith('/');
    const body = p.replace(/^\//, '').replace(/\/$/, '').split('*').map((s) => s.replace(/[.+?^${}()|[\]\\]/g, '\\$&')).join('[^/]*');
    return new RegExp(dir ? `^${body}/` : `^${body}(/|$)`);
  });
}
export const isIgnored = (rel, pats) => pats.some((re) => re.test(rel));
