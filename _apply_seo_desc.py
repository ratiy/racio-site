#!/usr/bin/env python3
"""Insert SEO description placeholder block after hero section on all service pages.

Usage: python3 _apply_seo_desc.py
"""
import re
import sys
from pathlib import Path

RACIO = Path(__file__).resolve().parent

SERVICE_FILES = [
    "autsorsynh.html",
    "audit.html",
    "dokumentatsiia.html",
    "pakety-dokumentiv.html",
    "treningy-z-ohorony-pratsi.html",
    "rozsliduvannia-nv.html",
    "suprovid-derzhpratsi.html",
    "autsorsynh-pojejna-bezpeka.html",
    "audit-pojejna-bezpeka.html",
    "dokumentatsiia-pojejna-bezpeka.html",
    "treningy-z-pojejnoi-bezpeky.html",
    "deklaratsiia-dsns.html",
    "otsinka-ryzykiv.html",
    "tsyvilnyi-zakhyst.html",
    "treningy-z-bezpeky-pratsi.html",
]

SEO_DESC_BLOCK = """
<!-- SEO · Опис послуги (placeholder для копірайтера) -->
<section class="cream">
  <div class="container">
    <div class="sec-head"><div class="eyebrow">Опис послуги</div></div>
    <div class="seo-desc">
      <div class="seo-desc-card">
        <h2 class="placeholder">[H2 · Назва послуги · ВЕЛИКИМИ]</h2>
        <p class="lead placeholder">[Lead-параграф · 2-3 речення · формальне визначення послуги, її основна цінність для бізнесу]</p>
        <a href="#quiz" class="btn btn-primary">Замовити консультацію</a>
      </div>
      <div class="seo-desc-text">
        <p class="placeholder">[Параграф 1 · ~80 слів · типові ситуації звернення, для кого підходить ця послуга, з якими проблемами клієнти приходять]</p>
        <p class="placeholder">[Параграф 2 · ~80 слів · як ми працюємо у цьому напрямку, ключові моменти процесу, що робить нас ефективними]</p>
        <p class="placeholder">[Параграф 3 · ~50 слів · заклик до дії, чому варто почати з безкоштовної консультації або аудиту, що отримає клієнт після першого дзвінка]</p>
      </div>
    </div>
  </div>
</section>
"""


def insert_after_hero(html: str) -> tuple[str, bool]:
    """Insert SEO desc block after the first <section class="hero">...</section>."""
    # Skip if already inserted
    if "SEO · Опис послуги" in html:
        return html, False

    # Find balanced hero section (matches "hero" possibly with extra classes like "hero dark")
    open_re = re.compile(r'<section\s+class="[^"]*\bhero\b[^"]*">', re.S)
    m = open_re.search(html)
    if not m:
        return html, False

    # Walk to balanced </section>
    depth = 1
    pos = m.end()
    while depth > 0 and pos < len(html):
        nm = re.search(r'<(/?)section(\s[^>]*)?>', html[pos:])
        if not nm:
            return html, False
        if nm.group(1) == "/":
            depth -= 1
        else:
            depth += 1
        pos += nm.end()
        if depth == 0:
            break
    if depth != 0:
        return html, False

    # Insert block after hero close tag
    return html[:pos] + SEO_DESC_BLOCK + html[pos:], True


def main():
    inserted = 0
    skipped = 0
    for f in SERVICE_FILES:
        path = RACIO / f
        if not path.exists():
            print(f"  ! {f} not found")
            continue
        html = path.read_text(encoding="utf-8")
        new_html, did_insert = insert_after_hero(html)
        if did_insert:
            path.write_text(new_html, encoding="utf-8")
            inserted += 1
            print(f"  + {f}")
        else:
            skipped += 1
            print(f"  - {f} (already has block or no hero)")
    print(f"\nDone: inserted={inserted} skipped={skipped}")


if __name__ == "__main__":
    main()
