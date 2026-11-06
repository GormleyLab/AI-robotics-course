import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import { execSync } from "node:child_process";
import rehypeGuide from "./src/lib/rehype-guide.mjs";

// Which revision of the guide the reviewer read, recorded in their feedback
// file, because step numbers can move between revisions.
function revision() {
  try {
    return execSync("git rev-parse --short HEAD", { encoding: "utf8" }).trim();
  } catch {
    return "unknown";
  }
}

// Static site. The guide is CAD/docs/assembly-*.md, read from outside this folder, so
// each page has one source (see src/lib/rehype-guide.mjs).
// Hosted on GitHub Pages under the repo's name: build every internal URL from
// import.meta.env.BASE_URL, never a bare "/...".
export default defineConfig({
  output: "static",
  site: "https://gormleylab.github.io",
  base: "/AI-robotics-course/",
  markdown: { rehypePlugins: [rehypeGuide] },
  vite: {
    plugins: [tailwindcss()],
    define: { __GUIDE_REVISION__: JSON.stringify(revision()) },
    server: { fs: { allow: [".."] } },
  },
});
