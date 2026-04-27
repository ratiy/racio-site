#!/usr/bin/env python3
"""Align all service pages to 13-block target structure (matching autsorsynh.html).

Removes:
- Quick form section (стрічка під hero)
- SEO-A prose block (.seo-prose)

Keeps everything else.

Note: «Для кого / Коли» block already exists on most pages (only autsorsynh was missing it,
already fixed manually).
"""
import re
import sys
from pathlib import Path

RACIO = Path(__file__).resolve().parent

# All service pages EXCEPT autsorsynh (already done manually)
PAGES = [
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


def find_balanced_section_with(html: str, marker_pattern: str):
    """Find first <section>...</section> containing marker. Returns (start, end) or None."""
    for m in re.finditer(r'<section[^>]*>', html):
        start = m.start()
        # walk balanced
        depth = 1
        pos = m.end()
        while depth > 0 and pos < len(html):
            nm = re.search(r'<(/?)section(\s[^>]*)?>', html[pos:])
            if not nm:
                break
            if nm.group(1) == '/':
                depth -= 1
                pos += nm.end()
                if depth == 0:
                    break
            else:
                depth += 1
                pos += nm.end()
        if depth != 0:
            continue
        section_html = html[start:pos]
        if re.search(marker_pattern, section_html):
            return (start, pos)
    return None


def strip_section(html: str, start: int, end: int) -> str:
    """Remove section [start,end) plus immediately preceding HTML comment if any."""
    look_back_window = 250
    look_back_start = max(0, start - look_back_window)
    look_back = html[look_back_start:start]
    # match a comment block at end of look_back (optionally followed by whitespace)
    cm = re.search(r'<!--[^>]*?-->\s*\Z', look_back, re.S)
    if cm:
        actual_start = look_back_start + cm.start()
    else:
        actual_start = start
    return html[:actual_start].rstrip() + '\n\n' + html[end:].lstrip('\n')


def process_file(path: Path):
    html = path.read_text(encoding='utf-8')
    original = html
    changes = []

    # 1. Remove Quick form section
    found = find_balanced_section_with(html, r'<div class="qform"')
    if found:
        html = strip_section(html, *found)
        changes.append('Quick form')

    # 2. Remove SEO-A (uses .seo-prose, distinct from .seo-desc placeholder)
    found = find_balanced_section_with(html, r'<div class="seo-prose"')
    if found:
        html = strip_section(html, *found)
        changes.append('SEO-A prose')

    if html != original:
        path.write_text(html, encoding='utf-8')
        return changes
    return None


def word_count(html: str) -> int:
    t = re.sub(r'<(script|style|svg)[^>]*>.*?</\1>', '', html, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return len(re.sub(r'\s+', ' ', t).strip().split())


def main():
    print(f"{'PAGE':<40s} {'BEFORE':>7s} -> {'AFTER':>6s}  CHANGES")
    print('-' * 80)
    total_removed = 0
    for f in PAGES:
        p = RACIO / f
        if not p.exists():
            print(f"  ! {f} not found")
            continue
        before = word_count(p.read_text())
        changes = process_file(p)
        after = word_count(p.read_text())
        diff = before - after
        total_removed += diff
        marker = ', '.join(changes) if changes else '(no change)'
        print(f"  {f:<38s} {before:>7d} -> {after:>6d}  {marker}")
    print('-' * 80)
    print(f"Total words removed across all pages: {total_removed}")


if __name__ == "__main__":
    main()
