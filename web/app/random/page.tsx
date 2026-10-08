import { RandomDeck } from '@/components/RandomDeck';
import { loadRandom } from '@/lib/random-load';

export const dynamic = 'force-dynamic';
export const metadata = { title: 'Random poidh bounty - poidhz', description: 'A random bounty from all of poidh, Base and Arbitrum.' };

// The first pick is rendered on the server so the page shows a bounty at once;
// the deck then loads more ahead in the browser.
export default async function RandomPage() {
  return <RandomDeck first={await loadRandom()} />;
}
