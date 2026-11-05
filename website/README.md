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

The page is `CAD/docs/assembly-guide.md` itself, read at build time by
`src/pages/assembly/index.astro`. There is no second copy: edit the Markdown and rebuild.
`src/lib/rehype-guide.mjs` adapts it for the site.

## The TA review

- **Questions:** `src/data/review-questions.json`, one list per step. Every step also gets
  the standard questions in `src/lib/review.ts`. The build fails if the guide's steps and
  this file disagree.
- **Answers:** saved in the reviewer's browser (`src/scripts/review.ts`). The site has no
  server, so nothing is sent anywhere. **Download my answers** makes one Markdown file to
  send to Dr. Gormley, and **Restore** loads that file on another device.
- **Keep returned files out of this repo.** It's public, and the files hold the reviewer's name.
- **Students:** remove `addReviewSlots` from the plugin, the script and review boxes from
  the guide page, and the draft labels.

The password gate in `src/layouts/Base.astro` only turns away passers-by: its password is in
this public repo.

## Hosting

GitHub Pages, at https://gormleylab.github.io/AI-robotics-course/. A push to `main` that
touches the site or the guide deploys it through `.github/workflows/site.yml`. The site sits
under the repo's name, so build internal URLs from `import.meta.env.BASE_URL`, never a bare `/...`.
