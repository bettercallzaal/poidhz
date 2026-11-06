// The story of /singapore, in the same order and words as the POIDH bounty text Zaal casts (v15c,
// vault inbox/clips/clip-20261106-080613-singapore-bounty-v15c-submit.md; decisions items 263 to 265). Every
// fact comes from his own answers and his own 2016 and 2017 essays. He chose
// to link his dad's 2014 interview (item 263). No content-schedule promises (item 263: "dont comit to anythign").

export const PITCH = "Help me bring my story onchain through POIDH.";

export type StoryBlock = {
  text: string;
  link?: { href: string; label: string };
  images?: { src: string; alt: string }[];
};

export const STORY_BLOCKS: StoryBlock[] = [
  {
    text: "In 6th grade I went to India for a month to become a mobed, a Zoroastrian priest. I'm Zaal, and that's where this story starts.",
  },
  {
    text: "And as always, POIDH (pics or it didn't happen), so here's my Navar, the ceremony where I became a mobed:",
    link: { href: "https://web.archive.org/web/20141221183716/http://www.zagba.org/Navar.htm", label: "my Navar, 20 December 2010" },
    images: [{ src: "https://web.archive.org/web/20141029011334im_/http://www.zagba.org/Dec20.JPG", alt: "My Navar, 20 December 2010" }],
  },
  {
    text: "And here's my Navjote. It's like a first communion or a baptism. You get your sudreh and kusti, and you wear them for the rest of your life.",
    link: { href: "https://pluralism.org/zoroastrianism", label: "the Pluralism Project" },
    images: [{ src: "https://web.archive.org/web/20260913211523im_/https://pluralism.org/sites/g/files/omnuum10836/files/styles/hwp_1_1__960x960/public/2025-09/navjote.foxboro_1.jpg?itok=cO5ZIjr_", alt: "My Navjote" }],
  },
  {
    text: "I grew up in our local Zoroastrian community in Boston, ZAGBA (the Zoroastrian Association of Greater Boston Area). My dad was the head priest and taught our religion classes, and my mom was vice president (she's the president now), so I was always one of the first people there and one of the last to leave. Setting up chairs and tables, running the computer and music, organizing games for the kids, then cleaning up after.",
  },
  {
    text: "Becoming a priest started years before India, at home. Most weekends, in between Boy Scouts, baseball and homework, I spent hours learning the ancient Avesta prayers with my dad. Then I spent 24 days at a Zoroastrian temple in Mumbai, sleeping on a floor mat and memorizing prayers. I missed my family, and yes, I even missed school. After 14 days another kid from New Zealand joined me, and between prayers we played dominos and cards. We still text. On the 24th day I wore the white priest robe and cap for the first time, with my family looking on.",
  },
  {
    text: "I was the first Zoroastrian priest born and brought up in our Boston community. Until college I was my dad's right hand, his assistant priest whenever he was called. House warmings, funerals, community thanksgiving prayers, Navjotes (our coming of age ceremony, kind of like a bar mitzvah) and even one wedding, when I was 16. And every year our Ayathrem Gahambar Jashan, where I did the prayers alongside my dad and the other community priests. (A jashan is our thanksgiving prayer, and a gahambar is one of our seasonal feasts.)",
  },
  {
    text: "And at the same time, I was the Zoroastrian kid at Catholic school, K to 12. That taught me the importance of learning about other religions and customs. Junior year we had to argue for or against the death penalty, and the class was split in half. For me it was a chance to hear a lot of people's opinions, and to realize how many people's beliefs conflict with one another.",
  },
  {
    text: "That's something I appreciate about our religion. It isn't a long list of do this and don't do that. It comes down to three things: humata, hukhta, hvarshta, good thoughts, good words, good deeds. In our oldest prayers, the Gathas, Zarathushtra asks each person to listen, think it through with a clear mind, and choose for themselves. Our word for religion, daena, also means conscience. So your conscience is what tells you right from wrong.",
  },
  {
    text: "When I was out for a month in 6th grade, all my friends knew, and maybe some asked questions. But I never really spoke about it a ton. I wasn't as sure of myself as I am now, and I didn't understand how blessed I was with this opportunity.",
  },
  {
    text: "Then in 2022 I went to the World Zoroastrian Congress in New York. For the first time I saw Zoroastrian communities from all around the world coming together, a whole world outside my small Boston community. I learned a lot more, I made some friends, and I got to spend more time with my cousins.",
  },
  {
    text: "I also met someone there who introduced me to NFTs and blockchain. That evolved into me diving deeper, building The ZAO, a community around music and blockchain, and becoming who I am today. A lot of what I build into it is inspired by communities like ZAGBA. And these communities have supported my business ever since.",
    link: { href: "https://thezao.com", label: "thezao.com" },
  },
  {
    text: "New York, and then growing my supportive community, is what changed me. Now I'm sure of myself, and I want to share it. This is my version of art: storytelling about this long lost religion.",
  },
  {
    text: "In 2023 I went to a youth Zoroastrian congress in London and learned more about the problems facing our religion. There are around 100k to 200k known Zoroastrians in the world. We need to come together.",
  },
  {
    text: "The big one for me was the rift between Parsi and Iranian Zoroastrians. You can see it at these big events, in the language, the snacks, the customs. One of my best friends from ZAGBA is Iranian and I'm Parsi, and I had never really known about it.",
  },
  {
    text: "Life kept moving. I got sent out to Portland, Oregon, where there were few to no known Zoroastrians, then moved to Maine, and we bought our house. Last year my dad and I did a house warming jashan in my own home. It was my first time performing a ritual in my own home, with my fiance and her family there with us. (A jashan is our thanksgiving prayer, so a house warming jashan gives thanks for the new home.)",
    images: [{ src: "/assets/singapore/housewarming-1.jpg", alt: "The jashan setup for my house warming" }, { src: "/assets/singapore/housewarming-2.jpg", alt: "My dad and me during the house warming jashan" }, { src: "/assets/singapore/housewarming-3.jpg", alt: "Family and friends after the house warming jashan" }],
  },
  {
    text: "Now I'm going to the 13th World Zoroastrian Congress in Singapore as a youth delegate, 28 to 30 December 2026. It's the first World Congress since New York, the one that changed me. I've grown so much since, in my personal life and my business.",
  },
  {
    text: "I was selected for a full subsidy from ZYAB Singapore, which covers my hotel, registration and meals, but not the flight.",
    images: [{ src: "/assets/singapore/zyab-subsidy-letter.jpg", alt: "My ZYAB Singapore full subsidy letter" }],
  },
  {
    text: "The hotel dates should read 27 to 31 December 2026, five nights. ZYAB corrected this after sending.",
  },
  {
    text: "The flights are around $2k and are already bought, and this fundraiser helps pay them back. My family and friends are covering over half of the trip, and the extra $200 is for the extra hotel night the day before and public transport. So I'm raising $1k from my community.",
  },
  {
    text: "On this trip I want to learn more about the rift between Parsi and Iranian Zoroastrians and about both sets of customs, and bring that back to my community. (Parsis like my family are the Zoroastrians who left Iran for India over a thousand years ago to keep their faith. Iranian Zoroastrians are the ones who stayed.)",
  },
  {
    text: "I'll share as much content as I can from the Congress, fueled by the questions people send me. What I really want is a community built around learning more about my culture and faith.",
  },
  {
    text: "My communities have backed my business. This time I'm asking you to back something personal. It's not a something for something. It's supporting me on a personal journey, and the chance to ask questions and learn with me as I make content about Zoroastrianism.",
  },
  {
    text: "The goal is $1,000 from the community across every platform. On top of that, I'm putting in the first $100 on POIDH myself. The tracker below shows the current amount on all platforms, and I update it each week.",
  },
  {
    text: "If you can support me, I'd love that. If not, I'll keep rocking out until I find a way to raise the $1,000, even if I have to keep crowdfunding after the trip.",
  },
];

export const FUN_FACTS_INTRO = 'A few fun facts, the way my dad explains them, to get your questions going:';
export const FUN_FACTS: string[] = [
  "Zoroastrianism started over 3,500 years ago in ancient Persia, with the prophet Zarathushtra.",
  "We don't worship fire. Fire is a symbol of wisdom and truth, light pushing out darkness.",
  "The kusti is 72 strands of lamb's wool, looped three times around the waist for good thoughts, good words and good deeds.",
  "There are six gahambars, seasonal feasts for the skies, waters, earth, plants, animals and humans. Our Ayathrem Gahambar is one of them.",
  "Around the 10th century, Zoroastrians left Iran for India to keep their faith, and they became the Parsis. That's my side of the family.",
];

export const INTERVIEW_INTRO = "Want to go deeper? My dad did a three part interview in 2014 that I found while making this. He's humble and would never ask for credit, but he's a big part of why I'm on this journey.";
export const INTERVIEW_PARTS: { label: string; href: string }[] = [
  { label: 'Part 1', href: "https://projectinterfaith.blogspot.com/2014/06/mr-farhad-panthaki-desribes-his-roots.html" },
  { label: 'Part 2', href: "https://projectinterfaith.blogspot.com/2014/06/mr-farhad-panthaki-brings-light-to.html" },
  { label: 'Part 3', href: "https://projectinterfaith.blogspot.com/2014/07/mr-farhad-panthaki-brings-light-to.html" },
];

export const CURIOUS = "Curious about any of it? Anyone can ask, and how to send a question is right below.";

export const WHAT_YOU_GET = "Send me any question about Zoroastrianism, big or small. I'll bring your questions with me to Singapore and answer as many as I can in the content I share from the trip. If no questions come in, I'll make a piece of content about Zoroastrianism and credit everyone who backed this trip.";
