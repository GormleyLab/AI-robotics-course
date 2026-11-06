// The review's answers and the file they travel in. No DOM here.
import { chapters } from "./chapters.mjs";

export type Question = {
  id: string;
  label: string;
  type: "text" | "long" | "number" | "date" | "choice";
  options?: string[];
  hint?: string;
};
export type Questions = {
  reviewer: Question[];
  steps: Record<string, Question[]>;
  chapterOverall: Record<string, Question[]>; // a chapter's own questions, by slug
  overall: Question[]; // asked of every chapter
};
/** Keyed "<group>.<question>": "reviewer.name", "step3.bind", "overall.hardest". */
export type Answers = Record<string, string | string[]>;

// Asked of every step, ahead of its own questions.
export const STATUS = ["Worked as written", "Worked, with changes", "Didn't work", "Not done yet"];
export const FIXES = ["Guide wording", "Picture", "Part design", "Print or fit", "Parts list"];
export const standard: Question[] = [
  { id: "status", label: "How did this step go?", type: "choice", options: STATUS },
  { id: "minutes", label: "Minutes", type: "number" },
];

// The gearbox was once the only chapter, and its answers are already saved as "overall.*".
export const overallGroup = (slug: string) => (slug === "gearbox" ? "overall" : `overall-${slug}`);
export const overallQuestions = (q: Questions, slug: string) => [...q.chapterOverall[slug], ...q.overall];

const DATA_START = "<!-- review-data ";
const DATA_END = " -->";

const has = (v: Answers[string] | undefined) => (Array.isArray(v) ? v.length > 0 : Boolean(v));
const shown = (v: Answers[string]) => (Array.isArray(v) ? v.join(", ") : v);

function lines(heading: string, group: string, questions: Question[], answers: Answers): string[] {
  const out = questions
    .filter((q) => has(answers[`${group}.${q.id}`]))
    .map((q) => `- **${q.label}** ${shown(answers[`${group}.${q.id}`])}`);
  return out.length ? [`## ${heading}`, "", ...out, ""] : [];
}

/** A file that reads as Markdown and carries the raw answers, so it can be restored. */
export function toFile(q: Questions, answers: Answers, revision: string, savedOn: string): string {
  const parts = [
    "# Assembly guide review",
    "",
    `Guide revision ${revision}. Saved ${savedOn}.`,
    "",
    ...lines("Reviewer", "reviewer", q.reviewer, answers),
  ];
  for (const step of Object.keys(q.steps)) {
    const asked = [
      ...standard,
      { id: "fix", label: "What needs fixing:", type: "text" as const },
      ...q.steps[step],
      { id: "notes", label: "Notes:", type: "long" as const },
    ];
    parts.push(...lines(`Step ${step}`, `step${step}`, asked, answers));
  }
  for (const c of chapters) {
    parts.push(...lines(`Chapter ${c.number} overall: ${c.title}`, overallGroup(c.slug), overallQuestions(q, c.slug), answers));
  }
  // "--" can't appear inside an HTML comment, and a reviewer may well type it.
  const raw = JSON.stringify(answers).replaceAll("--", "-\\u002d");
  parts.push(`${DATA_START}${raw}${DATA_END}`, "");
  return parts.join("\n");
}

export function fromFile(text: string): Answers {
  const start = text.lastIndexOf(DATA_START);
  const end = text.lastIndexOf(DATA_END);
  if (start < 0 || end < start) throw new Error("This isn't a review file saved from this page.");
  return JSON.parse(text.slice(start + DATA_START.length, end));
}

export const hasAnswers = (answers: Answers) => Object.values(answers).some(has);

/** Asked before a restore overwrites answers: a stale file would otherwise lose newer work. */
export function restoreWarning(q: Questions, current: Answers, incoming: Answers): string {
  const count = (a: Answers) => {
    const n = stepsDone(q, a);
    return `${n} ${n === 1 ? "step" : "steps"}`;
  };
  return (
    `This browser has ${count(current)} reviewed. The file has ${count(incoming)}.\n\n` +
    "Restoring replaces everything in this browser with the file, and any answers that aren't in the file are lost. Restore it?"
  );
}

export function stepsDone(q: Questions, answers: Answers): number {
  const done = (s: string) => {
    const status = answers[`step${s}.status`];
    return Boolean(status) && status !== "Not done yet";
  };
  return Object.keys(q.steps).filter(done).length;
}
