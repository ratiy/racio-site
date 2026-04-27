#!/usr/bin/env python3
"""Extract copy from RACIO HTML pages into per-page markdown files for copywriter.

Usage: python3 _extract_copy.py
Output: docs/copy/*.md
"""
import re
import os
import html as html_module
from pathlib import Path

RACIO_DIR = Path(__file__).resolve().parent.parent
DOCS_COPY = RACIO_DIR / "docs" / "copy"

# Page inventory: (filename, display title, breadcrumb path, category)
PAGES = [
    ("index.html",                          "Головна",                               "/",                                                    "home"),
    # ОП
    ("autsorsynh.html",                     "Аутсорсинг охорони праці",              "/ › Охорона праці › Аутсорсинг",                       "op"),
    ("audit.html",                          "Аудит охорони праці",                   "/ › Охорона праці › Аудит ОП",                         "op"),
    ("dokumentatsiia.html",                 "Розробка документації з ОП",            "/ › Охорона праці › Документація",                     "op"),
    ("pakety-dokumentiv.html",              "Пакети документів з ОП",                "/ › Охорона праці › Пакети документів",                "op"),
    ("treningy-z-ohorony-pratsi.html",      "Тренінги з охорони праці",              "/ › Охорона праці › Тренінги з ОП",                    "op"),
    ("rozsliduvannia-nv.html",              "Розслідування нещасних випадків",       "/ › Охорона праці › Розслідування НВ",                 "op"),
    ("suprovid-derzhpratsi.html",           "Супровід перевірок Держпраці",          "/ › Охорона праці › Супровід Держпраці",               "op"),
    # ПБ
    ("autsorsynh-pojejna-bezpeka.html",     "Аутсорсинг пожежної безпеки",           "/ › Пожежна безпека › Аутсорсинг ПБ",                  "pb"),
    ("audit-pojejna-bezpeka.html",          "Аудит пожежної безпеки",                "/ › Пожежна безпека › Аудит ПБ",                       "pb"),
    ("dokumentatsiia-pojejna-bezpeka.html", "Документація з пожежної безпеки",       "/ › Пожежна безпека › Документація",                   "pb"),
    ("treningy-z-pojejnoi-bezpeky.html",    "Тренінги з пожежної безпеки",           "/ › Пожежна безпека › Тренінги з ПБ",                  "pb"),
    ("deklaratsiia-dsns.html",              "Декларація відповідності ДСНС",         "/ › Пожежна безпека › Декларація ДСНС",                "pb"),
    # КР
    ("otsinka-ryzykiv.html",                "Оцінка ризиків на робочих місцях",      "/ › Керування ризиками › Оцінка ризиків",              "kr"),
    ("tsyvilnyi-zakhyst.html",              "Цивільний захист і техногенна безпека", "/ › Керування ризиками › Цивільний захист",            "kr"),
    ("treningy-z-bezpeky-pratsi.html",      "Тренінги з безпеки праці",              "/ › Керування ризиками › Тренінги з безпеки праці",    "kr"),
    # Про нас
    ("pro-kompaniyu.html",                  "Про компанію RACIO",                    "/ › Про нас › Про компанію",                           "about"),
    ("kliyenty-ta-keysu.html",              "Клієнти та кейси",                      "/ › Про нас › Клієнти та кейси",                       "about"),
    ("kontakty.html",                       "Контакти",                              "/ › Про нас › Контакти",                               "about"),
    # Ще
    ("halusi.html",                         "Галузі",                                "/ › Ще › Галузі",                                      "extra"),
    ("tarify.html",                         "Тарифи",                                "/ › Ще › Тарифи",                                      "extra"),
    # Блог
    ("blog.html",                           "Блог",                                  "/ › Блог › Статті",                                    "blog"),
    ("koryisne.html",                       "Корисне",                               "/ › Блог › Корисне",                                   "blog"),
]


def strip_tags(html: str) -> str:
    """Remove HTML tags, return plain text with cleaned whitespace."""
    # Remove comments
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    # Remove tags
    text = re.sub(r"<[^>]+>", " ", html)
    # Decode entities
    text = html_module.unescape(text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_inner(tag_html: str) -> str:
    """Extract inner text of a simple tag, keeping <em>, <b>, <a href> as markdown-ish."""
    # Convert <em> to _italic_
    tag_html = re.sub(r"<em[^>]*>(.*?)</em>", r"_\1_", tag_html, flags=re.S)
    # Convert <b> / <strong> to **bold**
    tag_html = re.sub(r"<b[^>]*>(.*?)</b>", r"**\1**", tag_html, flags=re.S)
    tag_html = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", tag_html, flags=re.S)
    # Convert <a href="X">text</a> to [text](X)
    def link_sub(m):
        href = m.group(1)
        text = strip_tags(m.group(2))
        return f"[{text}]({href})"
    tag_html = re.sub(r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', link_sub, tag_html, flags=re.S)
    return strip_tags(tag_html)


def extract_meta(html: str) -> dict:
    meta = {}
    m = re.search(r"<title>([^<]+)</title>", html)
    meta["title_tag"] = html_module.unescape(m.group(1).strip()) if m else ""
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html)
    meta["meta_description"] = html_module.unescape(m.group(1).strip()) if m else ""
    return meta


def find_sections(html: str) -> list:
    """Split HTML into <section>...</section> blocks. Return list of (index, html-block)."""
    sections = []
    # Use a balanced-depth approach: find each <section ...> and its matching </section>
    pos = 0
    idx = 0
    while True:
        m = re.search(r"<section(\s[^>]*)?>", html[pos:])
        if not m:
            break
        start = pos + m.start()
        # Find matching close
        depth = 1
        scan = pos + m.end()
        while depth > 0:
            nm = re.search(r"<(/?)section(\s[^>]*)?>", html[scan:])
            if not nm:
                break
            if nm.group(1) == "/":
                depth -= 1
            else:
                depth += 1
            scan += nm.end()
            if depth == 0:
                break
        if depth != 0:
            break
        sections.append((idx, html[start:scan]))
        idx += 1
        pos = scan
    return sections


def classify_section(section_html: str) -> dict:
    """Classify section type and extract key content."""
    out = {
        "bg": "default",
        "classes": "",
        "eyebrow": "",
        "heading": "",
        "heading_level": "",
        "blocks": [],
        "raw_length": len(section_html),
    }
    # Section background class
    opening = re.search(r"<section([^>]*)>", section_html).group(1)
    m = re.search(r'class="([^"]+)"', opening)
    if m:
        classes = m.group(1)
        out["classes"] = classes
        for tag in ("cream", "dark", "red"):
            if tag in classes:
                out["bg"] = tag
                break
        if "hero" in classes:
            out["bg"] = "hero"
        if "finalcta" in classes:
            out["bg"] += " finalcta"
    # ID
    m = re.search(r'id="([^"]+)"', opening)
    if m:
        out["section_id"] = m.group(1)

    # Eyebrow
    m = re.search(r'<div class="eyebrow">([^<]*)</div>', section_html)
    if m:
        out["eyebrow"] = html_module.unescape(m.group(1).strip())

    # Heading
    for level in ("h1", "h2", "h3"):
        m = re.search(rf"<{level}[^>]*>(.*?)</{level}>", section_html, flags=re.S)
        if m:
            out["heading"] = extract_inner(m.group(1))
            out["heading_level"] = level
            break

    return out


def extract_paragraphs(section_html: str) -> list:
    return [extract_inner(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", section_html, flags=re.S)]


def extract_list_items(section_html: str) -> list:
    return [extract_inner(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", section_html, flags=re.S)]


def extract_balanced(html: str, tag: str, class_marker: str) -> list:
    """Extract balanced <tag class='...class_marker...'>...</tag> bodies.

    Handles nested tags of the same name correctly.
    """
    results = []
    pos = 0
    open_re = re.compile(rf'<{tag}(\s+[^>]*class="[^"]*\b{class_marker}\b[^"]*"[^>]*)>', re.S)
    tag_re = re.compile(rf'<(/?){tag}(\s[^>]*)?>', re.S)
    while pos < len(html):
        m = open_re.search(html, pos)
        if not m:
            break
        body_start = m.end()
        scan = body_start
        depth = 1
        while depth > 0 and scan < len(html):
            nm = tag_re.search(html, scan)
            if not nm:
                break
            if nm.group(1) == '/':
                depth -= 1
                scan = nm.end()
                if depth == 0:
                    break
            else:
                depth += 1
                scan = nm.end()
        if depth != 0:
            break
        results.append(html[body_start:nm.start()])  # body only (without closing tag)
        pos = scan
    return results


def extract_balanced_any(html: str, tags: list, class_marker: str) -> list:
    """Try multiple tags for the same class marker (e.g. card can be div or a)."""
    results = []
    for tag in tags:
        results.extend(extract_balanced(html, tag, class_marker))
    # Preserve original order by position in html
    # (caller gets them grouped by tag; fine for our use)
    return results


def extract_cards(section_html: str) -> list:
    """Extract cards: num, h3/h4 title, paragraphs. Uses balanced tag extraction."""
    cards = []
    bodies = extract_balanced_any(section_html, ["div", "a"], "card")
    for body in bodies:
        card = {}
        nm = re.search(r'<div class="num">(.*?)</div>', body, flags=re.S)
        card["num"] = extract_inner(nm.group(1)) if nm else ""
        for lvl in ("h3", "h4"):
            hm = re.search(rf"<{lvl}[^>]*>(.*?)</{lvl}>", body, flags=re.S)
            if hm:
                card["title"] = extract_inner(hm.group(1))
                break
        card["body"] = [extract_inner(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", body, flags=re.S)]
        sublis = re.findall(r"<li[^>]*>(.*?)</li>", body, flags=re.S)
        if sublis:
            card["items"] = [extract_inner(li) for li in sublis]
        mm = re.search(r'<span class="more">(.*?)</span>', body, flags=re.S)
        if mm:
            card["more"] = extract_inner(mm.group(1))
        cards.append(card)
    return cards


def extract_process_steps(section_html: str) -> list:
    steps = []
    for body in extract_balanced(section_html, "div", "step"):
        nm = re.search(r'<div class="num">(.*?)</div>', body, flags=re.S)
        tm = re.search(r'<h3[^>]*>(.*?)</h3>', body, flags=re.S)
        timem = re.search(r'<div class="time">(.*?)</div>', body, flags=re.S)
        pm = re.search(r'<p[^>]*>(.*?)</p>', body, flags=re.S)
        steps.append({
            "num": extract_inner(nm.group(1)) if nm else "",
            "title": extract_inner(tm.group(1)) if tm else "",
            "time": extract_inner(timem.group(1)) if timem else "",
            "description": extract_inner(pm.group(1)) if pm else "",
        })
    return steps


def extract_deliverables(section_html: str) -> list:
    """Extract .deliv list (h4 + p)."""
    items = []
    m = re.search(r'<ul class="deliv"[^>]*>(.*?)</ul>', section_html, flags=re.S)
    if not m:
        return items
    for li in re.finditer(r"<li[^>]*>(.*?)</li>", m.group(1), flags=re.S):
        body = li.group(1)
        hm = re.search(r'<h4[^>]*>(.*?)</h4>', body, flags=re.S)
        pm = re.search(r'<p[^>]*>(.*?)</p>', body, flags=re.S)
        if hm or pm:
            items.append({
                "title": extract_inner(hm.group(1)) if hm else "",
                "description": extract_inner(pm.group(1)) if pm else "",
            })
    return items


def extract_num_list(section_html: str) -> list:
    """Extract .num-list items (h4 + p)."""
    items = []
    m = re.search(r'<ol class="num-list"[^>]*>(.*?)</ol>', section_html, flags=re.S)
    if not m:
        return items
    for li in re.finditer(r"<li[^>]*>(.*?)</li>", m.group(1), flags=re.S):
        body = li.group(1)
        hm = re.search(r'<h4[^>]*>(.*?)</h4>', body, flags=re.S)
        pm = re.search(r'<p[^>]*>(.*?)</p>', body, flags=re.S)
        items.append({
            "title": extract_inner(hm.group(1)) if hm else "",
            "description": extract_inner(pm.group(1)) if pm else "",
        })
    return items


def extract_kpi(section_html: str) -> list:
    items = []
    m = re.search(r'<div class="kpi">(.*?)</div>\s*</div>\s*</section>', section_html, flags=re.S)
    if not m:
        return items
    for divm in re.finditer(r'<div><div class="v">(.*?)</div><div class="l">(.*?)</div></div>', m.group(1), flags=re.S):
        items.append({"value": extract_inner(divm.group(1)), "label": extract_inner(divm.group(2))})
    return items


def extract_testimonials(section_html: str) -> list:
    items = []
    # Find the .testi wrapper first
    testis = extract_balanced(section_html, "div", "testi")
    if not testis:
        return items
    wrapper = testis[0]
    # Find individual .t cards within
    for body in extract_balanced(wrapper, "div", "t"):
        hm = re.search(r'<h3[^>]*>(.*?)</h3>', body, flags=re.S)
        pm = re.search(r'<p[^>]*>(.*?)</p>', body, flags=re.S)
        wm = re.search(r'<div class="who">(.*?)</div>', body, flags=re.S)
        if hm or pm:
            items.append({
                "quote_title": extract_inner(hm.group(1)) if hm else "",
                "quote_body": extract_inner(pm.group(1)) if pm else "",
                "author": extract_inner(wm.group(1)) if wm else "",
            })
    return items


def extract_logos(section_html: str) -> list:
    m = re.search(r'<div class="logos">(.*?)</div>', section_html, flags=re.S)
    if not m:
        return []
    return [html_module.unescape(s.strip()) for s in re.findall(r'<span>([^<]+)</span>', m.group(1))]


def extract_faq(section_html: str) -> list:
    items = []
    for dm in re.finditer(r'<details[^>]*>(.*?)</details>', section_html, flags=re.S):
        body = dm.group(1)
        sm = re.search(r'<summary[^>]*>(.*?)</summary>', body, flags=re.S)
        pm = re.search(r'<p[^>]*>(.*?)</p>', body, flags=re.S)
        items.append({
            "question": extract_inner(sm.group(1)) if sm else "",
            "answer": extract_inner(pm.group(1)) if pm else "",
        })
    return items


def extract_quiz(section_html: str) -> list:
    steps = []
    for m in re.finditer(r'<div class="quiz-step[^"]*"\s+data-step="(\d+)">(.*?)</div>\s*(?=<div class="quiz-step|<div class="quiz-fields)', section_html, flags=re.S):
        step_num = m.group(1)
        body = m.group(2)
        hm = re.search(r'<h3[^>]*>(.*?)</h3>', body, flags=re.S)
        opts = [extract_inner(o) for o in re.findall(r'<button class="quiz-opt">(.*?)</button>', body, flags=re.S)]
        steps.append({
            "step": step_num,
            "question": extract_inner(hm.group(1)) if hm else "",
            "options": opts,
        })
    return steps


def extract_form(section_html: str) -> dict:
    """Quick form or inline form."""
    f = {}
    hm = re.search(r'<div class="qform">(.*?)</div>\s*</div>', section_html, flags=re.S)
    if hm:
        body = hm.group(1)
        h3 = re.search(r'<h3[^>]*>(.*?)</h3>', body, flags=re.S)
        hint = re.search(r'<div class="hint">(.*?)</div>', body, flags=re.S)
        placeholders = re.findall(r'placeholder="([^"]+)"', body)
        buttons = [extract_inner(b) for b in re.findall(r'<button[^>]*>(.*?)</button>', body, flags=re.S)]
        f = {
            "heading": extract_inner(h3.group(1)) if h3 else "",
            "hint": extract_inner(hint.group(1)) if hint else "",
            "fields": placeholders,
            "buttons": buttons,
        }
    return f


def extract_ctas(section_html: str) -> list:
    """Extract primary/ghost CTAs (hero-cta or final btns)."""
    ctas = []
    for m in re.finditer(
        r'<a\s+[^>]*href="([^"]+)"[^>]*class="[^"]*\bbtn\b[^"]*"[^>]*>(.*?)</a>',
        section_html,
        flags=re.S,
    ):
        ctas.append({"text": extract_inner(m.group(2)), "href": m.group(1)})
    # Also match class then href ordering variant
    for m in re.finditer(
        r'<a\s+[^>]*class="[^"]*\bbtn\b[^"]*"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        section_html,
        flags=re.S,
    ):
        entry = {"text": extract_inner(m.group(2)), "href": m.group(1)}
        if entry not in ctas:
            ctas.append(entry)
    return ctas


def extract_trust_chips(section_html: str) -> list:
    m = re.search(r'<div class="hero-trust">(.*?)</div>', section_html, flags=re.S)
    if not m:
        return []
    return [extract_inner(s) for s in re.findall(r'<span>(.*?)</span>', m.group(1), flags=re.S)]


def extract_catalog_cols(section_html: str) -> list:
    """For home page catalog block with .catalog-col."""
    cols = []
    for body in extract_balanced(section_html, "div", "catalog-col"):
        hm = re.search(r'<h3[^>]*>(.*?)</h3>', body, flags=re.S)
        heading = extract_inner(hm.group(1)) if hm else ""
        items = []
        for am in re.finditer(r'<li[^>]*>\s*<a\s+href="([^"]+)"[^>]*>(.*?)</a>\s*</li>', body, flags=re.S):
            items.append({"href": am.group(1), "text": extract_inner(am.group(2))})
        cols.append({"heading": heading, "items": items})
    return cols


def extract_hub_tiles(section_html: str) -> list:
    """For hub-tiles block (home 4 directions / 3 training hubs)."""
    tiles = []
    # .hub can be <a> — find balanced
    for body in extract_balanced(section_html, "a", "hub"):
        href_m = re.search(r'<a\s[^>]*href="([^"]+)"[^>]*class="[^"]*hub', section_html) or re.search(r'<a\s[^>]*class="[^"]*hub[^"]*"[^>]*href="([^"]+)"', section_html)
        # href extraction: find hub's open tag just before body
        nm = re.search(r'<div class="num">(.*?)</div>', body, flags=re.S)
        hm = re.search(r'<h3[^>]*>(.*?)</h3>', body, flags=re.S)
        pm = re.search(r'<p[^>]*>(.*?)</p>', body, flags=re.S)
        am = re.search(r'<span class="arr">(.*?)</span>', body, flags=re.S)
        tiles.append({
            "href": "",  # will be filled below
            "num": extract_inner(nm.group(1)) if nm else "",
            "title": extract_inner(hm.group(1)) if hm else "",
            "description": extract_inner(pm.group(1)) if pm else "",
            "arrow": extract_inner(am.group(1)) if am else "",
        })
    # Fill hrefs by matching in order
    hrefs = re.findall(r'<a\s+class="hub"\s+href="([^"]+)"', section_html)
    for i, h in enumerate(hrefs):
        if i < len(tiles):
            tiles[i]["href"] = h
    return tiles


def extract_industries(section_html: str) -> list:
    out = []
    bodies = extract_balanced(section_html, "a", "ind")
    hrefs = re.findall(r'<a\s+href="([^"]+)"\s+class="ind">', section_html)
    for i, body in enumerate(bodies):
        im = re.search(r'<div class="icon">(.*?)</div>', body, flags=re.S)
        hm = re.search(r'<h4[^>]*>(.*?)</h4>', body, flags=re.S)
        pm = re.search(r'<p[^>]*>(.*?)</p>', body, flags=re.S)
        out.append({
            "icon": extract_inner(im.group(1)) if im else "",
            "title": extract_inner(hm.group(1)) if hm else "",
            "description": extract_inner(pm.group(1)) if pm else "",
            "href": hrefs[i] if i < len(hrefs) else "",
        })
    return out


def extract_cases(section_html: str) -> list:
    out = []
    for body in extract_balanced(section_html, "div", "case"):
        def g(cls):
            mm = re.search(rf'<div class="{cls}">(.*?)</div>', body, flags=re.S)
            return extract_inner(mm.group(1)) if mm else ""
        pm = re.search(r'<p\s+class="desc">(.*?)</p>', body, flags=re.S)
        out.append({
            "industry": g("ind"),
            "brand": g("brand"),
            "metric": g("metric"),
            "description": extract_inner(pm.group(1)) if pm else "",
        })
    return out


def extract_blog_posts(section_html: str) -> list:
    out = []
    bodies = extract_balanced(section_html, "a", "post")
    hrefs = re.findall(r'<a class="post"\s+href="([^"]+)">', section_html)
    for i, body in enumerate(bodies):
        km = re.search(r'<div class="kind">(.*?)</div>', body, flags=re.S)
        hm = re.search(r'<h3[^>]*>(.*?)</h3>', body, flags=re.S)
        rm = re.search(r'<div class="r">(.*?)</div>', body, flags=re.S)
        out.append({
            "href": hrefs[i] if i < len(hrefs) else "",
            "kicker": extract_inner(km.group(1)) if km else "",
            "title": extract_inner(hm.group(1)) if hm else "",
            "cta": extract_inner(rm.group(1)) if rm else "",
        })
    return out


def extract_prices(section_html: str) -> list:
    out = []
    for body in extract_balanced(section_html, "div", "price"):
        h = re.search(r'<h3[^>]*>(.*?)</h3>', body, flags=re.S)
        v = re.search(r'<div class="val">(.*?)</div>', body, flags=re.S)
        f = re.search(r'<p class="for">(.*?)</p>', body, flags=re.S)
        items = [extract_inner(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", body, flags=re.S)]
        out.append({
            "name": extract_inner(h.group(1)) if h else "",
            "price": extract_inner(v.group(1)) if v else "",
            "for_whom": extract_inner(f.group(1)) if f else "",
            "features": items,
        })
    return out


def extract_breadcrumb(html: str) -> str:
    m = re.search(r'<nav class="crumbs">(.*?)</nav>', html, flags=re.S)
    if not m:
        return ""
    return re.sub(r"\s+", " ", extract_inner(m.group(1))).strip()


def identify_block_type(section: dict, section_html: str) -> str:
    """Heuristically identify block type by markers."""
    c = section["classes"]
    heading = (section["heading"] or "").lower()
    eyebrow = (section["eyebrow"] or "").lower()

    if "hero" in c:
        return "hero"
    if "finalcta" in c:
        return "final_cta"
    if "red" in c and '<div class="kpi">' in section_html:
        return "kpi"
    if "dark" in c and '<div class="vs">' in section_html:
        return "problem_solution"
    if '<div class="qform">' in section_html:
        return "quick_form"
    if '<div class="logos">' in section_html and '<div class="testi">' in section_html:
        return "testimonials"
    if '<div class="logos">' in section_html:
        return "logos_strip"
    if '<div class="cases">' in section_html:
        return "cases"
    if '<div class="industries">' in section_html:
        return "industries"
    if '<div class="quiz"' in section_html:
        return "quiz"
    if '<div class="faq">' in section_html:
        return "faq"
    if '<div class="blog">' in section_html:
        return "blog_cards"
    if '<div class="prices">' in section_html:
        return "pricing"
    if '<ul class="deliv"' in section_html:
        return "deliverables"
    if '<ol class="num-list"' in section_html:
        return "num_list"
    if '<div class="process"' in section_html:
        return "process"
    if '<div class="seo-prose"' in section_html:
        return "seo_prose"
    if '<div class="catalog-grid">' in section_html:
        return "catalog"
    if '<div class="about-grid">' in section_html:
        return "about_block"
    if '<div class="hub-tiles">' in section_html:
        return "hub_tiles"
    if '<div class="vs-diy">' in section_html:
        return "vs_diy"
    if '<div class="vs">' in section_html:
        return "problem_solution"
    if '<div class="cmp">' in section_html or '<table class="compare">' in section_html:
        return "comparison_table"
    if '<div class="grid-' in section_html and '<div class="card">' in section_html:
        return "grid_cards"
    if '<div class="grid-2' in section_html:
        return "grid_cards_2"
    if re.search(r'<h2[^>]*>', section_html) and '<p' in section_html:
        return "text_section"
    return "other"


# ─── Rendering markdown ───

def render_block_md(section: dict, section_html: str) -> str:
    btype = identify_block_type(section, section_html)
    lines = []

    eyebrow_line = f"**Eyebrow:** {section['eyebrow']}" if section["eyebrow"] else ""
    h_lvl = (section["heading_level"] or "h2").upper()
    heading_line = f"**{h_lvl}:** {section['heading']}" if section["heading"] else ""

    # ── Hero ──
    if btype == "hero":
        lines.append(f"### Блок · Hero")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        # Subtitle
        sub = re.search(r'<p class="sub">(.*?)</p>', section_html, flags=re.S)
        if sub:
            lines.append(f"\n**Subtitle:** {extract_inner(sub.group(1))}")
        # CTAs
        ctas = extract_ctas(re.search(r'<div class="hero-cta">(.*?)</div>', section_html, flags=re.S).group(1)) if re.search(r'<div class="hero-cta">', section_html) else []
        if ctas:
            lines.append(f"\n**CTAs:**")
            for cta in ctas:
                lines.append(f"- `{cta['href']}` — «{cta['text']}»")
        chips = extract_trust_chips(section_html)
        if chips:
            lines.append(f"\n**Trust markers:** {' · '.join(chips)}")
        lines.append(f"\n**SVG illustration:** line-art (див. `structure-for-designer.md` §3.2 для опису)")
        return "\n".join(lines)

    # ── Quick form ──
    if btype == "quick_form":
        lines.append(f"### Блок · Швидка форма")
        f = extract_form(section_html)
        if f.get("heading"): lines.append(f"**Заголовок:** {f['heading']}")
        if f.get("hint"): lines.append(f"**Hint-текст:** {f['hint']}")
        if f.get("fields"):
            lines.append(f"**Поля форми:** {', '.join(f['fields'])}")
        if f.get("buttons"):
            lines.append(f"**Кнопка:** {f['buttons'][0]}")
        return "\n".join(lines)

    # ── Problem / solution ──
    if btype == "problem_solution":
        lines.append(f"### Блок · Проблема → Рішення (темна / cream)")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        # Both columns
        cols = re.findall(r'<div class="vs-col\s+(bad|good)(?:\s+[^"]*)?"[^>]*>(.*?)</div>\s*(?=<div class="vs-col|</div>)', section_html, flags=re.S)
        cols_light = re.findall(r'<div class="vs-col-light(?:\s+[^"]*)?"[^>]*>(.*?)</div>', section_html, flags=re.S)
        for kind, body in cols:
            hh = re.search(r'<h4[^>]*>(.*?)</h4>', body, flags=re.S)
            lis = re.findall(r'<li[^>]*>(.*?)</li>', body, flags=re.S)
            lines.append(f"\n**Колонка «{extract_inner(hh.group(1)) if hh else kind.upper()}»:**")
            for li in lis:
                lines.append(f"- {extract_inner(li)}")
        for body in cols_light:
            hh = re.search(r'<h4[^>]*>(.*?)</h4>', body, flags=re.S)
            lis = re.findall(r'<li[^>]*>(.*?)</li>', body, flags=re.S)
            lines.append(f"\n**Колонка «{extract_inner(hh.group(1)) if hh else 'Колонка'}»:**")
            for li in lis:
                lines.append(f"- {extract_inner(li)}")
        return "\n".join(lines)

    # ── KPI ──
    if btype == "kpi":
        lines.append(f"### Блок · KPI-смужка (червона)")
        items = extract_kpi(section_html)
        for it in items:
            lines.append(f"- **{it['value']}** — {it['label']}")
        return "\n".join(lines)

    # ── Grid cards ──
    if btype in ("grid_cards", "grid_cards_2"):
        lines.append(f"### Блок · {section['eyebrow'] or 'Картки'}")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        cards = extract_cards(section_html)
        for i, c in enumerate(cards, 1):
            num = c.get("num") or f"{i:02d}"
            title = c.get("title", "")
            lines.append(f"\n**{num}. {title}**")
            for p in c.get("body", []):
                lines.append(p)
            if c.get("items"):
                for it in c["items"]:
                    lines.append(f"- {it}")
            if c.get("more"):
                lines.append(f"_«{c['more']}»_")
        return "\n".join(lines)

    # ── Process ──
    if btype == "process":
        lines.append(f"### Блок · Процес (timeline)")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        steps = extract_process_steps(section_html)
        for s in steps:
            lines.append(f"\n**{s['num']} · {s['title']}** _({s['time']})_")
            if s["description"]:
                lines.append(s["description"])
        return "\n".join(lines)

    # ── Deliverables ──
    if btype == "deliverables":
        lines.append(f"### Блок · Що ви отримаєте (deliverables)")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        items = extract_deliverables(section_html)
        for i in items:
            lines.append(f"\n**→ {i['title']}**\n{i['description']}")
        return "\n".join(lines)

    # ── SEO prose ──
    if btype == "seo_prose":
        lines.append(f"### Блок · SEO-проза")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        # Extract paragraphs inside .seo-prose
        m = re.search(r'<div class="seo-prose"[^>]*>(.*?)</div>', section_html, flags=re.S)
        if m:
            for p in re.findall(r'<p[^>]*>(.*?)</p>', m.group(1), flags=re.S):
                lines.append(f"\n{extract_inner(p)}")
        return "\n".join(lines)

    # ── Numbered list ──
    if btype == "num_list":
        lines.append(f"### Блок · Нумерований SEO-список")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        # Lead paragraph if present
        lead = re.search(r'<p class="lead"[^>]*>(.*?)</p>', section_html, flags=re.S)
        if lead:
            lines.append(f"\n**Вступ:** {extract_inner(lead.group(1))}")
        items = extract_num_list(section_html)
        for i, it in enumerate(items, 1):
            lines.append(f"\n**{i}. {it['title']}**")
            if it["description"]:
                lines.append(it["description"])
        # Trailing lead-paragraph (conclusion)
        lead_paras = re.findall(r'<p class="lead"[^>]*>(.*?)</p>', section_html, flags=re.S)
        if len(lead_paras) > 1:
            lines.append(f"\n**Висновок:** {extract_inner(lead_paras[-1])}")
        return "\n".join(lines)

    # ── Testimonials ──
    if btype == "testimonials":
        lines.append(f"### Блок · Клієнти та відгуки")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        logos = extract_logos(section_html)
        if logos:
            lines.append(f"\n**Логотипи:** {' · '.join(logos)}")
        tests = extract_testimonials(section_html)
        for t in tests:
            lines.append(f"\n**«{t['quote_title']}»**\n{t['quote_body']}\n_— {t['author']}_")
        # Footer link
        fm = re.search(r'<p\s+style="margin-top:24px[^"]*">(.*?)</p>', section_html, flags=re.S)
        if fm:
            lines.append(f"\n**Під блоком:** {extract_inner(fm.group(1))}")
        return "\n".join(lines)

    # ── Logos strip ──
    if btype == "logos_strip":
        lines.append(f"### Блок · Стрічка логотипів")
        logos = extract_logos(section_html)
        lines.append(f"**Логотипи:** {' · '.join(logos)}")
        return "\n".join(lines)

    # ── Quiz ──
    if btype == "quiz":
        lines.append(f"### Блок · Калькулятор (quiz)")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        steps = extract_quiz(section_html)
        for s in steps:
            lines.append(f"\n**Крок {s['step']}.** {s['question']}")
            for opt in s["options"]:
                lines.append(f"- {opt}")
        # Contact step
        cm = re.search(r'<div class="quiz-step"[^>]*data-step="5">(.*?)(?=<div class="quiz-step|</div>\s*</div>)', section_html, flags=re.S)
        if cm:
            body = cm.group(1)
            hh = re.search(r'<h3[^>]*>(.*?)</h3>', body, flags=re.S)
            pls = re.findall(r'placeholder="([^"]+)"', body)
            mm = re.search(r'<span class="quiz-micro">(.*?)</span>', body, flags=re.S)
            btn = re.search(r'<button[^>]*>(.*?)</button>', body, flags=re.S)
            if hh: lines.append(f"\n**Фінальний крок:** {extract_inner(hh.group(1))}")
            if pls: lines.append(f"**Поля:** {', '.join(pls)}")
            if mm: lines.append(f"**Microcopy:** _{extract_inner(mm.group(1))}_")
            if btn: lines.append(f"**Кнопка:** «{extract_inner(btn.group(1))}»")
        return "\n".join(lines)

    # ── FAQ ──
    if btype == "faq":
        lines.append(f"### Блок · FAQ")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        for i, q in enumerate(extract_faq(section_html), 1):
            lines.append(f"\n**Q{i}.** {q['question']}")
            lines.append(f"**A:** {q['answer']}")
        return "\n".join(lines)

    # ── Blog cards ──
    if btype == "blog_cards":
        lines.append(f"### Блок · Дотичні матеріали (блог-картки)")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        for p in extract_blog_posts(section_html):
            lines.append(f"\n**[{p['kicker']}]** {p['title']}  \n→ `{p['href']}`")
        # Blog-foot
        bf = re.search(r'<div class="blog-foot">(.*?)</div>', section_html, flags=re.S)
        if bf:
            lines.append(f"\n**Під блоком:** {extract_inner(bf.group(1))}")
        return "\n".join(lines)

    # ── Pricing ──
    if btype == "pricing":
        lines.append(f"### Блок · Тарифи")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        for p in extract_prices(section_html):
            lines.append(f"\n**{p['name']}** · {p['price']}")
            lines.append(f"_{p['for_whom']}_")
            for f in p["features"]:
                lines.append(f"- {f}")
        ctas = extract_ctas(section_html)
        rel_ctas = [c for c in ctas if "tarify.html" in c["href"]]
        if rel_ctas:
            lines.append(f"\n**CTA під блоком:** «{rel_ctas[0]['text']}» → `{rel_ctas[0]['href']}`")
        return "\n".join(lines)

    # ── Cases ──
    if btype == "cases":
        lines.append(f"### Блок · Кейси")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        for c in extract_cases(section_html):
            lines.append(f"\n**[{c['industry']}] {c['brand']} · {c['metric']}**")
            lines.append(c["description"])
        return "\n".join(lines)

    # ── Industries ──
    if btype == "industries":
        lines.append(f"### Блок · Галузі")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        for i in extract_industries(section_html):
            lines.append(f"\n**[{i['icon']}] {i['title']}** — {i['description']}")
        return "\n".join(lines)

    # ── Final CTA ──
    if btype == "final_cta":
        lines.append(f"### Блок · Фінальний CTA (темна / червона)")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        ps = extract_paragraphs(section_html)
        if ps:
            lines.append(f"\n{ps[0]}")
        ctas = extract_ctas(section_html)
        for c in ctas:
            lines.append(f"- `{c['href']}` — «{c['text']}»")
        return "\n".join(lines)

    # ── Catalog ──
    if btype == "catalog":
        lines.append(f"### Блок · Повний каталог послуг")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        for col in extract_catalog_cols(section_html):
            lines.append(f"\n**{col['heading']}:**")
            for it in col["items"]:
                lines.append(f"- {it['text']} → `{it['href']}`")
        return "\n".join(lines)

    # ── About (home) ──
    if btype == "about_block":
        lines.append(f"### Блок · Про компанію (home-variant)")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        m = re.search(r'<div class="about-intro">(.*?)</div>', section_html, flags=re.S)
        if m:
            for p in re.findall(r'<p[^>]*>(.*?)</p>', m.group(1), flags=re.S):
                lines.append(f"\n{extract_inner(p)}")
        m = re.search(r'<div class="about-stats">(.*?)</div>', section_html, flags=re.S)
        if m:
            lines.append(f"\n**Stat-картки:**")
            for st in re.finditer(r'<div class="v">(.*?)</div>\s*<div class="l">(.*?)</div>', m.group(1), flags=re.S):
                lines.append(f"- **{extract_inner(st.group(1))}** — {extract_inner(st.group(2))}")
        return "\n".join(lines)

    # ── Hub tiles (home/trainings) ──
    if btype == "hub_tiles":
        lines.append(f"### Блок · 3 hub-картки")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        for t in extract_hub_tiles(section_html):
            lines.append(f"\n**{t['num']} · {t['title']}** → `{t['href']}`")
            if t["description"]:
                lines.append(t["description"])
            if t["arrow"]:
                lines.append(f"_{t['arrow']}_")
        return "\n".join(lines)

    # ── VS-DIY (home) ──
    if btype == "vs_diy":
        lines.append(f"### Блок · «Чому не самостійно?» (2-колонкове порівняння + inline-форма)")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        for m in re.finditer(r'<div class="vs-col-light(?:\s+[^"]*)?"[^>]*>(.*?)</div>\s*(?=<div class="vs-col-light|<div class="vs-diy-cta")', section_html, flags=re.S):
            body = m.group(1)
            hh = re.search(r'<h4[^>]*>(.*?)</h4>', body, flags=re.S)
            lines.append(f"\n**Колонка «{extract_inner(hh.group(1)) if hh else ''}»:**")
            for li in re.findall(r'<li[^>]*>(.*?)</li>', body, flags=re.S):
                lines.append(f"- {extract_inner(li)}")
        # CTA form
        cm = re.search(r'<div class="vs-diy-cta">(.*?)</div>', section_html, flags=re.S)
        if cm:
            body = cm.group(1)
            ps = re.findall(r'<p(?:\s+[^>]*)?>(.*?)</p>', body, flags=re.S)
            if ps:
                lines.append(f"\n**Під порівнянням:** {extract_inner(ps[0])}")
            pls = re.findall(r'placeholder="([^"]+)"', body)
            if pls:
                lines.append(f"**Поля форми:** {', '.join(pls)}")
            btn = re.search(r'<button[^>]*>(.*?)</button>', body, flags=re.S)
            if btn:
                lines.append(f"**Кнопка:** «{extract_inner(btn.group(1))}»")
            if len(ps) > 1:
                lines.append(f"**Microcopy:** _{extract_inner(ps[-1])}_")
        return "\n".join(lines)

    # ── Comparison table ──
    if btype == "comparison_table":
        lines.append(f"### Блок · Порівняльна таблиця")
        if eyebrow_line: lines.append(eyebrow_line)
        if heading_line: lines.append(heading_line)
        # Lead
        ld = re.search(r'<p class="lead"[^>]*>(.*?)</p>', section_html, flags=re.S)
        if ld:
            lines.append(f"\n{extract_inner(ld.group(1))}")
        # Table rows
        tm = re.search(r'<table[^>]*class="[^"]*(?:cmp|compare)[^"]*"[^>]*>(.*?)</table>', section_html, flags=re.S)
        if not tm:
            tm = re.search(r'<div class="cmp"[^>]*>.*?<table[^>]*>(.*?)</table>', section_html, flags=re.S)
        if tm:
            body = tm.group(1)
            headers = re.findall(r'<th[^>]*>(.*?)</th>', body, flags=re.S)
            if headers:
                lines.append("")
                lines.append("| " + " | ".join([extract_inner(h) for h in headers]) + " |")
                lines.append("|" + "---|" * len(headers))
                for row in re.finditer(r'<tr>(.*?)</tr>', body, flags=re.S):
                    cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row.group(1), flags=re.S)
                    if cells and cells != headers:
                        lines.append("| " + " | ".join([extract_inner(c) for c in cells]) + " |")
        # Conclusion
        cc = re.search(r'<p class="compare-concl"[^>]*>(.*?)</p>', section_html, flags=re.S)
        if cc:
            lines.append(f"\n**Висновок:** {extract_inner(cc.group(1))}")
        return "\n".join(lines)

    # ── Generic / fallback ──
    lines.append(f"### Блок · {section['eyebrow'] or section['heading'] or '(без заголовка)'}")
    if eyebrow_line: lines.append(eyebrow_line)
    if heading_line: lines.append(heading_line)
    ps = extract_paragraphs(section_html)
    for p in ps[:10]:
        if p.strip():
            lines.append(f"\n{p}")
    return "\n".join(lines)


def count_words(html: str) -> int:
    t = re.sub(r'<(script|style|svg)[^>]*>.*?</\1>', '', html, flags=re.S)
    return len(strip_tags(t).split())


def render_page_md(filename: str, title: str, breadcrumb: str, category: str) -> str:
    path = RACIO_DIR / filename
    if not path.exists():
        return f"# {title}\n\n⚠ Файл `{filename}` не знайдено.\n"

    html = path.read_text(encoding="utf-8")
    meta = extract_meta(html)
    crumb = extract_breadcrumb(html)
    wc = count_words(html)

    lines = [
        f"# {title}",
        "",
        f"**Файл:** `{filename}`  ",
        f"**Шлях від головної:** {breadcrumb}  ",
        f"**Поточний обсяг тексту:** {wc} слів  ",
    ]
    # Status flag
    if wc < 800:
        lines.append("**⚠ Статус:** тонка сторінка — потребує розгортання за ТЗ")
    else:
        lines.append("**✅ Статус:** повний лендинг")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Метадані")
    lines.append("")
    lines.append(f"- **Title tag:** {meta['title_tag']}")
    lines.append(f"- **Meta description:** {meta['meta_description']}")
    if crumb:
        lines.append(f"- **Breadcrumb на сторінці:** {crumb}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Структура й копі")
    lines.append("")

    sections = find_sections(html)
    for i, (idx, sec_html) in enumerate(sections, 1):
        sec = classify_section(sec_html)
        lines.append(f"---")
        lines.append("")
        lines.append(f"#### Секція {i}/{len(sections)}" + (f" · bg: `{sec['bg']}`" if sec['bg'] != 'default' else ""))
        lines.append("")
        block_md = render_block_md(sec, sec_html)
        lines.append(block_md)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("_Кінець сторінки._")

    return "\n".join(lines)


def main():
    DOCS_COPY.mkdir(parents=True, exist_ok=True)
    summary_rows = []
    for i, (fname, title, breadcrumb, category) in enumerate(PAGES, 1):
        outname = f"{i:02d}-{fname.replace('.html', '.md')}"
        md = render_page_md(fname, title, breadcrumb, category)
        (DOCS_COPY / outname).write_text(md, encoding="utf-8")
        path = RACIO_DIR / fname
        wc = count_words(path.read_text(encoding="utf-8")) if path.exists() else 0
        summary_rows.append((i, title, fname, breadcrumb, wc, outname))
        print(f"{i:2d}. {fname:45s} → {outname}")
    print("\nDone.")
    return summary_rows


if __name__ == "__main__":
    main()
