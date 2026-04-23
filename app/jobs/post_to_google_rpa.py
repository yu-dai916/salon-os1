from pathlib import Path
import uuid
from playwright.sync_api import sync_playwright


def run(location_id: str, text: str):
    user_data_dir = f"/tmp/pw-{uuid.uuid4()}"  # ←ここ修正

    post_url = f"https://business.google.com/posts/l/{location_id}"

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
    user_data_dir=user_data_dir,
    headless=True,  # ←これ
    viewport={"width": 1440, "height": 900},
)

        page = browser.pages[0] if browser.pages else browser.new_page()

        page.goto(post_url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)

        candidates = [
            'textarea',
            '[contenteditable="true"]',
            '[role="textbox"]',
        ]

        filled = False

        for sel in candidates:
            loc = page.locator(sel)
            if loc.count() > 0:
                try:
                    first = loc.first
                    first.click(timeout=3000)
                    first.fill(text, timeout=3000)
                    filled = True
                    break
                except Exception:
                    try:
                        first.click(timeout=3000)
                        page.keyboard.press("Meta+A")
                        page.keyboard.type(text)
                        filled = True
                        break
                    except Exception:
                        pass

        if not filled:
            browser.close()
            raise RuntimeError("入力欄見つからん")

        page.wait_for_timeout(2000)
        browser.close()