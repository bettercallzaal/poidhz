import type { Round } from './types';
export const countText = (n: number | null | undefined) => (n === null || n === undefined ? 'UNKNOWN' : String(n));
export const shortAddr = (a: string) => `${a.slice(0, 6)}...${a.slice(-4)}`;
export const usd = (n: number | null | undefined) => (n === null || n === undefined ? 'UNKNOWN' : `$${n.toFixed(2)}`);
export const potText = (r: Round) => (r.amount_usd != null ? usd(r.amount_usd) : r.amount_eth != null ? `${r.amount_eth} ETH` : 'UNKNOWN');
export const roundName = (r: Round) => r.label || (typeof r.round === 'number' || /^\d+$/.test(String(r.round)) ? `Round ${r.round}` : String(r.round));
