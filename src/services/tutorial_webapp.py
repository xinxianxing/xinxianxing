"""Local-only web form for adding tutorial drafts."""

from __future__ import annotations

import html
import asyncio
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from src.models import ContentItem
from src.services.manual_add import ManualAddError, fetch_url_as_item
from src.services.tutorials import (
    TUTORIAL_CATEGORIES,
    TUTORIAL_FIELD_LABELS,
    write_tutorial_draft,
)


ROOT = Path(__file__).resolve().parents[2]
DRAFTS_DIR = ROOT / "data/tutorials/drafts"
HOST = "127.0.0.1"
PORT = 8766
MAX_FORM_BYTES = 2 * 1024 * 1024

TEXT_FIELDS = [
    "title",
    "summary",
    "audience",
    "source_author",
    "source_url",
    "source_summary",
    "tools",
    "alternatives",
    "cost_and_effect",
    "updated_at",
]
LONG_TEXT_FIELDS = [
    "steps",
    "prompt_template",
    "case_result",
    "risk_notice",
]
REQUIRED_FIELDS = ["title", "summary", "category"]
IMPORTED_BODY_LIMIT = 12000


class TutorialWebAppHandler(BaseHTTPRequestHandler):
    """Small localhost-only handler for tutorial draft creation."""

    server_version = "XinxianxingTutorialWebApp/0.1"

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path not in {"/", "/tutorials/new"}:
            self.send_html(render_page(status_code=404, errors=["页面不存在。"]), status_code=404)
            return
        self.send_html(render_page(values=default_values()))

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path == "/import":
            self.handle_import_url()
            return
        if path != "/tutorials":
            self.send_html(render_page(status_code=404, errors=["页面不存在。"]), status_code=404)
            return

        try:
            params = self.read_form_params()
        except ValueError as exc:
            self.send_html(render_page(errors=[str(exc)], values=default_values()), status_code=400)
            return

        values = form_values(params)
        errors = validate_values(values)
        if errors:
            self.send_html(render_page(errors=errors, values=values), status_code=400)
            return

        path = write_tutorial_draft(values, DRAFTS_DIR)
        relative_path = path.relative_to(ROOT)
        self.send_html(render_page(success=f"已保存到 {relative_path}", values=default_values()))

    def handle_import_url(self) -> None:
        try:
            params = self.read_form_params()
        except ValueError as exc:
            self.send_html(render_page(errors=[str(exc)], values=default_values()), status_code=400)
            return

        url = first_value(params, "import_url").strip()
        if not url:
            self.send_html(render_page(errors=["请先粘贴一个文章链接。"], values=default_values()), status_code=400)
            return

        try:
            item = asyncio.run(fetch_url_as_item(url))
        except ManualAddError as exc:
            self.send_html(render_page(errors=[str(exc)], values=default_values(), import_url=url), status_code=400)
            return

        values = values_from_imported_item(item)
        self.send_html(
            render_page(
                success="已采集链接，标题、来源和正文已预填。请整理字段后保存为草稿。",
                values=values,
                import_url=url,
            )
        )

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")

    def read_form_params(self) -> dict[str, list[str]]:
        length = int(self.headers.get("Content-Length") or "0")
        if length > MAX_FORM_BYTES:
            raise ValueError("表单内容太大，请拆成更短的教程草稿。")
        body = self.rfile.read(length).decode("utf-8", errors="replace")
        return parse_qs(body, keep_blank_values=True)

    def send_html(self, body: str, status_code: int = 200) -> None:
        payload = body.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), TutorialWebAppHandler)
    print(f"信先行教程录入页已启动：http://{HOST}:{PORT}/")
    print("只监听 127.0.0.1，本机浏览器访问即可。按 Ctrl+C 退出。")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止教程录入页。")
    finally:
        server.server_close()


def default_values() -> dict[str, str | bool]:
    values: dict[str, str | bool] = {field: "" for field in TEXT_FIELDS + LONG_TEXT_FIELDS}
    values["category"] = TUTORIAL_CATEGORIES[0]
    values["is_member_only"] = True
    values["updated_at"] = date.today().isoformat()
    return values


def form_values(params: dict[str, list[str]]) -> dict[str, str | bool]:
    values = default_values()
    for field in TEXT_FIELDS + LONG_TEXT_FIELDS + ["category"]:
        values[field] = first_value(params, field).strip()
    values["is_member_only"] = "is_member_only" in params
    if not values["updated_at"]:
        values["updated_at"] = date.today().isoformat()
    return values


def first_value(params: dict[str, list[str]], field: str) -> str:
    values = params.get(field, [""])
    return values[0] if values else ""


def values_from_imported_item(item: ContentItem) -> dict[str, str | bool]:
    """Prefill tutorial fields from a fetched article."""

    values = default_values()
    body = truncate_imported_body(item.content)
    source_url = str(item.url)
    values.update(
        {
            "title": item.title,
            "summary": summarize_imported_body(body, item.title),
            "category": infer_category(item.title, body),
            "source_author": item.author or urlparse(source_url).netloc,
            "source_url": source_url,
            "source_summary": (
                "【自动采集原文，请改写为原帖核心观点】\n\n" + body
            ).strip(),
            "updated_at": item.published_at.date().isoformat()
            if item.published_at
            else date.today().isoformat(),
        }
    )
    return values


def truncate_imported_body(body: str) -> str:
    text = body.strip()
    if len(text) <= IMPORTED_BODY_LIMIT:
        return text
    return text[:IMPORTED_BODY_LIMIT].rstrip() + "\n\n【正文过长，已截断】"


def summarize_imported_body(body: str, fallback_title: str) -> str:
    for paragraph in body.splitlines():
        cleaned = " ".join(paragraph.split()).strip()
        if len(cleaned) < 12:
            continue
        sentence = cleaned
        for marker in ("。", "！", "？", ".", "!", "?"):
            if marker in sentence:
                sentence = sentence.split(marker, 1)[0] + marker
                break
        if len(sentence) > 90:
            sentence = sentence[:88].rstrip() + "..."
        return sentence
    return fallback_title


def infer_category(title: str, body: str) -> str:
    text = f"{title}\n{body}".lower()
    rules = [
        ("电商运营", ("电商", "淘宝", "拼多多", "抖店", "店铺", "客服", "ecommerce")),
        ("独立站", ("独立站", "shopify", "woocommerce", "落地页", "landing page")),
        ("内容创作", ("内容", "小红书", "公众号", "短视频", "视频", "脚本", "写作", "创作")),
        ("开源项目", ("开源", "github", "repository", "repo", "open source")),
        ("海外获客", ("海外", "获客", "linkedin", "外贸", "出海", "b2b", "lead")),
        ("AI副业赚钱", ("副业", "赚钱", "变现", "收入", "月入", "revenue", "monetize")),
        ("AI自动化", ("自动化", "workflow", "agent", "zapier", "make.com", "n8n")),
    ]
    for category, keywords in rules:
        if any(keyword in text for keyword in keywords):
            return category
    return TUTORIAL_CATEGORIES[0]


def validate_values(values: dict[str, str | bool]) -> list[str]:
    errors = []
    for field in REQUIRED_FIELDS:
        if not str(values.get(field) or "").strip():
            errors.append(f"{label_for(field)} 必填。")
    category = str(values.get("category") or "").strip()
    if category and category not in TUTORIAL_CATEGORIES:
        errors.append("分类无效，请从下拉框选择。")
    return errors


def render_page(
    success: str = "",
    errors: list[str] | None = None,
    values: dict[str, str | bool] | None = None,
    import_url: str = "",
    status_code: int = 200,
) -> str:
    del status_code
    values = values or default_values()
    errors = errors or []
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>信先行教程录入</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #faf8f5;
      --surface: #fffdf9;
      --border: #e0dbd3;
      --text: #2d2a3e;
      --muted: #756f89;
      --accent: #e0652e;
      --primary: #2f2b73;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.6;
    }}
    main {{
      width: min(100% - 32px, 980px);
      margin: 0 auto;
      padding: 32px 0 56px;
    }}
    header {{
      margin-bottom: 20px;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(30px, 6vw, 48px);
      line-height: 1.1;
    }}
    header p {{
      margin: 10px 0 0;
      color: var(--muted);
    }}
    form {{
      display: grid;
      gap: 18px;
      padding: 20px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
    }}
    label {{
      display: grid;
      gap: 6px;
      font-weight: 800;
    }}
    label span {{
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
    }}
    input, select, textarea {{
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 12px;
      color: var(--text);
      background: #fff;
      font: inherit;
    }}
    textarea {{
      min-height: 116px;
      resize: vertical;
    }}
    textarea.tall {{
      min-height: 180px;
    }}
    .checkbox {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 800;
    }}
    .checkbox input {{
      width: 18px;
      height: 18px;
    }}
    .actions {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }}
    button {{
      border: 1px solid var(--primary);
      border-radius: 8px;
      padding: 11px 18px;
      color: #fff;
      background: var(--primary);
      font: inherit;
      font-weight: 900;
      cursor: pointer;
    }}
    .hint {{
      color: var(--muted);
      font-size: 14px;
    }}
    .message {{
      margin-bottom: 16px;
      padding: 12px 14px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #fff;
      font-weight: 800;
    }}
    .message.success {{
      border-color: #1d7f64;
      color: #12664f;
    }}
    .message.error {{
      border-color: #be185d;
      color: #9f1239;
    }}
    .import-box {{
      display: grid;
      gap: 12px;
      margin-bottom: 16px;
      padding: 16px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #fff;
    }}
    .import-box h2 {{
      margin: 0;
      font-size: 20px;
    }}
    .import-row {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
    }}
    .import-box .hint {{
      margin: 0;
    }}
    @media (max-width: 760px) {{
      .grid {{
        grid-template-columns: 1fr;
      }}
      .import-row {{
        grid-template-columns: 1fr;
      }}
      form {{
        padding: 16px;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>信先行教程录入</h1>
      <p>提交后会生成 Markdown 草稿到 <code>data/tutorials/drafts/</code>，确认后再手动移动到 published。</p>
    </header>
    {render_messages(success, errors)}
    <form class="import-box" method="post" action="/import">
      <h2>粘贴链接采集</h2>
      <div class="import-row">
        <input type="url" name="import_url" value="{value_attr(import_url)}" placeholder="https://example.com/article" required>
        <button type="submit">采集并预填</button>
      </div>
      <p class="hint">会自动抓取标题、来源和正文，预填到下面表单；保存前请人工整理成教程结构。</p>
    </form>
    <form method="post" action="/tutorials">
      <div class="grid">
        {input_field("title", "教程标题", values, required=True)}
        {select_field("category", "分类", values, required=True)}
        {input_field("summary", "一句话说明", values, required=True)}
        {input_field("audience", "适合谁/适用场景", values)}
        {input_field("source_author", "原作者", values)}
        {input_field("source_url", "原帖链接", values, input_type="url")}
        {input_field("updated_at", "更新时间", values, input_type="date")}
      </div>
      {textarea_field("source_summary", "原帖核心观点", values, tall=True)}
      {textarea_field("steps", "中文步骤拆解", values, tall=True)}
      {textarea_field("tools", "使用工具", values)}
      {textarea_field("prompt_template", "可复制Prompt", values, tall=True)}
      {textarea_field("case_result", "实操案例/实测结果", values, tall=True)}
      {textarea_field("alternatives", "国内可替代方案", values)}
      {textarea_field("cost_and_effect", "成本与预计效果", values)}
      {textarea_field("risk_notice", "风险和注意事项", values, tall=True)}
      <label class="checkbox">
        <input type="checkbox" name="is_member_only" value="1" {checked_attr(values.get("is_member_only"))}>
        是否需要会员权限
      </label>
      <div class="actions">
        <button type="submit">保存为草稿</button>
        <span class="hint">必填：教程标题、一句话说明、分类。</span>
      </div>
    </form>
  </main>
</body>
</html>
"""


def render_messages(success: str, errors: list[str]) -> str:
    if success:
        return f'<div class="message success">{html.escape(success)}</div>'
    if errors:
        items = "".join(f"<li>{html.escape(error)}</li>" for error in errors)
        return f'<div class="message error"><strong>保存失败：</strong><ul>{items}</ul></div>'
    return ""


def input_field(
    name: str,
    label: str,
    values: dict[str, str | bool],
    input_type: str = "text",
    required: bool = False,
) -> str:
    required_attr = " required" if required else ""
    return (
        f'<label>{html.escape(label)}'
        f'<input type="{html.escape(input_type)}" name="{html.escape(name)}" '
        f'value="{value_attr(values.get(name))}"{required_attr}></label>'
    )


def select_field(
    name: str,
    label: str,
    values: dict[str, str | bool],
    required: bool = False,
) -> str:
    required_attr = " required" if required else ""
    current = str(values.get(name) or "")
    options = "".join(
        f'<option value="{html.escape(category, quote=True)}"'
        f'{" selected" if category == current else ""}>{html.escape(category)}</option>'
        for category in TUTORIAL_CATEGORIES
    )
    return f'<label>{html.escape(label)}<select name="{html.escape(name)}"{required_attr}>{options}</select></label>'


def textarea_field(
    name: str,
    label: str,
    values: dict[str, str | bool],
    tall: bool = False,
) -> str:
    class_attr = ' class="tall"' if tall else ""
    return (
        f'<label>{html.escape(label)}'
        f'<textarea name="{html.escape(name)}"{class_attr}>'
        f'{html.escape(str(values.get(name) or ""))}</textarea></label>'
    )


def checked_attr(value: object) -> str:
    return "checked" if bool(value) else ""


def value_attr(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def label_for(field: str) -> str:
    return TUTORIAL_FIELD_LABELS.get(field, field)


if __name__ == "__main__":
    main()
