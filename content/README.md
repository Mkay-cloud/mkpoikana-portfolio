# Blog articles

Each article is one Markdown file in `content/posts/`. The file name becomes the web address
(`content/posts/click-to-call.md` → `https://mkpoikana.online/blog/click-to-call`).

Front matter at the top of each file: `title`, `cat` (SEO, WEB DESIGN, TECHNICAL SEO or PROCESS),
`date` (shown on the site, e.g. `SEP 2026`), `iso` (e.g. `2026-09-15`, used for sorting and Google),
and `excerpt`.

In the body: a blank line starts a new paragraph, `## ` starts a heading, `- ` makes a bullet point.
Em dashes and en dashes are not allowed; the build stops if it finds one.

Featured images live in `assets/blog/<slug>.webp` (1600x900) and `assets/blog/<slug>-og.jpg`
(1200x630, used for link previews). `scripts/blog_images.py` draws the current set.

After editing, run `python3 scripts/build_blog.py` and commit everything it changes.
