"""Build the BIGGER! dev blog: posts/*.md -> docs/ (plain static HTML for GitHub Pages).

    python build.py                 # build docs/ with the theme in site.json
    python build.py --theme callsheet --out _look/callsheet   # a look-first render
    python build.py --publish       # refuse if any post still has a ::: todo block

Posts are Markdown with a small front matter block and a few magazine blocks:

    ::: box | The toolkit         an aside card (Markdown inside)
    ::: pull | Duncan, Thu 1:15 AM    a pull quote (Markdown inside)
    ::: pair                      two images side by side
    ::: wide                      content wider than the text column
    ::: numbers | By the numbers  lines of `value | label`
    ::: timeline | Title          lines of `when | title | note`
    ::: todo                      a writer's note; drafts only (--publish refuses it)
    :::                           closes the block

The front page's words live in home.md: kicker, headline, tagline and footer in its front
matter (one line each, Markdown allowed: *italics*, [links](https://...)), and the intro as
its body. The footer shows on every page.

An image alone on a line becomes a figure, its title the caption:
    ![alt text](media/file.jpg "Caption.")
A .mp4 source becomes a silent looping video.
Needs: pip install markdown
"""
import argparse
import html
import json
import math
import re
import shutil
import sys
from pathlib import Path
from string import Template

import markdown

ROOT = Path(__file__).resolve().parent
BLOCK_OPEN = re.compile(r"^:::\s*(\w+)\s*(?:\|\s*(.*))?$")


def read_post(path):
    text = path.read_text(encoding="utf-8")
    meta = {}
    if text.startswith("---"):
        head, text = text[3:].split("\n---", 1)
        for line in head.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    meta.setdefault("slug", path.stem)
    meta["order"] = int(meta.get("order", 99))
    return meta, text.lstrip("\n")


def rows(lines):
    return [[c.strip() for c in ln.split("|")] for ln in lines if ln.strip()]


def render_block(kind, arg, lines, todos):
    body = "\n".join(lines)
    arg = (arg or "").strip()
    if kind == "box":
        title = f'<p class="box-title">{html.escape(arg)}</p>\n\n' if arg else ""
        return f'<aside class="box" markdown="1">\n{title}{body}\n\n</aside>'
    if kind == "pull":
        cite = f"\n<cite>{html.escape(arg)}</cite>" if arg else ""
        return f'<blockquote class="pull" markdown="1">\n\n{body}\n{cite}\n</blockquote>'
    if kind in ("pair", "wide"):
        # One image per paragraph, so each becomes its own figure.
        body = "\n\n".join(ln for ln in lines if ln.strip())
        return f'<div class="{kind}" markdown="1">\n\n{body}\n\n</div>'
    if kind == "todo":
        todos.append(body[:60])
        return f'<div class="todo" markdown="1">\n<p class="todo-label">You write</p>\n\n{body}\n\n</div>'
    if kind == "numbers":
        cells = "".join(
            f'<div class="num"><span class="num-v">{html.escape(r[0])}</span>'
            f'<span class="num-l">{html.escape(r[1] if len(r) > 1 else "")}</span></div>'
            for r in rows(lines))
        title = f'<p class="box-title">{html.escape(arg)}</p>' if arg else ""
        return f'<aside class="box numbers">{title}<div class="num-grid">{cells}</div></aside>'
    if kind == "timeline":
        items = "".join(
            f'<li><span class="tl-when">{html.escape(r[0])}</span>'
            f'<span class="tl-what">{html.escape(r[1] if len(r) > 1 else "")}</span>'
            f'<span class="tl-note">{html.escape(r[2] if len(r) > 2 else "")}</span></li>'
            for r in rows(lines))
        title = f'<p class="box-title">{html.escape(arg)}</p>' if arg else ""
        return f'<aside class="box timeline">{title}<ol>{items}</ol></aside>'
    raise SystemExit(f"Unknown block ::: {kind}")


def preprocess(text, todos):
    out, i, lines = [], 0, text.splitlines()
    while i < len(lines):
        m = BLOCK_OPEN.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        kind, arg, inner = m.group(1), m.group(2), []
        i += 1
        while i < len(lines) and lines[i].strip() != ":::":
            inner.append(lines[i])
            i += 1
        i += 1  # the closing :::
        out += ["", render_block(kind, arg, inner, todos), ""]
    return "\n".join(out)


ATTR = re.compile(r'(\w+)="([^"]*)"')


def figure(match):
    attrs = dict(ATTR.findall(match.group(1)))
    src, alt = attrs.get("src", ""), attrs.get("alt", "")
    cap, cls = attrs.get("title", ""), attrs.get("class", "")
    caption = f"<figcaption>{cap}</figcaption>" if cap else ""
    if src.lower().endswith(".mp4"):
        media = (f'<video src="{src}" autoplay muted loop playsinline preload="metadata" '
                 f'aria-label="{alt}"></video>')
    else:
        media = f'<img src="{src}" alt="{alt}" loading="lazy">'
    return f'<figure class="{cls}">{media}{caption}</figure>'


def to_html(text, todos):
    md = markdown.Markdown(extensions=["extra", "smarty", "sane_lists"])
    body = md.convert(preprocess(text, todos))
    return re.sub(r"<p>\s*<img ([^>]*?)\s*/?>\s*</p>", figure, body)


def inline(s):
    """One line of Markdown (smart quotes, *italics*, links), without the <p>."""
    out = markdown.markdown(s, extensions=["smarty"]).strip()
    return re.sub(r"^<p>|</p>$", "", out)


def words(text):
    text = re.sub(r"^:::.*$", "", text, flags=re.M)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    return len(re.findall(r"[A-Za-z0-9'’]+", text))


def rebase(markup, root):
    return re.sub(r'(src|href)="(media|static)/', rf'\1="{root}\2/', markup)


def build(theme, out, publish):
    site = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
    theme = theme or site["theme"]
    tpl_post = Template((ROOT / "templates" / "post.html").read_text(encoding="utf-8"))
    tpl_index = Template((ROOT / "templates" / "index.html").read_text(encoding="utf-8"))

    posts = []
    for path in sorted((ROOT / "posts").glob("*.md")):
        meta, text = read_post(path)
        todos = []
        meta["body"] = to_html(text, todos)
        meta["todos"] = todos
        meta["minutes"] = max(1, math.ceil(words(text) / 225))
        posts.append(meta)
    posts.sort(key=lambda p: p["order"])

    home, home_text = read_post(ROOT / "home.md")
    home_todos = []
    intro = to_html(home_text, home_todos)

    left = [(p["slug"], len(p["todos"])) for p in posts if p["todos"]]
    if home_todos:
        left.append(("home", len(home_todos)))
    if publish and left:
        sys.exit(f"Refusing to publish: writer's notes left in {left}")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(ROOT / "static", out / "static")
    if (ROOT / "media").exists():
        shutil.copytree(ROOT / "media", out / "media")
    (out / ".nojekyll").write_text("", encoding="utf-8")

    common = dict(site_title=site["title"], theme=theme, author=site["author"],
                  footer=inline(home.get("footer", "")), base_url=site["base_url"])
    for n, p in enumerate(posts):
        root = "../"
        prev_link = next_link = ""
        if n > 0:
            q = posts[n - 1]
            prev_link = f'<a class="pn prev" href="../{q["slug"]}/"><span>Previous</span>{html.escape(q["title"])}</a>'
        if n + 1 < len(posts):
            q = posts[n + 1]
            next_link = f'<a class="pn next" href="../{q["slug"]}/"><span>Next</span>{html.escape(q["title"])}</a>'
        hero = ""
        if p.get("hero"):
            hero = (f'<figure class="hero"><img src="media/{p["hero"]}" alt="{html.escape(p.get("hero_alt", ""))}">'
                    f'<figcaption>{p.get("hero_caption", "")}</figcaption></figure>')
        page = tpl_post.substitute(
            common, root=root, title=html.escape(p["title"]),
            kicker=html.escape(p.get("kicker", "")), standfirst=p.get("standfirst", ""),
            dateline=html.escape(p.get("dateline", "")), minutes=p["minutes"],
            hero=rebase(hero, root), body=rebase(p["body"], root),
            prev=prev_link, next=next_link, slug=p["slug"],
            og_image=f'{site["base_url"]}media/{p.get("hero", "")}',
            description=html.escape(re.sub("<[^>]+>", "", p.get("standfirst", ""))))
        (out / p["slug"]).mkdir()
        (out / p["slug"] / "index.html").write_text(page, encoding="utf-8")

    cards = "".join(
        f'<a class="card" href="{p["slug"]}/">'
        + (f'<img src="media/{p["hero"]}" alt="" loading="lazy">' if p.get("hero") else "")
        + f'<span class="card-kicker">{html.escape(p.get("kicker", ""))}</span>'
        f'<span class="card-title">{html.escape(p["title"])}</span>'
        f'<span class="card-stand">{p.get("standfirst", "")}</span>'
        f'<span class="card-meta">{html.escape(p.get("dateline", ""))} · {p["minutes"]} min read</span></a>'
        for p in posts)
    (out / "index.html").write_text(
        tpl_index.substitute(
            common, root="", cards=cards, intro=intro,
            home_kicker=inline(home.get("kicker", "")), headline=inline(home.get("headline", site["title"])),
            tagline=inline(home.get("tagline", "")),
            description=re.sub("<[^>]+>", "", inline(home.get("tagline", "")))),
        encoding="utf-8")

    for slug, n in left:
        print(f"WARNING {slug}: {n} writer's note(s) left (::: todo)")
    print(f"BUILT {out} theme={theme} posts={len(posts)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme")
    ap.add_argument("--out", default="docs")
    ap.add_argument("--publish", action="store_true")
    a = ap.parse_args()
    build(a.theme, ROOT / a.out, a.publish)
