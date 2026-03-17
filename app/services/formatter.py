def format_for_google_post(title: str, excerpt: str, source_url: str) -> str:
    title = (title or "").strip()
    excerpt = (excerpt or "").strip()

    lines = []
    if title:
        lines.append(f"")
    if excerpt:
        lines.append(excerpt)

    lines.append("")
    lines.append("▼詳細はこちら")
    lines.append(source_url)

    return "\n".join(lines).strip()