def format_for_google_post(
    title: str,
    excerpt: str,
    source_url: str,
    area: str,
    main_menu: str,
    store_name: str,
    phone_number: str | None,
    cta_url: str | None,
) -> str:

    phone = phone_number or ""
    cta = cta_url or ""

    # None対策（これ重要）
    area = area or ""
    main_menu = main_menu or ""

    seo_title = f"{area} 美容室｜{main_menu}なら{store_name}"

    body = f"""
{area}の美容室「{store_name}」です。

今回は【{main_menu}】のご紹介。

{excerpt}

ダメージを抑えながら、ツヤとまとまりのある仕上がりに。
"""

    if cta:
        body += f"\n▼ご予約はこちら\n{cta}"
    elif phone:
        body += f"\n▼お電話はこちら\n{phone}"

    body += f"\n\n▼詳しくはこちら\n{source_url}"

    return f"{seo_title}\n\n{body.strip()}"