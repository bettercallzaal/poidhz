// PENDING section of /singapore: Zaal's time in Catholic school. Nothing here renders until he
// gives the specifics and reads the draft aloud.
// His seed, raw, typed in the messenger pane Fri 6 Nov 2026 (vault
// inbox/clips/clip-20261106-063356-zoro-catholic-school-raw.md):
//   "We should prob write about my time in Catholic school aslo teaching me the importance of
//    learning about other religions and customs"
// The messenger is asking him for 2 or 3 specifics. Build the paragraphs only from his own words
// (item 232). Invent nothing: no school name, years or teachers unless he gives them.
// His specifics, raw, typed in the poidhz pane Fri 6 Nov 2026 (vault
// inbox/clips/clip-20261106-065318-zoro-story-gaps-raw.md, answer 1):
//   "k -12 i enjoyed tlaking about morality in junior year of high school"
export const SCHOOL_PENDING = false;
export const SCHOOL_HEADING: string | null = 'My time in Catholic school';
export const SCHOOL: string[] = [
  'I went to Catholic school from K to 12, and it taught me the importance of learning about other religions and customs. I enjoyed talking about morality in junior year of high school.',
];

/** True only once the section has his words and a heading. Until then the page shows nothing. */
export const schoolReady = (heading: string | null = SCHOOL_HEADING, paras: string[] = SCHOOL, pending = SCHOOL_PENDING) =>
  !pending && !!heading && paras.length > 0;
