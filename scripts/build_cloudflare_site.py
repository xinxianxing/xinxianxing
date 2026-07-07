"""Build the public 信先行 static site from docs/.

The public build includes reader-facing pages, published posts, feeds, review
preview drafts for webhook links, and minimal assets. Project-maintenance docs
stay private.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from pathlib import Path

import markdown

from src.services.tutorials import (
    TUTORIAL_CATEGORIES,
    Tutorial,
    load_access_codes,
    load_tutorials,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DIST = ROOT / "dist"
TUTORIALS_PUBLISHED = ROOT / "data/tutorials/published"
TUTORIAL_CODES = ROOT / "data/tutorials/codes.json"

SITE_TITLE = "信先行"
SITE_DESCRIPTION = "AI教程、AI变现与效率技巧行动卡片"
SITE_URL = "https://xinxianxing.com"

MARKDOWN_EXTENSIONS = [
    "extra",
    "toc",
    "sane_lists",
]

PAGE_FILES = [
    "index.md",
]

ASSET_FILES = [
    (DOCS / "assets/css/xinxianxing.css", DIST / "assets/css/site.css"),
    (DOCS / "assets/js/xinxianxing.js", DIST / "assets/js/site.js"),
]

BRAND_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 420" role="img" aria-labelledby="title desc">
  <title id="title">信先行</title>
  <desc id="desc">日出、山线与信先行品牌字样</desc>
  <defs>
    <linearGradient id="sky" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#26265f"/>
      <stop offset="40%" stop-color="#a83162"/>
      <stop offset="72%" stop-color="#e46b35"/>
      <stop offset="100%" stop-color="#f2bd4b"/>
    </linearGradient>
    <radialGradient id="sun" cx="50%" cy="45%" r="45%">
      <stop offset="0%" stop-color="#fff7d6"/>
      <stop offset="55%" stop-color="#f8cf62"/>
      <stop offset="100%" stop-color="#e46b35" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="word" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#fffaf0"/>
      <stop offset="100%" stop-color="#ffd69b"/>
    </linearGradient>
  </defs>
  <rect width="900" height="420" rx="32" fill="url(#sky)"/>
  <circle cx="450" cy="178" r="118" fill="url(#sun)" opacity="0.95"/>
  <path d="M0 288 C140 246 236 267 338 238 C454 205 558 271 660 241 C762 210 826 240 900 224 L900 420 L0 420 Z" fill="#2f236c" opacity="0.82"/>
  <path d="M0 338 C130 306 250 330 372 298 C506 262 598 326 724 292 C804 270 850 284 900 276 L900 420 L0 420 Z" fill="#1f1b46" opacity="0.92"/>
  <g opacity="0.16" stroke="#fff9e9" stroke-width="1.2">
    <path d="M60 276 H840"/>
    <path d="M100 308 H800"/>
    <path d="M140 334 H760"/>
    <path d="M190 354 H710"/>
  </g>
  <text x="50%" y="46%" dominant-baseline="middle" text-anchor="middle" font-family="PingFang SC, Microsoft YaHei, sans-serif" font-size="96" font-weight="900" fill="url(#word)">信先行</text>
  <text x="50%" y="64%" dominant-baseline="middle" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="700" fill="#ffe7b5" letter-spacing="6">XINXIANXING</text>
</svg>
"""


@dataclass(frozen=True)
class Page:
    source: Path
    title: str
    body: str
    permalink: str
    lang: str | None = None
    published_at: date | None = None


def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    posts = load_posts()
    draft_previews = load_draft_previews()
    tutorials = load_tutorials(TUTORIALS_PUBLISHED)
    tutorial_codes = load_access_codes(TUTORIAL_CODES)
    render_pages(posts)
    render_posts(posts)
    render_draft_previews(draft_previews)
    render_tutorials(tutorials, tutorial_codes)
    write_feeds(posts)
    copy_assets()
    write_redirects()
    write_404()

    print(f"Built {DIST}")


def load_posts() -> list[Page]:
    posts: list[Page] = []
    for path in sorted((DOCS / "_posts").glob("*.md"), reverse=True):
        front, body = split_front_matter(path.read_text(encoding="utf-8"))
        post_date = parse_date(front.get("date")) or date_from_filename(path)
        lang = front.get("lang", "")
        raw_title = front.get("title") or title_from_markdown(body) or path.stem
        title = public_post_title(raw_title, post_date, lang)
        slug = path.stem
        if post_date and slug.startswith(post_date.isoformat()):
            slug = slug[len(post_date.isoformat()) + 1 :]
        permalink = (
            f"/{post_date:%Y/%m/%d}/{slug}.html"
            if post_date
            else f"/posts/{path.with_suffix('').name}.html"
        )
        posts.append(
            Page(
                source=path,
                title=title,
                body=body,
                permalink=permalink,
                lang=lang,
                published_at=post_date,
            )
        )
    posts.sort(key=lambda page: page.published_at or date.min, reverse=True)
    return posts


def load_draft_previews() -> list[Page]:
    drafts: list[Page] = []
    for path in sorted((DOCS / "drafts").glob("*.md"), reverse=True):
        front, body = split_front_matter(path.read_text(encoding="utf-8"))
        draft_date = parse_date(front.get("date")) or date_from_filename(path)
        lang = front.get("lang", "")
        raw_title = front.get("title") or title_from_markdown(body) or path.stem
        title = public_post_title(raw_title, draft_date, lang)
        drafts.append(
            Page(
                source=path,
                title=title,
                body=body,
                permalink=f"/drafts/{path.with_suffix('').name}.html",
                lang=lang,
                published_at=draft_date,
            )
        )
    return drafts


def public_post_title(title: str, post_date: date | None, lang: str | None) -> str:
    if post_date and re.search(r"\bsummary\b|Action Cards", title, re.IGNORECASE):
        if lang == "en":
            return f"{post_date.isoformat()} AI Picks"
        return f"{post_date.isoformat()} AI精选"
    return title.strip()


def render_pages(posts: list[Page]) -> None:
    for name in PAGE_FILES:
        path = DOCS / name
        if not path.exists():
            continue
        front, body = split_front_matter(path.read_text(encoding="utf-8"))
        title = front.get("title") or title_from_markdown(body) or path.stem
        if name == "index.md":
            body = render_index_content(body, posts)
            permalink = "/index.html"
            html_body = clean_raw_html(body)
        else:
            permalink = f"/{path.stem}/index.html"
            html_body = markdown_to_html(body)
        write_page(permalink, title, html_body)
        if name != "index.md":
            write_page(f"/{path.stem}.html", title, html_body)


def render_posts(posts: list[Page]) -> None:
    for post in posts:
        html_body = markdown_to_html(post.body)
        write_page(post.permalink, post.title, html_body)


def render_draft_previews(drafts: list[Page]) -> None:
    for draft in drafts:
        html_body = markdown_to_html(draft.body)
        write_page(draft.permalink, draft.title, html_body)


def render_tutorials(tutorials: list[Tutorial], codes: list[str]) -> None:
    list_body = build_tutorial_list_page(tutorials)
    write_page("/tutorials/index.html", "教程库", list_body)
    write_page("/tutorials.html", "教程库", list_body)

    categories_body = build_tutorial_categories_page(tutorials)
    write_page("/tutorials/categories/index.html", "教程分类", categories_body)
    write_page("/tutorials/categories.html", "教程分类", categories_body)

    for tutorial in tutorials:
        detail_body = build_tutorial_detail_page(tutorial, codes)
        write_page(f"/tutorials/{tutorial.slug}/index.html", tutorial.title, detail_body)
        write_page(f"/tutorials/{tutorial.slug}.html", tutorial.title, detail_body)


def build_tutorial_list_page(tutorials: list[Tutorial]) -> str:
    cards = build_tutorial_cards(tutorials)
    category_links = "\n".join(
        f'<a href="/tutorials/categories/#{html.escape(category, quote=True)}">{html.escape(category)}</a>'
        for category in TUTORIAL_CATEGORIES
    )
    return f"""<section class="tutorial-intro">
  <p>人工精选的深度教程，优先收录能直接上手的 AI 自动化、AI变现和效率技巧。</p>
  <div class="tutorial-category-links">
    {category_links}
  </div>
</section>
{cards}
"""


def build_tutorial_categories_page(tutorials: list[Tutorial]) -> str:
    buttons = [
        '<button class="tutorial-filter-button active" type="button" data-category="all">全部</button>'
    ]
    buttons.extend(
        f'<button class="tutorial-filter-button" type="button" data-category="{html.escape(category, quote=True)}">{html.escape(category)}</button>'
        for category in TUTORIAL_CATEGORIES
    )
    cards = build_tutorial_cards(tutorials, show_empty_category=True)
    return f"""<section class="tutorial-intro">
  <p>按分类快速筛选教程。这里只展示已经手动发布到教程库的内容。</p>
  <div class="tutorial-filter-bar" aria-label="教程分类筛选">
    {''.join(buttons)}
  </div>
</section>
{cards}
"""


def build_tutorial_cards(tutorials: list[Tutorial], show_empty_category: bool = False) -> str:
    if not tutorials:
        return '<p class="empty-state">暂无已发布教程。</p>'

    cards = []
    for tutorial in tutorials:
        status = "会员" if tutorial.is_member_only else "免费"
        status_class = "member" if tutorial.is_member_only else "free"
        category = html.escape(tutorial.category, quote=True)
        cards.append(
            f"""<article class="tutorial-card" data-category="{category}">
  <a href="{tutorial_permalink(tutorial)}">
    <div class="tutorial-card-meta">
      <span class="tutorial-category">{html.escape(tutorial.category)}</span>
      <span class="tutorial-status {status_class}">{status}</span>
    </div>
    <h2>{html.escape(tutorial.title)}</h2>
    <p>{html.escape(tutorial.summary or "暂无简介")}</p>
    <span class="tutorial-card-audience">{html.escape(tutorial.audience or "适用场景待补充")}</span>
  </a>
</article>"""
        )

    empty = (
        '<p class="empty-state tutorial-filter-empty" hidden>这个分类暂时没有已发布教程。</p>'
        if show_empty_category
        else ""
    )
    return '<section class="tutorial-card-grid">\n' + "\n".join(cards) + f"\n</section>{empty}"


def build_tutorial_detail_page(tutorial: Tutorial, codes: list[str]) -> str:
    locked = tutorial.is_member_only
    lock_class = " is-locked" if locked else ""
    lock_box = build_tutorial_lock_box(codes) if locked else ""
    source = build_tutorial_source_link(tutorial)
    member_status = "会员内容" if tutorial.is_member_only else "免费教程"
    updated = tutorial.updated_at or "未标注"
    return f"""<section class="tutorial-detail-head">
  <div class="tutorial-card-meta">
    <span class="tutorial-category">{html.escape(tutorial.category)}</span>
    <span class="tutorial-status {'member' if tutorial.is_member_only else 'free'}">{member_status}</span>
  </div>
  <p class="tutorial-detail-summary">{html.escape(tutorial.summary or "暂无简介")}</p>
  <dl class="tutorial-free-meta">
    <div>
      <dt>适合谁/适用场景</dt>
      <dd>{html.escape(tutorial.audience or "未填写")}</dd>
    </div>
    <div>
      <dt>原帖链接</dt>
      <dd>{source}</dd>
    </div>
    <div>
      <dt>更新时间</dt>
      <dd>{html.escape(updated)}</dd>
    </div>
  </dl>
</section>
{lock_box}
<section class="tutorial-member-content{lock_class}" data-tutorial-member-content>
  {render_tutorial_field("原帖核心观点", tutorial.source_summary)}
  {render_tutorial_field("中文步骤拆解", tutorial.steps)}
  {render_tutorial_field("使用工具", tutorial.tools)}
  {render_tutorial_field("可复制Prompt", tutorial.prompt_template, as_prompt=True)}
  {render_tutorial_field("实操案例/实测结果", tutorial.case_result)}
  {render_tutorial_field("国内可替代方案", tutorial.alternatives)}
  {render_tutorial_field("成本与预计效果", tutorial.cost_and_effect)}
  {render_tutorial_field("风险和注意事项", tutorial.risk_notice)}
</section>
"""


def build_tutorial_lock_box(codes: list[str]) -> str:
    payload = json.dumps({"codes": codes}, ensure_ascii=False).replace("</", "<\\/")
    return f"""<section class="tutorial-lock" data-tutorial-lock>
  <h2>输入授权码解锁</h2>
  <p>会员内容包含步骤拆解、工具清单、Prompt 模板、成本效果和风险提示。</p>
  <form class="tutorial-unlock-form">
    <input type="password" name="code" autocomplete="off" placeholder="输入授权码" aria-label="授权码">
    <button type="submit">解锁</button>
  </form>
  <p class="tutorial-unlock-message" aria-live="polite"></p>
  <script type="application/json" id="tutorial-access-codes">{payload}</script>
</section>"""


def build_tutorial_source_link(tutorial: Tutorial) -> str:
    author = tutorial.source_author or "原帖"
    if not tutorial.source_url:
        return html.escape(author)
    return (
        f'<a href="{html.escape(tutorial.source_url, quote=True)}" '
        f'target="_blank" rel="noopener noreferrer">{html.escape(author)}</a>'
    )


def render_tutorial_field(label: str, value: str, as_prompt: bool = False) -> str:
    content = value.strip() if value else "未填写"
    if as_prompt:
        body = f'<pre class="tutorial-prompt"><code>{html.escape(content)}</code></pre>'
    else:
        body = markdown_to_html(content)
    return f"""<article class="tutorial-field">
  <h2>{html.escape(label)}</h2>
  {body}
</article>"""


def tutorial_permalink(tutorial: Tutorial) -> str:
    return f"/tutorials/{tutorial.slug}/"


def render_index_content(body: str, posts: list[Page]) -> str:
    zh_posts = [post for post in posts if post.lang == "zh"]
    en_posts = [post for post in posts if post.lang == "en"]
    body = replace_issue_grid(body, "zh", zh_posts)
    body = replace_issue_grid(body, "en", en_posts)
    return replace_relative_url(body)


def clean_raw_html(body: str) -> str:
    body = replace_relative_url(body)
    return re.sub(r'\s+markdown="1"', "", body)


def replace_issue_grid(body: str, lang: str, posts: list[Page]) -> str:
    marker = f'<div class="issue-grid" data-post-list="{lang}"></div>'
    return body.replace(marker, build_issue_grid(posts, lang))


def build_issue_grid(posts: list[Page], lang: str) -> str:
    if not posts:
        empty = "暂无已发布内容。" if lang == "zh" else "No reviewed issues yet."
        return f'<div class="issue-grid"><p class="empty-state">{empty}</p></div>'

    cards = []
    for post in posts[:12]:
        date_label = post.published_at.isoformat() if post.published_at else "LATEST"
        preview_items = extract_item_titles(post.body, limit=4)
        if preview_items:
            preview = "<ul class=\"issue-preview\">" + "".join(
                f"<li>{html.escape(item)}</li>" for item in preview_items
            ) + "</ul>"
        else:
            fallback = "查看本期精选内容" if lang == "zh" else "Open this issue"
            preview = f'<p class="issue-preview-text">{fallback}</p>'
        label = "中文精选" if lang == "zh" else "English Picks"
        cards.append(
            f"""<article class="issue-card">
  <a href="{post.permalink}">
    <span class="issue-meta">{html.escape(label)} · {html.escape(date_label)}</span>
    <h3>{html.escape(post.title)}</h3>
    {preview}
  </a>
</article>"""
        )
    return '<div class="issue-grid">\n' + "\n".join(cards) + "\n</div>"


def extract_item_titles(body: str, limit: int) -> list[str]:
    titles: list[str] = []
    pattern = re.compile(r"^\d+\.\s+\[([^\]]+)\]\(#item-\d+\)", re.MULTILINE)
    for match in pattern.finditer(body):
        titles.append(match.group(1).strip())
        if len(titles) >= limit:
            break
    return titles


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + len("\n---\n") :]
    front: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        front[key.strip()] = value.strip().strip("\"'")
    return front, body


def markdown_to_html(body: str) -> str:
    body = replace_relative_url(body)
    body = render_markdown_sections(body)
    return markdown.markdown(body, extensions=MARKDOWN_EXTENSIONS, output_format="html5")


def replace_relative_url(body: str) -> str:
    return re.sub(
        r"\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}",
        lambda match: match.group(1),
        body,
    )


def render_markdown_sections(body: str) -> str:
    pattern = re.compile(
        r'(<section\b[^>]*\bmarkdown="1"[^>]*>)(.*?)(</section>)',
        re.DOTALL,
    )

    def repl(match: re.Match[str]) -> str:
        opening = re.sub(r'\s+markdown="1"', "", match.group(1))
        inner = markdown.markdown(
            match.group(2).strip(),
            extensions=MARKDOWN_EXTENSIONS,
            output_format="html5",
        )
        return f"{opening}\n{inner}\n{match.group(3)}"

    return pattern.sub(repl, body)


def write_page(permalink: str, title: str, body_html: str) -> None:
    output = DIST / permalink.strip("/")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(layout(title, body_html, permalink), encoding="utf-8")


def layout(title: str, body_html: str, permalink: str) -> str:
    is_home = permalink == "/index.html"
    is_draft = permalink.startswith("/drafts/")
    is_tutorial = permalink.startswith("/tutorials")
    canonical = absolute_url(permalink)
    if is_home:
        canonical = SITE_URL
    escaped_title = html.escape(title)
    body_class = "home-page" if is_home else "article-page"
    if is_draft:
        body_class += " draft-preview-page"
    if is_tutorial:
        body_class += " tutorial-page"
    robots_meta = '  <meta name="robots" content="noindex,nofollow">\n' if is_draft else ""
    article_header = ""
    if not is_home:
        if is_tutorial:
            eyebrow = "教程库"
        else:
            eyebrow = "待审核草稿" if is_draft else "已发布精选"
        article_header = f"""    <header class="article-title">
      <p class="eyebrow">{eyebrow}</p>
      <h1>{escaped_title}</h1>
    </header>
"""
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escaped_title} · {SITE_TITLE}</title>
  <meta name="description" content="{html.escape(SITE_DESCRIPTION)}">
  <meta property="og:title" content="{escaped_title} · {SITE_TITLE}">
  <meta property="og:description" content="{html.escape(SITE_DESCRIPTION)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{absolute_url('/assets/brand-sunrise.svg')}">
{robots_meta.rstrip()}
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="/assets/brand-sunrise.svg" type="image/svg+xml">
  <link rel="alternate" type="application/atom+xml" title="信先行 · 全部精选" href="/feed.xml">
  <link rel="alternate" type="application/atom+xml" title="信先行 · 中文精选" href="/feed-zh.xml">
  <link rel="alternate" type="application/atom+xml" title="Xinxianxing · English Picks" href="/feed-en.xml">
  <link rel="stylesheet" href="/assets/css/site.css">
  <script src="/assets/js/site.js" defer></script>
</head>
<body class="{body_class}">
  <header class="site-header">
    <a class="site-brand" href="/" aria-label="信先行首页">
      <span class="site-brand-mark">信</span>
      <span>信先行</span>
    </a>
    <div class="site-actions">
      <a class="site-feed-link" href="/tutorials/">教程库</a>
      <a class="site-feed-link" href="/feed-zh.xml">RSS</a>
    </div>
  </header>
  <main class="main-content">
{article_header}{body_html}
  </main>
  <footer class="site-footer">
    <p>信先行 · AI教程 / AI变现 / 效率技巧</p>
  </footer>
</body>
</html>
"""


def absolute_url(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return SITE_URL.rstrip("/") + "/" + path.strip("/")


def write_feeds(posts: list[Page]) -> None:
    write_atom_feed("feed.xml", posts, "信先行 · 全部精选")
    write_atom_feed("feed-zh.xml", [post for post in posts if post.lang == "zh"], "信先行 · 中文精选")
    write_atom_feed("feed-en.xml", [post for post in posts if post.lang == "en"], "Xinxianxing · English Picks")


def write_atom_feed(filename: str, posts: list[Page], title: str) -> None:
    output = DIST / filename
    output.parent.mkdir(parents=True, exist_ok=True)
    updated = atom_datetime(posts[0].published_at if posts else date.today())
    entries = []
    for post in posts[:20]:
        url = absolute_url(post.permalink)
        content_html = markdown_to_html(post.body)
        entries.append(
            f"""  <entry>
    <title>{html.escape(post.title)}</title>
    <link href="{html.escape(url, quote=True)}"/>
    <updated>{atom_datetime(post.published_at)}</updated>
    <id>{html.escape(url)}</id>
    <content type="html"><![CDATA[{cdata(content_html)}]]></content>
  </entry>"""
        )
    output.write_text(
        f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>{html.escape(title)}</title>
  <link href="{html.escape(absolute_url('/' + filename), quote=True)}" rel="self"/>
  <link href="{html.escape(SITE_URL, quote=True)}"/>
  <updated>{updated}</updated>
  <id>{html.escape(absolute_url('/'))}</id>
{chr(10).join(entries)}
</feed>
""",
        encoding="utf-8",
    )


def atom_datetime(value: date | None) -> str:
    dt = datetime.combine(value or date.today(), time.min, tzinfo=timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")


def cdata(value: str) -> str:
    return value.replace("]]>", "]]]]><![CDATA[>")


def copy_assets() -> None:
    for source, target in ASSET_FILES:
        if not source.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    write_brand_asset()


def write_brand_asset() -> None:
    target = DIST / "assets/brand-sunrise.svg"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(BRAND_SVG, encoding="utf-8")


def write_redirects() -> None:
    (DIST / "_redirects").write_text(
        "/xinxianxing/* /:splat 301\n"
        "/xinxianxing / 301\n",
        encoding="utf-8",
    )


def write_404() -> None:
    body = markdown.markdown(
        "# 页面未找到\n\n你可以回到 [信先行首页](/) 查看已发布的行动卡片。",
        extensions=MARKDOWN_EXTENSIONS,
    )
    write_page("/404.html", "页面未找到", body)


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def date_from_filename(path: Path) -> date | None:
    match = re.match(r"(\d{4}-\d{2}-\d{2})-", path.name)
    return parse_date(match.group(1)) if match else None


def title_from_markdown(body: str) -> str | None:
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return match.group(1).strip() if match else None


if __name__ == "__main__":
    main()
