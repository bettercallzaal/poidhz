import type { Phase, Round } from './types';
export function roundPhase(r: Round, now: Date): Phase {
  if (r.status === 'CANCELED') return 'canceled';
  if (r.winner || r.status === 'WINNER SET') return 'won';
  if (r.status === 'CLOSED') return 'closed';
  if (r.closes_at && new Date(r.closes_at).getTime() <= now.getTime()) return 'awaiting-pick';
  return 'open';
}
// Every public round, canceled included: entrants of a canceled round still made work and keep a page.
export const personBountyIds = (rs: Round[]) => publicRounds(rs).map((r) => r.bounty_id!);
export const publicRounds = (rs: Round[]) => rs.filter((r) => typeof r.bounty_id === 'number');
