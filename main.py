import json
from pathlib import Path

STATUS_ORDER = ["on_plan", "on_developing", "done"]

STATUS_TITLES = {
    "en": {
        "on_plan": "Planned",
        "on_developing": "In Development",
        "done": "Completed",
    },
    "zh": {
        "on_plan": "已计划",
        "on_developing": "开发中",
        "done": "已完成",
    },
}

EMPTY_COPY = {
    "en": {
        "on_plan": "No queued bindings yet—add one via the [wishlist](wishlist.md).",
        "on_developing": "Nothing is in active development right now.",
        "done": "No releases yet—stay tuned!",
    },
    "zh": {
        "on_plan": "暂未排期新项目，欢迎通过 [心愿单](wishlist.md) 提案。",
        "on_developing": "当前没有活跃开发中的项目。",
        "done": "尚无发布记录，敬请期待。",
    },
}

HEADERS = {
    "en": "| Project | Upstream | Link | Description |",
    "zh": "| 项目 | 原链接 | 链接 | 描述 |",
}

SEPARATOR = "| --- | --- | --- | --- |"


def _load_projects():
    json_path = Path(__file__).parent / "projects.json"
    if not json_path.exists():
        return []
    with json_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _format_cell(text: str) -> str:
    if not text:
        return "—"
    return text.replace("|", r"\|").replace("\n", "<br>")


def _format_link(link: dict) -> str:
    if not link or not link.get("url"):
        return "—"
    label = link.get("label") or link["url"]
    return f"[{label}]({link['url']})"


def _group_by_status(projects):
    grouped = {status: [] for status in STATUS_ORDER}
    for item in projects:
        status = item.get("status")
        if status not in grouped:
            continue
        grouped[status].append(item)
    for items in grouped.values():
        items.sort(key=lambda entry: entry.get("name", "").lower())
    return grouped


def define_env(env):
    projects = _group_by_status(_load_projects())
    env.variables["project_status_order"] = STATUS_ORDER
    env.variables["project_headings"] = STATUS_TITLES

    @env.macro
    def projects_table(lang: str, status: str) -> str:
        if lang not in HEADERS:
            raise ValueError(f"Unsupported language '{lang}' for projects_table macro.")
        rows = [HEADERS[lang], SEPARATOR]
        items = projects.get(status, [])
        if not items:
            rows.append(f"| _{EMPTY_COPY[lang][status]}_ | — | — | — |")
            return "\n".join(rows)
        for entry in items:
            desc = entry.get("desc") or {}
            desc_text = desc.get(lang) or desc.get("en") or ""
            rows.append(
                "| {project} | {origin} | {link} | {desc} |".format(
                    project=_format_cell(entry.get("name", "")),
                    origin=_format_link(entry.get("origin")),
                    link=_format_link(entry.get("link")),
                    desc=_format_cell(desc_text),
                )
            )
        return "\n".join(rows)
