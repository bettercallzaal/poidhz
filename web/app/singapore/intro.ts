// The intro and the POIDH moment of /singapore. Assembled only from Zaal's own words: his
// pitch line, his Q1 and later answers, and rulings 236, 244, 247, 248 and 251 in vault
// decisions/grill-2026-11-02-misc-morning.md (draft 4, inbox/clips/clip-20261105-192727-singapore-intro-draft4.md).
// The photos are Internet Archive copies because the original hosts are gone or block tools;
// private copies and their sources are indexed in vault notes/private/zoroastrian-photos/INDEX.md.
// No family member is named here.

export const PITCH = 'Help me bring my story onchain through POIDH.';

export const INTRO: string[] = [
  "I'm going to the 13th World Zoroastrian Congress in Singapore as a youth delegate. I grew up in the Zoroastrian community and have been a mobed, a Zoroastrian priest, since 6th grade. I got a sponsorship from ZYAB Singapore that covers a bunch of it, my hotel, registration and meals, but not the flight. My family and friends are supporting over half of the travel. The flights are around $2k and the extra $200 is for hotel and public transport, so that's why I'm working on raising $1k from my community who is interested in supporting my personal journey.",
  "One of my goals on this trip is to learn more about the rift between Parsi and Iranian Zoroastrians, learn more about both customs, and share them with my community. During the Congress I'll share a short dispatch each day, and one recap after the trip.",
  "If anyone wants to support me in my personal journey, I'd love that support. If not, I'll keep rocking out until I find a way to raise the $1,000 for this trip, even if I have to keep crowdfunding after the trip.",
];

export type MomentBlock = {
  text: string;
  link?: { href: string; label: string };
  image?: { src: string; alt: string };
};

export const NAVAR_PAGE = 'https://web.archive.org/web/20141221183716/http://www.zagba.org/Navar.htm';
export const NAVAR_PHOTO = 'https://web.archive.org/web/20141029011334im_/http://www.zagba.org/Dec20.JPG';
export const NAVJOTE_PAGE = 'https://pluralism.org/zoroastrianism';
export const NAVJOTE_PHOTO =
  'https://web.archive.org/web/20260913211523im_/https://pluralism.org/sites/g/files/omnuum10836/files/styles/hwp_1_1__960x960/public/2025-09/navjote.foxboro_1.jpg?itok=cO5ZIjr_';

export const MOMENT: MomentBlock[] = [
  {
    text: "And as always, POIDH, so here's a link to my ceremony when I was in 6th grade, when I became a mobed:",
    link: { href: NAVAR_PAGE, label: 'my Navar, 20 December 2010' },
    image: { src: NAVAR_PHOTO, alt: 'My Navar, 20 December 2010' },
  },
  {
    text: "And here's one from my Navjote. It's like your first communion or your baptism. You get your sudreh and kusti, which you are supposed to wear for the rest of your life.",
    link: { href: NAVJOTE_PAGE, label: 'the Pluralism Project' },
    image: { src: NAVJOTE_PHOTO, alt: 'My Navjote' },
  },
  {
    text: 'I have participated multiple times in doing the jashan prayer for our ZAGBA community. Our Ayathrem Gahambar Jashan is one of the ones I participated in, in the community as a child, and then I was one of the priests as a kid, in the center praying with everyone.',
  },
];
