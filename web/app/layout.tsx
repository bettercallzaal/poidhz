import './globals.css';
import Link from 'next/link';
import type { Metadata } from 'next';

export const metadata: Metadata = { title: 'poidhz - The ZAO bounty board', description: 'Paid bounties for The ZAO, judged in public, with notes for everyone who enters.' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[var(--bg)] text-[var(--fg)] antialiased">
        <header className="mx-auto flex max-w-4xl items-center gap-5 px-4 py-4 text-sm">
          <Link href="/" className="font-bold tracking-tight">poidhz</Link>
          <Link href="/people">People</Link>
          <Link href="/gallery">Gallery</Link>
          <Link href="/submit">Submit</Link>
          <a href="https://farcaster.xyz/~/channel/zao" className="ml-auto">/zao</a>
        </header>
        <main className="mx-auto max-w-4xl px-4 pb-16">{children}</main>
      </body>
    </html>
  );
}
