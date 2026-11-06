// Walks the review as the TA would, in the installed Microsoft Edge, against a
// running preview or the live site. Takes screenshots into qa/out/.
//
//   node qa/review_check.mjs [base-url, default the local preview]
//
// Exits non-zero on any failed check, console error or broken image.
import { chromium } from "playwright";
import fs from "node:fs";

const base = (process.argv[2] ?? "http://127.0.0.1:4321/AI-robotics-course").replace(/\/$/, "");
const out = new URL("./out/", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
fs.mkdirSync(out, { recursive: true });

const failures = [];
const check = (ok, what) => {
  console.log(`${ok ? "ok  " : "FAIL"} ${what}`);
  if (!ok) failures.push(what);
};

const browser = await chromium.launch({ channel: "msedge" });
const open = async (viewport) => {
  const context = await browser.newContext({ viewport, acceptDownloads: true });
  const page = await context.newPage();
  page.on("console", (m) => { if (m.type() === "error") failures.push(`console: ${m.text()}`); });
  page.on("pageerror", (e) => failures.push(`page error: ${e.message}`));
  return { context, page };
};

// The gate, then the home page's link into the guide.
const { context, page } = await open({ width: 1360, height: 900 });
await page.goto(`${base}/assembly/`);
check(await page.locator("#gate-pw").isVisible(), "the gate shows on first visit");
await page.fill("#gate-pw", "1");
await page.click("#gate-form button");
check(await page.locator("#gate-err").isVisible(), "a wrong password is refused");
await page.fill("#gate-pw", "444");
await page.click("#gate-form button");
check(await page.locator("article h3").first().isVisible(), "the right password opens the guide");

// Every page: its forms, its pictures and its links. Forms and pictures are counted per page,
// so a step or picture can't slip onto the wrong chapter.
await page.evaluate(() => { document.documentElement.style.scrollBehavior = "auto"; });
const PAGES = [
  { path: "", forms: 0, pictures: 0 },
  { path: "gearbox/", forms: 17, pictures: 29 },
  { path: "base-joint-1/", forms: 12, pictures: 17 },
  { path: "hinge-joint-2/", forms: 8, pictures: 11 },
];
const crossLinks = [];
for (const { path, forms, pictures } of PAGES) {
  const name = path || "overview";
  await page.goto(`${base}/assembly/${path}`);
  const slots = await page.locator("[data-review-slot]").count();
  check(slots === forms, `${name}: ${forms} review forms (${slots})`);
  check(!(await page.locator("article h1").count()), `${name}: the title block is gone`);
  const images = page.locator("article img");
  const count = await images.count();
  for (let i = 0; i < count; i++) await images.nth(i).scrollIntoViewIfNeeded();
  await page.waitForLoadState("networkidle");
  const broken = await images.evaluateAll((all) => all.filter((i) => !i.complete || !i.naturalWidth).map((i) => i.src));
  check(count === pictures && broken.length === 0, `${name}: all pictures load (${count}, broken ${broken.length})`);
  const hrefs = await page.locator("article a").evaluateAll((all) => all.map((a) => a.getAttribute("href")));
  const site = new URL(base).pathname + "/assembly/";
  crossLinks.push(...hrefs.filter((h) => h.startsWith(site)));
  const local = hrefs.filter((h) => !/^(https?:|#)/.test(h) && !h.startsWith(site));
  check(local.length === 0, `${name}: no link points at a file the site doesn't have (${local.join(", ")})`);
  for (const h of hrefs.filter((x) => x.startsWith("#"))) {
    check(await page.locator(`[id="${h.slice(1)}"]`).count() === 1, `${name}: anchor ${h} exists`);
  }
}
for (const link of new Set(crossLinks)) {
  const [where, anchor] = link.split("#");
  const answer = await page.goto(new URL(where, base).href);
  check(answer.ok(), `link ${where} opens`);
  if (anchor) check(await page.locator(`[id="${anchor}"]`).count() === 1, `link ${link} finds its heading`);
}

// Moving between chapters from the page itself.
await page.goto(`${base}/assembly/`);
await page.locator('main a:has-text("Hinge and joint 2")').first().click();
await page.waitForURL("**/assembly/hinge-joint-2/");
check(await page.locator('nav[aria-label="Other chapters"] a:has-text("Base and joint 1")').count() === 1, "a chapter links to the one before");
check(await page.locator('nav[aria-label="Guide contents"] a[aria-current="page"]').textContent() === "3. Hinge and joint 2", "the sidebar marks the current chapter");

// Answer a mix of field types, with text that could break the file format.
const tricky = 'Bound hard -- see "photo" --> then eased <off>\nsecond line';
await page.goto(`${base}/assembly/`);
await page.fill('[data-key="reviewer.name"]', "Test TA");
await page.goto(`${base}/assembly/hinge-joint-2/`);
await page.fill('[data-key="overall-hinge-joint-2.hardest"]', "Fitting the coupling");
await page.goto(`${base}/assembly/gearbox/`);
await page.fill('[data-key="overall.hardest"]', "Step 7");
await page.check('input[data-key="step3.status"][value="Worked, with changes"]');
await page.check('input[data-key="step3.bind"][value="Bind"]');
await page.check('input[data-key="step3.fix"][value="Part design"]');
await page.check('input[data-key="step3.fix"][value="Picture"]');
await page.fill('[data-key="step3.notes"]', tricky);
await page.fill('[data-key="step7.tries"]', "4");
check((await page.textContent("#review-status")).includes("1 of 34"), "the bar counts reviewed steps");

// Another chapter's answers go in the same store, even from a tab opened before this one saved.
const other = await context.newPage();
await other.goto(`${base}/assembly/base-joint-1/`);
await page.fill('[data-key="step7.trick"]', "from the first tab");
await other.check('input[data-key="step17.status"][value="Worked as written"]');
await page.reload();
check(await page.inputValue('[data-key="step7.trick"]') === "from the first tab", "a second tab doesn't overwrite the first");
await other.close();
check((await page.textContent("#review-status")).includes("2 of 34"), "the count covers every chapter");

const step3 = page.locator('[data-review-slot="3"]');
await step3.scrollIntoViewIfNeeded();
await page.screenshot({ path: `${out}desktop_step3_form.png` });

await page.reload();
check(await page.inputValue('[data-key="step3.notes"]') === tricky, "text survives a reload");
check(await page.isChecked('input[data-key="step3.bind"][value="Bind"]'), "a choice survives a reload");
check(await page.isChecked('input[data-key="step3.fix"][value="Picture"]'), "a tick box survives a reload");

// Download, read the file, restore it into a fresh browser.
const [download] = await Promise.all([page.waitForEvent("download"), page.click("#review-download")]);
const file = `${out}${download.suggestedFilename()}`;
await download.saveAs(file);
const text = fs.readFileSync(file, "utf8");
check(/assembly-review-\d{4}-\d\d-\d\d\.md$/.test(file), "the file has a dated name");
check(text.includes("## Step 3") && text.includes("**Which carrier screw") === false, "the file skips unanswered questions");
check(text.includes("## Step 17") && text.includes("Test TA"), "one file holds every page's answers");
check(text.includes("## Chapter 1 overall") && text.includes("Step 7"), "the file has chapter 1's overall review, in its old keys");
check(text.includes("## Chapter 3 overall") && text.includes("Fitting the coupling"), "the file has chapter 3's overall review");
check(!text.includes("## Chapter 2 overall"), "a chapter with no overall answers is left out");
check(text.includes("Part design, Picture") || text.includes("Picture, Part design"), "the file lists the ticks");
check(/Guide revision \w+/.test(text), "the file records the guide revision");
const comment = text.slice(text.lastIndexOf("<!-- review-data"));
check(comment.indexOf("-->") === comment.lastIndexOf("-->"), "reviewer text can't end the data comment early");

const fresh = await open({ width: 390, height: 844 });
await fresh.context.addInitScript(() => localStorage.setItem("spr-gate", "ok"));
await fresh.page.goto(`${base}/assembly/gearbox/`);
check(await fresh.page.inputValue('[data-key="step3.notes"]') === "", "a new browser starts empty");
await fresh.page.setInputFiles("#review-file", file);
await fresh.page.waitForFunction(() => document.querySelector('[data-key="step3.notes"]').value !== "");
check(await fresh.page.inputValue('[data-key="step3.notes"]') === tricky, "restore brings back tricky text exactly");
check(await fresh.page.isChecked('input[data-key="step3.bind"][value="Bind"]'), "restore brings back choices");
await fresh.page.setInputFiles("#review-file", { name: "x.md", mimeType: "text/markdown", buffer: Buffer.from("not ours") });
await fresh.page.waitForFunction(() => document.getElementById("review-status").textContent.includes("isn't a review file"));
check(await fresh.page.inputValue('[data-key="step3.notes"]') === tricky, "a wrong file changes nothing");

// Restoring over existing answers asks first: an old file would otherwise lose newer work.
const answerDialog = (accept) => new Promise((resolve) => {
  fresh.page.once("dialog", async (dialog) => {
    const message = dialog.message();
    await (accept ? dialog.accept() : dialog.dismiss());
    resolve(message);
  });
});
await fresh.page.fill('[data-key="step3.notes"]', "newer work");
let asked = answerDialog(false);
await fresh.page.setInputFiles("#review-file", file);
const warning = await asked;
check(warning.includes("replaces everything") && warning.includes("2 steps"), "restoring over answers warns, with the counts");
await fresh.page.waitForFunction(() => document.getElementById("review-status").textContent.includes("cancelled"));
check(await fresh.page.inputValue('[data-key="step3.notes"]') === "newer work", "cancelling keeps the newer answers");
await fresh.page.reload();
check(await fresh.page.inputValue('[data-key="step3.notes"]') === "newer work", "cancelling leaves the saved answers alone too");
asked = answerDialog(true);
await fresh.page.setInputFiles("#review-file", file);
await asked;
await fresh.page.waitForFunction((want) => document.querySelector('[data-key="step3.notes"]').value === want, tricky);
check(true, "accepting replaces them with the file");

// Phone: nothing wider than the screen, and pictures open full size.
const overflow = await fresh.page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
check(overflow <= 0, `no sideways scroll on a phone (${overflow}px over)`);
await fresh.page.locator('[data-review-slot="3"]').scrollIntoViewIfNeeded();
await fresh.page.screenshot({ path: `${out}phone_step3_form.png` });
await fresh.page.locator("article img").nth(3).click();
check(await fresh.page.locator("#zoom").isVisible(), "tapping a picture opens it");
await fresh.page.waitForFunction(() => document.querySelector("#zoom img").complete);
const zoomed = await fresh.page.evaluate(() => {
  const dialog = document.getElementById("zoom");
  dialog.scrollLeft = 450;
  return { width: dialog.querySelector("img").clientWidth, scrolled: dialog.scrollLeft };
});
check(zoomed.width >= 1200 && zoomed.scrolled > 0, `it opens at full resolution and scrolls (${zoomed.width}px wide)`);
await fresh.page.waitForTimeout(200);
await fresh.page.screenshot({ path: `${out}phone_zoom.png` });
await fresh.page.locator("#zoom").click();
check(!(await fresh.page.locator("#zoom").isVisible()), "tapping again closes it");

await page.goto(`${base}/`);
await page.screenshot({ path: `${out}home.png` });
await page.goto(`${base}/assembly/`);
await page.screenshot({ path: `${out}desktop_top.png` });
await page.goto(`${base}/assembly/hinge-joint-2/`);
await page.screenshot({ path: `${out}desktop_chapter.png` });

await browser.close();
for (const f of failures.filter((x) => x.startsWith("console") || x.startsWith("page error"))) console.log("FAIL", f);
console.log(failures.length ? `\n${failures.length} FAILED` : "\nPASS");
process.exit(failures.length ? 1 : 0);
