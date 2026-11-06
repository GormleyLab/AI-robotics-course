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

// Every step has a form, and every picture loaded.
await page.evaluate(() => { document.documentElement.style.scrollBehavior = "auto"; });
check(await page.locator("[data-review-slot]").count() === 35, "34 step forms and one overall form");
check(!(await page.locator("article h1").count()), "the guide's own title block is gone");
const images = page.locator("article img");
const pictures = await images.count();
for (let i = 0; i < pictures; i++) await images.nth(i).scrollIntoViewIfNeeded();
await page.waitForLoadState("networkidle");
const broken = await images.evaluateAll((all) => all.filter((i) => !i.complete || !i.naturalWidth).map((i) => i.src));
check(pictures === 57 && broken.length === 0, `all pictures load (${pictures}, broken ${broken.length})`);

const hrefs = await page.locator("article a").evaluateAll((all) => all.map((a) => a.getAttribute("href")));
const local = hrefs.filter((h) => !/^(https?:|#)/.test(h));
check(local.length === 0, `no link points at a file the site doesn't have (${local.join(", ")})`);
for (const h of hrefs.filter((x) => x.startsWith("#"))) {
  check(await page.locator(`[id="${h.slice(1)}"]`).count() === 1, `anchor ${h} exists`);
}

// Answer a mix of field types, with text that could break the file format.
const tricky = 'Bound hard -- see "photo" --> then eased <off>\nsecond line';
await page.fill('[data-key="reviewer.name"]', "Test TA");
await page.check('input[data-key="step3.status"][value="Worked, with changes"]');
await page.check('input[data-key="step3.bind"][value="Bind"]');
await page.check('input[data-key="step3.fix"][value="Part design"]');
await page.check('input[data-key="step3.fix"][value="Picture"]');
await page.fill('[data-key="step3.notes"]', tricky);
await page.fill('[data-key="step7.tries"]', "4");
await page.fill('[data-key="overall.hardest"]', "Step 7");
check((await page.textContent("#review-status")).includes("1 of 34"), "the bar counts reviewed steps");

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
check(text.includes("Part design, Picture") || text.includes("Picture, Part design"), "the file lists the ticks");
check(/Guide revision \w+/.test(text), "the file records the guide revision");
const comment = text.slice(text.lastIndexOf("<!-- review-data"));
check(comment.indexOf("-->") === comment.lastIndexOf("-->"), "reviewer text can't end the data comment early");

const fresh = await open({ width: 390, height: 844 });
await fresh.context.addInitScript(() => localStorage.setItem("spr-gate", "ok"));
await fresh.page.goto(`${base}/assembly/`);
check(await fresh.page.inputValue('[data-key="step3.notes"]') === "", "a new browser starts empty");
await fresh.page.setInputFiles("#review-file", file);
await fresh.page.waitForFunction(() => document.querySelector('[data-key="step3.notes"]').value !== "");
check(await fresh.page.inputValue('[data-key="step3.notes"]') === tricky, "restore brings back tricky text exactly");
check(await fresh.page.isChecked('input[data-key="step3.bind"][value="Bind"]'), "restore brings back choices");
await fresh.page.setInputFiles("#review-file", { name: "x.md", mimeType: "text/markdown", buffer: Buffer.from("not ours") });
await fresh.page.waitForFunction(() => document.getElementById("review-status").textContent.includes("isn't a review file"));
check(await fresh.page.inputValue('[data-key="step3.notes"]') === tricky, "a wrong file changes nothing");

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

await browser.close();
for (const f of failures.filter((x) => x.startsWith("console") || x.startsWith("page error"))) console.log("FAIL", f);
console.log(failures.length ? `\n${failures.length} FAILED` : "\nPASS");
process.exit(failures.length ? 1 : 0);
