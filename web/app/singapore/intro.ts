// The story of /singapore, in the same order and words as the POIDH bounty text Zaal casts (v19b,
// vault inbox/clips/clip-20261106-102326-singapore-bounty-v19b-final.md; decisions items 263 to 297). Every
// fact comes from his own answers and his own 2016 and 2017 writing; quotes from that writing are
// framed as his. He chose to link his dad's 2014 interview (item 263). No content-schedule promises
// (item 263: "dont comit to anythign"). The bounty points to this page for the fun facts; the page keeps them.

export const PITCH = "Help me bring my story onchain through POIDH.";

export type StoryBlock = {
  text: string;
  link?: { href: string; label: string };
  images?: { src: string; alt: string }[];
};

export const STORY_BLOCKS: StoryBlock[] = [
  {
    text: "I've been a Zoroastrian priest since I was 12. Zoroastrianism is one of the first monotheistic religions [1], and there are fewer than 200,000 of us left [7].",
  },
  {
    text: "From 28 to 30 December 2026 I'm going to the 13th World Zoroastrian Congress in Singapore as a youth delegate. I got a full subsidy for my hotel, registration and meals, and I'm raising $1,000 from my community to help cover my travel.",
  },
  {
    text: "Back this bounty and send me your questions about Zoroastrianism. I'll bring them to Singapore and answer as many as I can.",
  },
  {
    text: "And as always, POIDH (pics or it didn't happen), so here's how I got here.",
  },
  {
    text: "I'm Zaal. I grew up in our local Zoroastrian community in Boston, ZAGBA (the Zoroastrian Association of Greater Boston Area). Most of my family's friends were from ZAGBA. My dad was the head priest and taught our religion classes, and my mom was vice president and later president, so I was always one of the first people there and one of the last to leave. I was just a kid, helping out wherever I could: setting up chairs and tables, running the computer and music, organizing games with the other kids in our community, then cleaning up after.",
  },
  {
    text: "Before I became a priest, I had my Navjote. It's like a first communion or a baptism. You get your sudreh and kusti, and you wear them for the rest of your life and say your daily prayers with them. The sudreh even has a tiny pocket on the front, which the Pluralism Project calls a \"pocket of merit.\" [9] The idea is that every night you think back on the good thoughts, good words and good deeds you put in it that day.",
  },
  {
    text: "Over the years I've been part of different projects about our religion, like the Pluralism Project's page on Zoroastrianism [6]. They use a photo from my Navjote:",
    link: { href: "https://pluralism.org/zoroastrianism", label: "pluralism.org/zoroastrianism" },
    images: [{ src: "https://web.archive.org/web/20260913211523im_/https://pluralism.org/sites/g/files/omnuum10836/files/styles/hwp_1_1__960x960/public/2025-09/navjote.foxboro_1.jpg?itok=cO5ZIjr_", alt: "My Navjote" }],
  },
  {
    text: "Becoming a priest started years before India, at home. As I wrote in my 2016 college essay (you can read it, and all three of my 2017 scholarship pieces, on HackMD, linked below): \"On most weekends, in between boy scouts, baseball, and homework, I spent several hours learning the ancient Avesta prayers with my Dad, also a priest.\" [1]",
    link: { href: "https://hackmd.io/MPfKtFliTIKht1F3x6Q-rQ", label: "my writing on HackMD" },
  },
  {
    text: "Then in 6th grade I went to India and spent 24 days at a Zoroastrian temple in Mumbai. From the same essay: \"I was apprehensive about the hot weather, the new foods and especially being by myself at night, sleeping on a floor mat in the temple.\" [1] And: \"I missed my family and friends, and yes, I even missed school.\" [1] After 14 days another kid from New Zealand joined me, and between prayers we played dominos and cards. \"I had made a friend for life in this short time,\" [1] and we still text here and there. Then: \"On the 24th day, wearing the white priest robe and cap for the first time, I had my ordination ceremony with my proud family looking on.\" [1]",
  },
  {
    text: "Here's my Navar, the ceremony where I became a mobed, on 20 December 2010 [5]:",
    link: { href: "https://web.archive.org/web/20141221183716/http://www.zagba.org/Navar.htm", label: "the ZAGBA Navar page (archived)" },
    images: [{ src: "https://web.archive.org/web/20141029011334im_/http://www.zagba.org/Dec20.JPG", alt: "My Navar, 20 December 2010" }],
  },
  {
    text: "When I was out for a month in 6th grade, all my friends knew, and maybe some asked questions. But I never really spoke about it a ton. I wasn't as sure of myself as I am now, and I didn't understand how blessed I was with this opportunity. Years later I finally talked about it a lot, when Maceo asked me about it as a guest on Let's Talk About Web3, the show I co-hosted with Ohnahji B (Season 3, Episode 2, the Zoroastrian part starts at 18:35) [13]. I told them: \"Out of all of the people I've ever told the name of my religion, I could count on two or three hands of people that had heard of it.\" [13] And about becoming a priest so young: \"It somewhat feels undeserved, but at a certain point you learn to be appreciative of the privilege you've been given.\" [13]",
    link: { href: "https://www.youtube.com/watch?v=W64m1eEkroU&t=1115s", label: "watch from 18:35" },
  },
  {
    text: "Priesthood runs in families. My dad, my grandfather and generations of men before me went through the same thing. I was one of the first Zoroastrian priests born and brought up in our Boston community. Until college I was my dad's right hand, his assistant priest whenever he was called. House warmings, funerals, community thanksgiving prayers, Navjotes (our coming of age ceremony, kind of like a bar mitzvah) and even one wedding, when I was 16. And every year our Ayathrem Gahambar Jashan. In my 2017 FEZANA scholarship essay I wrote: \"I have been performing ZAGBA's Annual Gahambar Jashan since the last six years along with my father and other community priests.\" [2] (A jashan is our thanksgiving prayer, and a gahambar is one of our seasonal feasts.)",
  },
  {
    text: "And at the same time, I was the Zoroastrian kid at Catholic school, K to 12. That taught me the importance of learning about other religions and customs. Junior year we had to argue for or against the death penalty, and the class was split in half. For me it was a chance to hear a lot of people's opinions, and to realize how many people's beliefs conflict with one another.",
  },
  {
    text: "That's something I appreciate about our religion. It isn't a long list of do this and don't do that. It comes down to three things: humata, hukhta, hvarshta, good thoughts, good words, good deeds. In our oldest prayers, the Gathas, Zarathushtra asks each person to listen, think it through with a clear mind, and choose for themselves [10]. Our word for religion, daena, also means conscience [11]. So your conscience is what tells you right from wrong. Or as I put it on that episode: \"In your good mind and your consciousness, what is right and what is wrong, it's up to you to be that individual.\" [13]",
  },
  {
    text: "That 2016 college essay opened with: \"Most of my classmates are amazed when I tell them I'm a priest and that last summer I performed a wedding!\" [1]",
  },
  {
    text: "My Zoroastrian community backed me in college too. Some of my college scholarships came from Zoroastrian organizations, including the Vakhshoori Foundation. In the same FEZANA essay I wrote: \"I have heard so much about Zoroastrian Congresses, and the North American Mobeds Council meetings and would love to participate in these wonderful events.\" [2] And in my Vakhshoori scholarship application: \"I would like to participate and lead the Youth Groups at Congresses and Zarathushti Sports events.\" [3] I even wrote that I hoped \"to organize a summer camp or a ski camp where Zoroastrian youth can come together.\" [3] Going to Singapore as a youth delegate is a step toward that.",
  },
  {
    text: "Then in 2022 I went to the World Zoroastrian Congress in New York. For the first time I saw Zoroastrian communities from all around the world coming together, a whole world outside my small Boston community. I learned a lot more, I made some friends, and I got to spend more time with my cousins.",
  },
  {
    text: "I also met someone there who introduced me to NFTs and blockchain. On the show I said: \"The experience that onboarded me to crypto was going to New York for our Zoroastrian World Congress. Very similar to a crypto event, ironically enough.\" [13] Someone on another podcast once told me I'm \"probably one of the first people that's ever been onboarded through a religion.\" [13] That evolved into me diving deeper, building The ZAO, a community around music and blockchain, and becoming who I am today. A lot of what I build into it is inspired by communities like ZAGBA. And these communities have supported my business ever since.",
    link: { href: "https://thezao.com", label: "thezao.com" },
  },
  {
    text: "In 2023 I went to a youth Zoroastrian congress in London and learned more about the problems facing our religion. We need to come together.",
  },
  {
    text: "The big one for me was the rift between Parsi and Iranian Zoroastrians. You can see it at these big events, in the language, the snacks, the customs. One of my best friends from ZAGBA is Iranian and I'm Parsi, and I never really knew there was any difference. We just learned more about each other.",
  },
  {
    text: "Life kept moving. I got sent out to Portland, Oregon, where there were few to no known Zoroastrians, then moved to Maine, and we bought our house. Last year my dad and I did a house warming jashan in my own home. It was my first time performing a ritual in my own home, with my fiance and her family there with us. (A house warming jashan gives thanks for the new home.)",
    images: [{ src: "/assets/singapore/housewarming-1.jpg", alt: "The jashan setup for my house warming" }, { src: "/assets/singapore/housewarming-2.jpg", alt: "My dad and me during the house warming jashan" }, { src: "/assets/singapore/housewarming-3.jpg", alt: "Family and friends after the house warming jashan" }],
  },
  {
    text: "New York, and then growing my supportive community, is what changed me. Now I'm sure of myself, and I want to share it. This is my version of art: storytelling about this long lost religion. And it's not a new idea for me. Back in 2017, in another Vakhshoori scholarship essay, I wrote: \"I believe that the Zoroastrian Religion needs to be known about more in the US.\" [4] I suggested a website or a video showing our ideals, ceremonies and traditions. Nine years later, this is me doing it.",
  },
  {
    text: "Which brings me to Singapore. It's the first World Congress since New York, the one that changed me. I've grown so much since, in my personal life and my business.",
  },
  {
    text: "I was selected for a full subsidy from ZYAB Singapore, which covers my hotel, registration and meals, but not the flight [14].",
    images: [{ src: "/assets/singapore/zyab-subsidy-letter.jpg", alt: "My ZYAB Singapore full subsidy letter" }],
  },
  {
    text: "The hotel dates should read 27 to 31 December 2026, five nights. ZYAB corrected this after sending.",
  },
  {
    text: "The flights are around $2k and are already bought, and this fundraiser helps pay them back. My family and friends are covering over half of the trip, and the extra $200 is for the extra hotel night the day before and public transport. So I'm raising $1k from my community.",
  },
  {
    text: "On this trip I want to learn more about the rift between Parsi and Iranian Zoroastrians and about both sets of customs, and bring that back to my community. (Parsis like my family are the Zoroastrians who left Iran for India over a thousand years ago to keep their faith. Iranian Zoroastrians are the ones who stayed [7].)",
  },
  {
    text: "In America the two streams come back together. Parsi and Iranian Zoroastrians share organizations, youth programs and Congresses, and a lot of us hope that one day we will just be Zoroastrians [8].",
  },
  {
    text: "I'll share as much content as I can from the Congress, fueled by the questions people send me. What I really want is a community built around learning more about my culture and faith.",
  },
  {
    text: "My communities have backed my business. This time I'm asking you to back something personal. It's not a something for something. It's supporting me on a personal journey, and the chance to ask questions and learn with me as I make content about Zoroastrianism.",
  },
  {
    text: "The goal is $1,000 from the community across every platform. On top of that, I'm putting in the first $100 on POIDH myself. The tracker below shows the current amount on all platforms.",
  },
  {
    text: "If you can support me, I'd love that. If not, I'll keep rocking out until I find a way to raise the $1,000, even if I have to keep crowdfunding after the trip.",
  },
];
export const FUN_FACTS_INTRO = 'A few fun facts, the way my dad explains them, to get your questions going:';
export const FUN_FACTS: string[] = [
  "Zoroastrianism started over 3,500 years ago in ancient Persia, with the prophet Zarathushtra.",
  "We don't worship fire. Fire is a symbol of wisdom and truth, light pushing out darkness.",
  "The kusti is 72 threads of lamb's wool, one for each of the 72 chapters of the Yasna, our main book of prayers. It loops three times around the waist for good thoughts, good words and good deeds.",
  "There are six gahambars, seasonal feasts for the skies, waters, earth, plants, animals and humans. Our Ayathrem Gahambar is one of them.",
  "Around the 10th century, Zoroastrians left Iran for India to keep their faith, and they became the Parsis. That's my side of the family.",
  "When the Parsis landed in India, the story goes, the local king sent them a glass of milk filled to the brim, meaning there was no room. A priest stirred in a spoon of sugar: we will blend in and make things sweeter. Parsis still call themselves the sugar in the milk.",
];

export const INTERVIEW_INTRO = "Want to go deeper? My dad did a three part interview in 2014 that I found while making this [12]. He's humble and would never ask for credit, but he's a big part of why I'm on this journey. As I said on Let's Talk About Web3: \"We don't have a pope or any central figure. So for me, my dad was a huge part of that father figure in my life.\" [13]";
export const INTERVIEW_PARTS: { label: string; href: string }[] = [
  { label: 'Part 1', href: "https://projectinterfaith.blogspot.com/2014/06/mr-farhad-panthaki-desribes-his-roots.html" },
  { label: 'Part 2', href: "https://projectinterfaith.blogspot.com/2014/06/mr-farhad-panthaki-brings-light-to.html" },
  { label: 'Part 3', href: "https://projectinterfaith.blogspot.com/2014/07/mr-farhad-panthaki-brings-light-to.html" },
];

export const CURIOUS = "Curious about any of it? Anyone can ask, and how to send a question is right below.";

export const WHAT_YOU_GET = "Send me any question about Zoroastrianism, big or small. I'll bring your questions with me to Singapore and answer as many as I can in the content I share from the trip. If no questions come in, I'll make a piece of content about Zoroastrianism and credit everyone who backed this trip.";

// The bounty's numbered sources, in its words (v19b). The [n] in the story match these.
export const SOURCES_NOTE = "Numbered to match the [n] in the text. Entries follow Chicago style; web pages with no date show the day I checked them.";
export const SOURCES: { text: string; href?: string }[] = [
  { text: "[1] to [4] My own writing, 2016 to 2017, posted as written on HackMD:", href: "https://hackmd.io/MPfKtFliTIKht1F3x6Q-rQ" },
  { text: "[1] Panthaki, Zaal. \"Becoming a Zoroastrian Priest.\" College essay, October 2016." },
  { text: "[2] Panthaki, Zaal. \"My Future in the ZAGBA Community.\" FEZANA scholarship essay, July 2017." },
  { text: "[3] Panthaki, Zaal. \"My Vakhshoori Scholarship Video and Pledge.\" Video script and pledge, 2017." },
  { text: "[4] Panthaki, Zaal. \"Sharing Zoroastrianism.\" Vakhshoori Foundation scholarship essay, July 2017." },
  { text: "[5] ZAGBA. \"New Navar\" (my Navar, 20 December 2010). Archived 21 December 2014.", href: "https://web.archive.org/web/20141221183716/http://www.zagba.org/Navar.htm" },
  { text: "[6] Pluralism Project, Harvard University. \"Zoroastrianism.\" Accessed 6 November 2026.", href: "https://pluralism.org/zoroastrianism" },
  { text: "[7] Pluralism Project. \"Zoroastrians in India and Iran.\" Accessed 6 November 2026.", href: "https://pluralism.org/zoroastrians-in-india-and-iran" },
  { text: "[8] Pluralism Project. \"Two Streams Converge.\" Accessed 6 November 2026.", href: "https://pluralism.org/two-streams-converge" },
  { text: "[9] Pluralism Project. \"Initiation into the Faith.\" Accessed 6 November 2026.", href: "https://pluralism.org/initiation-into-the-faith" },
  { text: "[10] Yasna 30.2. In The Gathas, translated by Stanley Insler. Zoroastrian Heritage.", href: "http://www.zoroastrian.org.uk/scripture/gathas/insler/pages/gathas-insler-y30.html" },
  { text: "[11] Antia, Kersey H. \"Philosophical Justification of the Concept of Free Will as Taught by Zarathushtra.\" Avesta.org.", href: "https://www.avesta.org/antia/Philosophical_Justification_of_the_Concept_of_Free_Will_as_Taught_by_Zarathushtra.pdf" },
  { text: "[12] Project Interfaith Blog. Three-part interview with my dad, 24 June, 30 June and 7 July 2014 (links above)." },
  { text: "[13] The ZAO. \"Let's Talk About Web 3, Season 3, Episode 2 w/ Maceo from We Them Media.\" YouTube video, 56 min, 12 November 2025. Quotes from 20:04 to 27:46, from the auto transcript, lightly edited for filler words.", href: "https://www.youtube.com/watch?v=W64m1eEkroU" },
  { text: "[14] ZYAB Singapore. Full subsidy letter to the author, 2026 (image above)." },
];
