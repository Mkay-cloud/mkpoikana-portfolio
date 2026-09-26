#!/usr/bin/env python3
"""Build the blog from content/posts/*.md.

Run from the repo root:  python3 scripts/build_blog.py

It does three things:
1. Writes the article data into index.html (between the POSTS:START / POSTS:END markers).
2. Generates /blog/index.html and /blog/<slug>/index.html, copies of index.html with their own
   title, description, canonical URL, link-preview tags, structured data and a crawlable
   <noscript> copy of the article.
3. Rewrites sitemap.xml.
"""
import glob, html, json, math, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://mkpoikana.online"
AUTHOR = "Mkpoikana Otu"


def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        meta[k.strip()] = v
    blocks, para, items = [], [], []

    def flush():
        nonlocal para, items
        if para:
            blocks.append({"t": " ".join(para)}); para = []
        if items:
            blocks.append({"l": items}); items = []

    for line in m.group(2).splitlines():
        s = line.strip()
        if not s:
            flush()
        elif s.startswith("## "):
            flush(); blocks.append({"h": s[3:]})
        elif s.startswith("- "):
            if para:
                blocks.append({"t": " ".join(para)}); para = []
            items.append(s[2:])
        else:
            if items:
                blocks.append({"l": items}); items = []
            para.append(s)
    flush()
    words = len(re.findall(r"\S+", m.group(2)))
    meta["slug"] = os.path.splitext(os.path.basename(path))[0]
    meta["read"] = f"{max(1, math.ceil(words / 230))} MIN"
    meta["words"] = words
    meta["body"] = blocks
    return meta


def load_posts():
    posts = [parse(p) for p in glob.glob(os.path.join(ROOT, "content", "posts", "*.md"))]
    posts.sort(key=lambda p: p["iso"], reverse=True)
    for p in posts:
        for field in ("title", "excerpt"):
            if "—" in p[field] or "–" in p[field]:
                raise SystemExit(f"Dash found in {p['slug']} {field}")
        for b in p["body"]:
            text = json.dumps(b, ensure_ascii=False)
            if "—" in text or "–" in text:
                raise SystemExit(f"Dash found in {p['slug']}: {text[:80]}")
    return posts


def js_posts(posts):
    out = []
    for p in posts:
        out.append({
            "slug": p["slug"], "cat": p["cat"], "read": p["read"], "date": p["date"],
            "title": p["title"], "excerpt": p["excerpt"],
            "href": f"/blog/{p['slug']}",
            "img": f"/assets/blog/{p['slug']}.webp",
            "imgAlt": f"Illustration for the article: {p['title']}",
            "body": p["body"],
        })
    return json.dumps(out, ensure_ascii=False, indent=1)


def set_meta(doc, *, title, desc, url, image, image_alt, og_type):
    e = html.escape
    def sub(pattern, repl):
        nonlocal doc
        doc, n = re.subn(pattern, lambda _m: repl, doc, count=1)
        if n != 1:
            raise SystemExit(f"meta pattern not found: {pattern}")
    sub(r"<title>.*?</title>", f"<title>{e(title)}</title>")
    sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">')
    sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">')
    sub(r'<meta property="og:type" content="[^"]*">', f'<meta property="og:type" content="{og_type}">')
    sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{e(title)}">')
    sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{e(desc)}">')
    sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">')
    sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{image}">')
    sub(r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{e(image_alt)}">')
    sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{e(title)}">')
    sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{e(desc)}">')
    sub(r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{image}">')
    return doc


def noscript_article(p):
    e = html.escape
    parts = [f"<h1>{e(p['title'])}</h1>", f"<p>{e(p['excerpt'])}</p>"]
    for b in p["body"]:
        if "h" in b: parts.append(f"<h2>{e(b['h'])}</h2>")
        elif "t" in b: parts.append(f"<p>{e(b['t'])}</p>")
        elif "l" in b: parts.append("<ul>" + "".join(f"<li>{e(i)}</li>" for i in b["l"]) + "</ul>")
    parts.append(f'<p>By {AUTHOR}. <a href="/blog">More articles</a></p>')
    return "<noscript><article>" + "".join(parts) + "</article></noscript>"


def page(template, route, extra_head, body_prefix):
    doc = template.replace('<meta charset="utf-8">',
                           '<meta charset="utf-8">\n<script>window.__ROUTE=' + json.dumps(route) + ';</script>', 1)
    doc = doc.replace("</head>", extra_head + "\n</head>", 1)
    doc = doc.replace("<body>", "<body>\n" + body_prefix, 1)
    return doc


def main():
    posts = load_posts()
    idx_path = os.path.join(ROOT, "index.html")
    idx = open(idx_path, encoding="utf-8").read()
    new_idx, n = re.subn(r"/\*POSTS:START\*/.*?/\*POSTS:END\*/",
                         lambda _m: "/*POSTS:START*/" + js_posts(posts) + "/*POSTS:END*/", idx, flags=re.S)
    if n != 1:
        raise SystemExit("POSTS markers not found in index.html")
    open(idx_path, "w", encoding="utf-8").write(new_idx)

    # Blog index
    blog_desc = "Plain-language articles on web design, SEO and what actually brings in enquiries, by Mkpoikana Otu."
    doc = set_meta(new_idx, title="Blog | Mkpoikana Otu", desc=blog_desc, url=f"{SITE}/blog",
                   image=f"{SITE}/assets/og-image.png", image_alt="Mkpoikana Otu blog", og_type="website")
    items = "".join(f'<li><a href="/blog/{p["slug"]}">{html.escape(p["title"])}</a></li>' for p in posts)
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Mkpoikana Otu blog", "url": f"{SITE}/blog",
          "author": {"@type": "Person", "name": AUTHOR, "url": SITE}}
    doc = page(doc, {"page": "blog"},
               '<script type="application/ld+json">' + json.dumps(ld) + "</script>",
               f"<noscript><h1>Notes on design and search</h1><ul>{items}</ul></noscript>")
    os.makedirs(os.path.join(ROOT, "blog"), exist_ok=True)
    open(os.path.join(ROOT, "blog", "index.html"), "w", encoding="utf-8").write(doc)

    # Articles
    for i, p in enumerate(posts):
        url = f"{SITE}/blog/{p['slug']}"
        og = f"{SITE}/assets/blog/{p['slug']}-og.jpg"
        doc = set_meta(new_idx, title=f"{p['title']} | Mkpoikana Otu", desc=p["excerpt"], url=url,
                       image=og, image_alt=f"Illustration for the article: {p['title']}", og_type="article")
        ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
              "description": p["excerpt"], "image": og, "datePublished": p["iso"], "dateModified": p["iso"],
              "wordCount": p["words"], "articleSection": p["cat"].title(), "mainEntityOfPage": url,
              "author": {"@type": "Person", "name": AUTHOR, "url": SITE},
              "publisher": {"@type": "Person", "name": AUTHOR, "url": SITE}}
        crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog"},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]}
        head = (f'<meta property="article:published_time" content="{p["iso"]}">\n'
                f'<meta property="article:author" content="{AUTHOR}">\n'
                f'<link rel="preload" as="image" href="/assets/blog/{p["slug"]}.webp">\n'
                '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n"
                '<script type="application/ld+json">' + json.dumps(crumbs, ensure_ascii=False) + "</script>")
        doc = page(doc, {"page": "post", "postId": i}, head, noscript_article(p))
        d = os.path.join(ROOT, "blog", p["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)

    # Sitemap
    urls = [(f"{SITE}/", __import__("datetime").date.today().isoformat()), (f"{SITE}/blog", posts[0]["iso"])]
    urls += [(f"{SITE}/blog/{p['slug']}", p["iso"]) for p in posts]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{d}</lastmod>\n  </url>" for u, d in urls]
    sm.append("</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(sm))
    print(f"Built {len(posts)} articles:", ", ".join(f"{p['slug']} ({p['read']})" for p in posts))


if __name__ == "__main__":
    main()
