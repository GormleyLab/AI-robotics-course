# Course website

Astro static site for 14:125:444, on the same stack and look as the Principles of Drug
Delivery site. For now it hosts the assembly guide for TA review.

## Build and view

Needs Node 24 (`.node-version`).

```bash
cd website
npm install
npx astro build
npx astro preview --port 4321 --host 127.0.0.1   # http://127.0.0.1:4321/AI-robotics-course/
node qa/review_check.mjs                          # with preview running; uses installed Edge
```

## The assembly guide

The pages are the Markdown files themselves, read at build time, so there is no second copy:
edit the Markdown and rebuild. `CAD/docs/assembly-guide.md` is the overview
(`src/pages/assembly/index.astro`), and each chapter is its own `CAD/docs/assembly-<n>-*.md`
(`src/pages/assembly/[slug].astro`). `src/lib/chapters.mjs` lists the chapters: add a new
one there. `src/layouts/Guide.astro` is the shared page, and `src/lib/rehype-guide.mjs` adapts
the Markdown for the site.

## The TA review

- **Questions:** `src/data/review-questions.json`, one list per step. Every step also gets
  the standard questions in `src/lib/review.ts`. The build fails if the guide's steps and
  this file disagree.
- **Answers:** saved in the reviewer's browser (`src/scripts/review.ts`). The site has no
  server, so nothing is sent anywhere. **Download my answers** makes one Markdown file to
  send to Dr. Gormley, and **Restore** loads that file on another device. Each download holds
  everything so far, so TAs send one after every session and the newest replaces the rest.
  Restore replaces the browser's answers, so it asks first if the browser already has some.
- **Keep returned files out of this repo.** It's public, and the files hold the reviewer's name.
- **One store:** answers from every chapter save together, so one file covers the whole guide.
  The reviewer's details are on the overview page, and each chapter ends with its own overall
  review (`chapterOverall` and `overall` in the questions file).
- **Students:** remove `addReviewSlots` from the plugin, the script and review bar from
  `Guide.astro`, the review box from the overview page, and the draft labels.

The password gate in `src/layouts/Base.astro` only turns away passers-by: its password is in
this public repo.

## Hosting

GitHub Pages, at https://gormleylab.github.io/AI-robotics-course/. A push to `main` that
touches the site or the guide deploys it through `.github/workflows/site.yml`. The site sits
under the repo's name, so build internal URLs from `import.meta.env.BASE_URL`, never a bare `/...`.
