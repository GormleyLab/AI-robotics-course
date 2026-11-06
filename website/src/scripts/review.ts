// Fills the review slots in the guide, saves every answer in this browser as it's
// typed, and writes or restores the file the reviewer sends back.
import data from "../data/review-questions.json";
import { FIXES, fromFile, hasAnswers, overallGroup, overallQuestions, restoreWarning, standard, stepsDone, toFile, type Answers, type Question, type Questions } from "../lib/review";

declare const __GUIDE_REVISION__: string;

const questions = data as Questions;
const KEY = "assembly-review-gearbox";

function load(): Answers {
  try {
    return JSON.parse(localStorage.getItem(KEY) ?? "{}");
  } catch {
    return {};
  }
}
let answers = load();

function el<K extends keyof HTMLElementTagNameMap>(tag: K, props: Partial<HTMLElementTagNameMap[K]> = {}, ...kids: (Node | string)[]) {
  const node = Object.assign(document.createElement(tag), props);
  node.append(...kids);
  return node;
}

function field(group: string, q: Question): HTMLElement {
  const key = `${group}.${q.id}`;
  const wrap = el("div", { className: "fb-q" });
  if (q.type === "choice") {
    const opts = el("div", { className: "fb-opts" });
    for (const option of q.options ?? []) {
      const input = el("input", { type: "radio", name: key, value: option });
      input.dataset.key = key;
      opts.append(el("label", {}, input, option));
    }
    const legend = el("p", { className: "fb-label" }, q.label);
    wrap.append(legend, opts);
    return wrap;
  }
  const id = `fb-${key}`;
  const input =
    q.type === "long"
      ? el("textarea", { id, rows: 3 })
      : el("input", { id, type: q.type === "number" ? "number" : q.type === "date" ? "date" : "text" });
  if (q.type === "number") (input as HTMLInputElement).min = "0";
  if (q.hint) input.placeholder = q.hint;
  input.dataset.key = key;
  wrap.append(el("label", { className: "fb-label", htmlFor: id }, q.label), input);
  return wrap;
}

function fixField(group: string): HTMLElement {
  const key = `${group}.fix`;
  const opts = el("div", { className: "fb-opts" });
  for (const option of FIXES) {
    const input = el("input", { type: "checkbox", value: option });
    input.dataset.key = key;
    opts.append(el("label", {}, input, option));
  }
  return el("div", { className: "fb-q" }, el("p", { className: "fb-label" }, "What needs fixing, if anything?"), opts);
}

function stepForm(step: string): HTMLElement {
  const group = `step${step}`;
  return el(
    "div",
    { className: "fb" },
    el("p", { className: "fb-title" }, `Review: step ${step}`),
    ...standard.map((q) => field(group, q)),
    ...questions.steps[step].map((q) => field(group, q)),
    fixField(group),
    field(group, { id: "notes", label: "Notes: what went wrong, what you did instead, what should change", type: "long" }),
  );
}

function overallForm(slug: string): HTMLElement {
  return el(
    "div",
    { className: "fb" },
    el("p", { className: "fb-title" }, "Review: the whole chapter"),
    ...overallQuestions(questions, slug).map((q) => field(overallGroup(slug), q)),
    el("p", { className: "fb-q" }, "At the end of every session, use ",
      el("strong", {}, "Download my answers"),
      " in the bar below and send the file to Dr. Gormley, with any photos. Each file holds everything so far, so the newest replaces the earlier ones. Name each photo after its step, such as step07-1.jpg."),
  );
}

function paint() {
  document.querySelectorAll<HTMLInputElement | HTMLTextAreaElement>("[data-key]").forEach((input) => {
    const value = answers[input.dataset.key!];
    if (input instanceof HTMLInputElement && input.type === "radio") input.checked = value === input.value;
    else if (input instanceof HTMLInputElement && input.type === "checkbox")
      input.checked = Array.isArray(value) && value.includes(input.value);
    else input.value = typeof value === "string" ? value : "";
  });
  progress();
}

function progress(message?: string) {
  const total = Object.keys(questions.steps).length;
  const text = message ?? `Saved in this browser · ${stepsDone(questions, answers)} of ${total} steps reviewed`;
  document.getElementById("review-status")!.textContent = text;
}

function record(input: HTMLInputElement | HTMLTextAreaElement) {
  const key = input.dataset.key!;
  if (input instanceof HTMLInputElement && input.type === "checkbox") {
    const boxes = document.querySelectorAll<HTMLInputElement>(`input[type=checkbox][data-key="${key}"]`);
    answers[key] = [...boxes].filter((b) => b.checked).map((b) => b.value);
  } else if (input.type !== "radio" || (input as HTMLInputElement).checked) {
    answers[key] = input.value;
  }
  try {
    // Another chapter may be open in another tab, so merge rather than overwrite what it saved.
    const value = answers[key];
    answers = load();
    answers[key] = value;
    localStorage.setItem(KEY, JSON.stringify(answers));
    progress();
  } catch {
    progress("Couldn't save in this browser. Download your answers now.");
  }
}

function download() {
  const today = new Date().toISOString().slice(0, 10);
  const blob = new Blob([toFile(questions, answers, __GUIDE_REVISION__, today)], { type: "text/markdown" });
  const link = el("a", { href: URL.createObjectURL(blob), download: `assembly-review-${today}.md` });
  link.click();
  URL.revokeObjectURL(link.href);
}

async function restore(file: File) {
  try {
    const incoming = fromFile(await file.text());
    const current = load();
    if (hasAnswers(current) && !window.confirm(restoreWarning(questions, current, incoming))) {
      progress("Restore cancelled. Your answers are unchanged.");
      return;
    }
    answers = incoming;
    localStorage.setItem(KEY, JSON.stringify(answers));
    paint();
  } catch (error) {
    progress((error as Error).message);
  }
}

document.querySelectorAll<HTMLElement>("[data-review-slot]").forEach((slot) => {
  const id = slot.dataset.reviewSlot!;
  slot.append(id.startsWith("overall:") ? overallForm(id.slice("overall:".length)) : stepForm(id));
});
// Only the overview page asks who the reviewer is.
document.getElementById("review-reviewer")?.append(...questions.reviewer.map((q) => field("reviewer", q)));

document.addEventListener("input", (event) => {
  const target = event.target as HTMLInputElement | HTMLTextAreaElement;
  if (target.dataset?.key) record(target);
});
document.getElementById("review-download")!.addEventListener("click", download);
const picker = document.getElementById("review-file") as HTMLInputElement;
document.getElementById("review-restore")!.addEventListener("click", () => picker.click());
picker.addEventListener("change", () => {
  if (picker.files?.[0]) restore(picker.files[0]);
  picker.value = "";
});
paint();
