// Turns the assembly guide's Markdown (CAD/docs/assembly-*.md) into the site's pages, so each
// file stays the one copy of its text and the site can't drift from it:
//
// - drops the title block (the layout supplies it), keeping the overview's draft notice;
// - points links between chapters at their pages, and links to other repo files at GitHub,
//   since those files aren't on the site;
// - marks TO CONFIRM so it stands out;
// - while the TA review runs, puts an empty form slot at the end of each step, and one at the
//   end of each chapter for the whole chapter. src/scripts/review.ts fills the slots from
//   src/data/review-questions.json. To remove the review for students, drop addReviewSlots
//   here and the script from src/layouts/Guide.astro.
//
// The build fails if a step has no questions, or questions have no step, so a renumbered
// guide can't quietly file answers under the wrong step.
import { readFileSync } from "node:fs";
import path from "node:path";
import { chapters } from "./chapters.mjs";

const REPO = "https://github.com/GormleyLab/AI-robotics-course/blob/main/";
const GUIDE_DIR = "CAD/docs/";
const SITE_BASE = "/AI-robotics-course/";
const OVERVIEW = "assembly-guide.md";

const questions = JSON.parse(readFileSync(new URL("../data/review-questions.json", import.meta.url), "utf8"));
const pageOf = new Map([[OVERVIEW, "assembly/"], ...chapters.map((c) => [c.file, `assembly/${c.slug}/`])]);

const stepPattern = /^Step (\d+):/;

// Every step in every chapter against the questions file. Each page only sees its own steps,
// so this reads the files directly. It runs once, as the build starts.
function checkAllSteps() {
  const found = chapters.flatMap((c) => {
    const text = readFileSync(new URL(`../../../CAD/docs/${c.file}`, import.meta.url), "utf8");
    return [...text.matchAll(/^## (Step \d+:)/gm)].map((m) => m[1].match(stepPattern)[1]);
  });
  const wanted = Object.keys(questions.steps);
  const problems = [
    ...found.filter((s, i) => found.indexOf(s) !== i).map((s) => `step ${s} appears twice in the guide`),
    ...found.filter((s) => !wanted.includes(s)).map((s) => `step ${s} has no entry in review-questions.json`),
    ...wanted.filter((s) => !found.includes(s)).map((s) => `review-questions.json has step ${s}, the guide doesn't`),
    ...chapters.filter((c) => !questions.chapterOverall[c.slug]).map((c) => `chapter ${c.slug} has no chapterOverall in review-questions.json`),
  ];
  if (problems.length) throw new Error(problems.join("; "));
}
checkAllSteps();

const textOf = (node) =>
  node.type === "text" ? node.value : (node.children ?? []).map(textOf).join("");
const isTag = (node, ...tags) => node.type === "element" && tags.includes(node.tagName);

function dropTitleBlock(root, isOverview) {
  const rule = root.children.findIndex((n) => isTag(n, "hr"));
  if (rule < 0) throw new Error("assembly guide: expected a title block ending in a rule");
  const notice = isOverview ? root.children.filter((n, i) => i < rule && isTag(n, "blockquote")) : [];
  root.children = [...notice, ...root.children.slice(rule + 1)];
}

function rewrite(node) {
  if (node.type === "element" && node.tagName === "a") {
    const href = node.properties?.href ?? "";
    if (href && !/^(https?:|mailto:|#)/.test(href)) {
      const [file, anchor] = href.split("#");
      node.properties.href = pageOf.has(file)
        ? `${SITE_BASE}${pageOf.get(file)}${anchor ? `#${anchor}` : ""}`
        : REPO + path.posix.normalize(GUIDE_DIR + href);
    }
  }
  if (node.type === "element" && node.tagName === "strong" && textOf(node).includes("TO CONFIRM")) {
    node.properties = { ...node.properties, className: ["to-confirm"] };
  }
  (node.children ?? []).forEach(rewrite);
}

const slot = (id) => ({
  type: "element",
  tagName: "section",
  properties: { "data-review-slot": id },
  children: [],
});

function addReviewSlots(root, chapter) {
  const out = [];
  let open = null; // the step whose form is still to be placed
  const close = () => {
    if (open !== null) out.push(slot(open));
    open = null;
  };
  for (const node of root.children) {
    if (isTag(node, "h2", "hr")) close();
    out.push(node);
    const match = isTag(node, "h2") && textOf(node).match(stepPattern);
    if (match) open = match[1];
  }
  close();
  if (chapter) out.push(slot(`overall:${chapter.slug}`));
  root.children = out;
}

export default function rehypeGuide() {
  return (root, file) => {
    const name = path.posix.basename(String(file.path ?? "").replaceAll("\\", "/"));
    if (!pageOf.has(name)) return;
    const isOverview = name === OVERVIEW;
    dropTitleBlock(root, isOverview);
    rewrite(root);
    addReviewSlots(root, chapters.find((c) => c.file === name));
  };
}
