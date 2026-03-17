import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}


def fetch_latest_blog(blog_url: str) -> dict:
    """
    HPBブログ一覧URLから最新記事を1件返す
    戻り値:
      {
        "title": "...",
        "url": "https://beauty.hotpepper.jp/.../blog/bidA....html",
        "excerpt": "..."
      }
    失敗時:
      {
        "debug": "..."
      }
    """
    try:
        r = requests.get(blog_url, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except Exception as e:
        return {"debug": f"request_failed: {e}"}

    soup = BeautifulSoup(r.text, "html.parser")

    # -------------------------
    # 1) 一覧ページから記事リンクを拾う
    # -------------------------
    article_url = None

    # HPBのブログ記事URLは /blog/bidAxxxxxxx.html の形が多い
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        full_url = urljoin(blog_url, href)

        if "/blog/bid" in full_url and full_url.endswith(".html"):
            article_url = full_url
            break

    if not article_url:
        return {"debug": "article_url_not_found"}

    # -------------------------
    # 2) 記事ページを取得
    # -------------------------
    try:
        r2 = requests.get(article_url, headers=HEADERS, timeout=20)
        r2.raise_for_status()
    except Exception as e:
        return {"debug": f"article_request_failed: {e}"}

    soup2 = BeautifulSoup(r2.text, "html.parser")

    # タイトル候補
    title = ""
    title_candidates = [
        "h1",
        ".blogDetailTitle",
        ".pBlogDetail_title",
        ".title",
    ]
    for sel in title_candidates:
        el = soup2.select_one(sel)
        if el:
            title = el.get_text(" ", strip=True)
            if title:
                break

    # 本文候補
    excerpt = ""
    excerpt_candidates = [
        ".blogDetailText",
        ".pBlogDetail_body",
        ".blog_detail",
        ".detailText",
        "article",
    ]
    for sel in excerpt_candidates:
        el = soup2.select_one(sel)
        if el:
            text = el.get_text(" ", strip=True)
            if text:
                excerpt = text[:200]
                break

    # タイトルが空ならtitleタグから補完
    if not title:
        if soup2.title:
            title = soup2.title.get_text(" ", strip=True)
        else:
            title = "ブログ"

    return {
        "title": title,
        "url": article_url,
        "excerpt": excerpt,
    }