import type { Round } from './types';
export const countText = (n: number | null | undefined) => (n === null || n === undefined ? 'UNKNOWN' : String(n));
export const shortAddr = (a: string) => `${a.slice(0, 6)}...${a.slice(-4)}`;
export const usd = (n: number | null | undefined) => (n === null || n === undefined ? 'UNKNOWN' : `$${n.toFixed(2)}`);
export const roundName = (r: Round) => r.label || (typeof r.round === 'number' || /^\d+$/.test(String(r.round)) ? `Round ${r.round}` : String(r.round));
