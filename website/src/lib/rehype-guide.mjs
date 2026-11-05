// Turns CAD/docs/assembly-guide.md into the site's page, so the guide stays one
// document and the site can't drift from it:
//
// - drops the title block and contents list (the layout supplies both);
// - points links to other repo files at GitHub, since those files aren't on the site;
// - marks TO CONFIRM so it stands out;
// - while the TA review runs, puts an empty form slot at the end of each step and
//   after the open items. src/scripts/review.ts fills the slots from
//   src/data/review-questions.json. To remove the review for students, drop
//   addReviewSlots here and the script from src/pages/assembly/index.astro.
//
// The build fails if a step has no questions, or questions have no step, so a
// renumbered guide can't quietly file answers under the wrong step.
import { readFileSync } from "node:fs";
import path from "node:path";

const REPO = "https://github.com/GormleyLab/AI-robotics-course/blob/main/";
const GUIDE_DIR = "CAD/docs/";

const questions = JSON.parse(readFileSync(new URL("../data/review-questions.json", import.meta.url), "utf8"));

const textOf = (node) =>
  node.type === "text" ? node.value : (node.children ?? []).map(textOf).join("");
const isHeading = (node, ...tags) => node.type === "element" && tags.includes(node.tagName);

function dropTitleBlock(root) {
  // Everything before the draft notice's blockquote, then "Contents" up to its rule.
  const notice = root.children.findIndex((n) => isHeading(n, "blockquote"));
  const rule = root.children.findIndex((n) => isHeading(n, "hr"));
  if (notice < 0 || rule < notice) throw new Error("assembly-guide.md: expected title, draft notice, contents, rule");
  root.children = [root.children[notice], ...root.children.slice(rule + 1)];
}

function rewrite(node) {
  if (node.type === "element" && node.tagName === "a") {
    const href = node.properties?.href ?? "";
    if (href && !/^(https?:|mailto:|#)/.test(href)) {
      node.properties.href = REPO + path.posix.normalize(GUIDE_DIR + href);
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

function addReviewSlots(root) {
  const out = [];
  const seen = new Set();
  let open = null; // the step whose form is still to be placed
  const close = () => {
    if (open !== null) out.push(slot(open));
    open = null;
  };
  for (const node of root.children) {
    if (isHeading(node, "h2", "h3", "hr")) close();
    out.push(node);
    const match = isHeading(node, "h3") && textOf(node).match(/^Step (\d+):/);
    if (match) {
      open = match[1];
      seen.add(open);
    }
  }
  close();
  out.push(slot("overall"));
  root.children = out;

  const wanted = Object.keys(questions.steps);
  const problems = [
    ...[...seen].filter((s) => !wanted.includes(s)).map((s) => `step ${s} has no entry in review-questions.json`),
    ...wanted.filter((s) => !seen.has(s)).map((s) => `review-questions.json has step ${s}, the guide doesn't`),
  ];
  if (problems.length) throw new Error(problems.join("; "));
}

export default function rehypeGuide() {
  return (root, file) => {
    if (!String(file.path ?? "").replaceAll("\\", "/").endsWith("/assembly-guide.md")) return;
    dropTitleBlock(root);
    rewrite(root);
    addReviewSlots(root);
  };
}
