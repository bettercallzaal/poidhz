'use client';
import { useEffect, useState } from 'react';
import { ROUND, checkEmail } from '@/lib/signup';

type Status = { open: boolean; storeReady: boolean; count: number | null };

export function SignupForm() {
  const [status, setStatus] = useState<Status | null>(null);
  const [email, setEmail] = useState('');
  const [step, setStep] = useState<1 | 2>(1);
  const [artist, setArtist] = useState('');
  const [song, setSong] = useState('');
  const [handle, setHandle] = useState('');
  const [where, setWhere] = useState('');
  const [errors, setErrors] = useState<string[]>([]);
  const [done, setDone] = useState<{ title?: string; artist?: string } | null>(null);
  const [busy, setBusy] = useState(false);
  useEffect(() => { fetch('/api/signup').then((r) => r.json()).then(setStatus).catch(() => setStatus({ open: false, storeReady: false, count: null })); }, []);
  const field = 'mt-1 w-full rounded border border-[var(--line)] bg-transparent px-3 py-2 text-sm';
  const btn = 'rounded bg-[var(--accent)] px-4 py-2 text-sm font-semibold text-[var(--on-accent)] disabled:opacity-40';

  if (done) return (
    <section className="mt-6 rounded-lg border border-[var(--line)] p-4 text-sm">
      <p className="font-semibold">You are in.</p>
      <p className="mt-2">{done.title ? `${done.title} by ${done.artist}` : 'Your song'} is signed up for round ten. The rollout runs from sign-up close to the deadline in the bounty text. Claim on poidh with the record when you are done.</p>
    </section>
  );

  async function submit() {
    setBusy(true); setErrors([]);
    try {
      const r = await fetch('/api/signup', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email, artist, song, handle, where }) });
      const j = await r.json();
      if (j.ok) setDone(j.song); else setErrors(j.errors ?? ['something went wrong']);
    } catch { setErrors(['could not reach the server; try again']); }
    setBusy(false);
  }

  return (
    <section className="mt-6 rounded-lg border border-[var(--line)] p-4">
      {status && !status.open && <p className="text-sm text-[var(--warn)]">Sign-up closed at {ROUND.signupClosesText}.</p>}
      {status && status.open && !status.storeReady && <p className="text-sm text-[var(--warn)]">Sign-up is not switched on yet. You can fill this in, and it will tell you nothing was sent anywhere.</p>}
      {status?.count != null && <p className="text-sm text-[var(--muted)]">{status.count} {status.count === 1 ? 'song is' : 'songs are'} signed up.</p>}
      {step === 1 ? (
        <form onSubmit={(e) => { e.preventDefault(); const err = checkEmail(email); if (err) setErrors([err]); else { setErrors([]); setStep(2); } }}>
          <label className="mt-3 block text-sm">Your email<input className={field} type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" /></label>
          <p className="mt-2 text-xs text-[var(--muted)]">{ROUND.emailUse}</p>
          <button type="submit" className={`${btn} mt-3`} disabled={!status?.open}>Next</button>
        </form>
      ) : (
        <form onSubmit={(e) => { e.preventDefault(); submit(); }}>
          <p className="text-sm">Email: <span className="font-semibold">{email}</span> <button type="button" className="ml-2 text-xs underline" onClick={() => setStep(1)}>change</button></p>
          <label className="mt-3 block text-sm">Artist name<input className={field} value={artist} onChange={(e) => setArtist(e.target.value)} maxLength={80} /></label>
          <label className="mt-3 block text-sm">Your song&apos;s page on WaveZStation<input className={field} value={song} onChange={(e) => setSong(e.target.value)} placeholder="https://wavezstation.com/song/..." /></label>
          <label className="mt-3 block text-sm">X or Farcaster handle (optional)<input className={field} value={handle} onChange={(e) => setHandle(e.target.value)} maxLength={60} placeholder="@you" /></label>
          <label className="mt-3 block text-sm">Where the rollout will be posted<textarea className={field} rows={3} value={where} onChange={(e) => setWhere(e.target.value)} maxLength={300} placeholder="X and TikTok, plus two shows in November" /></label>
          <p className="mt-2 text-xs text-[var(--muted)]">One song, one artist, one entry. The song must already be listed on wavezstation.com.</p>
          <button type="submit" className={`${btn} mt-3`} disabled={busy || !status?.open}>{busy ? 'Checking the song' : 'Sign up'}</button>
        </form>
      )}
      {errors.length > 0 && <ul className="mt-3 list-disc pl-5 text-sm text-[var(--warn)]">{errors.map((e) => <li key={e}>{e}</li>)}</ul>}
    </section>
  );
}
