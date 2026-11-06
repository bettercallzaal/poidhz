// The story of /singapore, in the same order and words as the POIDH bounty text (v12d, vault
// inbox/clips/clip-20261106-073704-singapore-bounty-v12d.md). Every fact comes from Zaal's own answers,
// saved raw in the vault inbox/clips (zoro-q1, q28, q31, catholic-school, story-gaps, catholic-q2,
// what-changed, ny2022, london, little-bits); structure follows the Story Spine and GoFundMe's story
// guide at his ask on 6 Nov 2026. Fun facts are retold from his dad's 2014 Project Interfaith interview;
// his dad is not named and the interview is not linked. No family member is named here.

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
    text: "I grew up in our local Zoroastrian community in Boston, ZAGBA. My dad was the main priest and my mom was a vice president, so I was always one of the first people there and one of the last to leave after cleaning up.",
  },
  {
    text: "Until college I was my dad's right hand, his assistant priest whenever he was called. House warmings, funerals, celebrations, even one wedding. And our Ayathrem Gahambar Jashan, in the center praying with everyone.",
  },
  {
    text: "And at the same time, I was the Zoroastrian kid at Catholic school, K to 12. That taught me the importance of learning about other religions and customs. Junior year we had to argue for or against the death penalty, and the class was split in half. For me it was a chance to hear a lot of people's opinions, and to realize how many people's beliefs conflict with one another.",
  },
  {
    text: "That's something I appreciate about our religion. It's less prescriptive, less do this action and that action. It's good thoughts, good words, good deeds, and your conscience will tell you right from wrong.",
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
    text: "Life kept moving. I got sent out to Portland, Oregon, where there were few to no known Zoroastrians, then moved to Maine, and we bought our house. Last year my dad and I did a jashan in my own home, as the house warming.",
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
    text: "The flights are around $2k and are already bought, and this fundraiser helps pay them back. My family and friends are covering over half of the trip, and the extra $200 is for the extra hotel night the day before and public transport. So I'm raising $1k from my community.",
  },
  {
    text: "On this trip I want to learn more about the rift and about both customs, and bring that back.",
  },
  {
    text: "I'll share a short dispatch each day of the Congress and one recap after. What I really want is a community built around learning more about my culture and faith.",
  },
  {
    text: "My communities have backed my business. This time I'm asking you to back something personal. It's not a something for something. It's supporting me on a personal journey, and the chance to ask questions and learn with me as I make content about Zoroastrianism.",
  },
  {
    text: "The goal is $1,000 across every platform, and I'm putting in the first $100 on POIDH myself. The tracker below shows the current amount on all platforms, and I update it each week.",
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
