import type { Metadata } from 'next';
import { ROUND } from '@/lib/signup';
import { SignupForm } from '@/components/SignupForm';

// Held page for round ten. Not linked from the nav and not indexed until the bounty is cast; the
// bounty text carries the URL (rounds/daily/d10/description.md, SIGNUP_URL).
export const metadata: Metadata = {
  title: 'Round 10 sign-up - poidhz',
  description: 'Artists with a song on WaveZStation sign up here for the round ten marketing rollout.',
  robots: { index: false, follow: false },
};

export default function SignupPage() {
  return (
    <>
      <h1 className="mt-6 text-3xl font-bold tracking-tight">Round 10 - sign up</h1>
      <p className="mt-2 text-sm text-[var(--muted)]">For artists with a song listed on wavezstation.com. Best marketing rollout for one song over a month. Sign-up closes {ROUND.signupClosesText}.</p>
      <p className="mt-2 text-sm">The full rules, the pot, the buys and the disclosure are in the bounty text on poidh. Read it before you sign up.</p>
      <SignupForm />
      <p className="mt-4 text-xs text-[var(--muted)]">This page shows how many songs are signed up and never who. {ROUND.emailUse}</p>
    </>
  );
}
