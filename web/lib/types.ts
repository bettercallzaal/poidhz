export type Winner = { claim_id: number; handle: string | null; wallet: string };
export type Round = {
  round: string | number; label?: string | null; folder?: string | null; closes_at?: string | null;
  bounty_id?: number; title?: string; bounty_title?: string; url?: string; status: string;
  amount_usd?: number | null; claims?: number | null; winner?: Winner | null;
};
export type Phase = 'open' | 'awaiting-pick' | 'won' | 'canceled';
export type Claim = {
  claim_id: number; bounty_id: number; wallet: string; title: string; description: string;
  image_url: string | null; accepted: boolean; handle: string | null;
};
export type Note = { claim: number; handle: string; headline: string; did_well: string; items: { title: string; body: string }[]; bounty_id: number };
export type LeaderRow = { address: string; farcaster_username?: string | null; displayName?: string | null; avatar?: string | null; fid?: number | null };
export type Person = {
  key: string; wallet: string; handle: string | null; displayName: string | null; avatar: string | null; fid: number | null;
  claims: Claim[]; bounties: number[]; wins: number[]; notes: Note[];
};
