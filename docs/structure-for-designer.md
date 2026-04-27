# RACIO — структура сайту для дизайнера

**Версія:** 2026-04-25 · **Структура затверджена**
**Покриття:** 23 сторінки, 1 затверджений 13-блоковий шаблон сервісної сторінки, глобальні компоненти
**Live preview:** https://candid-profiterole-017286.netlify.app/
**GitHub repo:** https://github.com/ratiy/racio-site (public)

Документ описує **інформаційну архітектуру**. Типографіка, кольори, spacing — у design-system / Figma.

---

## 1. Sitemap

```
/
├── index.html                               — Головна (18 блоків)
│
├── /ohorona-pratsi/                          (категорія — dropdown, без landing)
│   ├── /autsorsynh/                         — Аутсорсинг ОП
│   ├── /audit/                              — Аудит ОП
│   ├── /dokumentatsiia/                     — Розробка документації ОП
│   ├── /pakety-dokumentiv/                  — Пакети документів ОП
│   ├── /treningy-z-op/                      — Тренінги з ОП
│   ├── /rozsliduvannia-nv/                  — Розслідування НВ (24/7 emergency)
│   └── /suprovid-derzhpratsi/               — Супровід Держпраці
│
├── /pozhezhna-bezpeka/                       (категорія — dropdown)
│   ├── /autsorsynh/                         — Аутсорсинг ПБ
│   ├── /audit/                              — Аудит ПБ
│   ├── /dokumentatsiia/                     — Документація ПБ (merged 3-tier)
│   ├── /treningy-z-pb/                      — Тренінги з ПБ
│   └── /deklaratsiia-dsns/                  — Декларація ДСНС (+ Замір опору ізоляції секція)
│
├── /keruvannia-ryzykamy/                     (категорія — dropdown)
│   ├── /otsinka-ryzykiv/                    — Оцінка ризиків
│   ├── /tsyvilnyi-zakhyst/                  — Цивільний захист
│   └── /treningy-z-bezpeky-pratsi/          — Тренінги з безпеки праці
│
├── /pro-nas/                                 (категорія — dropdown, 4 пункти)
│   ├── /pro-kompaniyu/                      — Про компанію (з RSS-секцією id="rss")
│   ├── /kliyenty-ta-keysu/                  — Клієнти та кейси
│   ├── /halusi/                             — Галузі (8 industries)
│   └── /kontakty/                           — Контакти
│
├── /blog/                                    — Блог (рубрикатор)
│   └── /koryisne/                           — Корисне (шаблони/чек-листи)
│
└── [footer-only «Ще»]
    ├── /tarify/                             — Тарифи
    └── /pro-kompaniyu/#rss                  — RACIO Safety Standard (anchor)

Всього: 23 окремих HTML.
```

---

## 2. Глобальні компоненти

### 2.1 Header (nav)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [LOGO]  [Охорона праці ▾] [Пожежна безпека ▾] [Керування ризиками ▾]          │
│         [Про нас ▾] [Блог ▾]              [+380 ...] [UA|EN] [primary CTA →]  │
└──────────────────────────────────────────────────────────────────────────────┘
```

**5 dropdown-меню:**
- Охорона праці — 7 пунктів
- Пожежна безпека — 5 пунктів
- Керування ризиками — 3 пункти
- Про нас — 4 пункти (Про компанію · Клієнти та Кейси · Галузі · Контакти)
- Блог — 2 пункти

**Mobile:** burger → overlay drawer з усіма dropdown як collapsed `<details>`.

### 2.2 Footer

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [LOGO + ISO + адреса] [ОП·7] [ПБ·5+К.Р.·3]              [Про нас·4]            │
│                                                          [Ще·2: Тарифи · RSS]  │
│                                                          [Блог·2]              │
├──────────────────────────────────────────────────────────────────────────────┤
│ [Телефон] [Email] [Адреса] [Графік]                                            │
├──────────────────────────────────────────────────────────────────────────────┤
│ © 2026 RACIO  [Політика] [Cookies] [Договір] [Мапа]   [LinkedIn][FB][YouTube]  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Sticky mobile CTA

Фіксована знизу на mobile — кнопка primary «Отримати прорахунок →» до `#quiz`.

---

## 3. Затверджений шаблон сервісної сторінки — 13 блоків

**Всі 15 сервісних сторінок** слідують цьому шаблону з мінімальними варіаціями. **Структура зафіксована 25.04.2026.**

```
┌─ 1.  Breadcrumb · «Головна › Категорія › Поточна»
│
├─ 2.  HERO  (split 60/40, beige bg)
│       ├─ Ліва: eyebrow + H1 (з <em> italic) + sub + 2 CTAs (primary + ghost) + 3 trust-chips
│       └─ Права: line-art SVG hero (унікальний на кожну сторінку)
│
├─ 3.  SEO ОПИС ПОСЛУГИ  (cream bg, 2-колонкова сітка) ← новий стандарт
│       ├─ Ліва card: H2 (caps) + lead-параграф + CTA «Замовити консультацію»
│       └─ Права: 3-5 параграфів прози (для копірайтера)
│       ↳ Замінює: колишній SEO-A intro + Quick form (обидва видалені)
│
├─ 4.  Service grid (default beige)
│       ├─ Sec-head
│       └─ 6 cards (numbered 01-06): «Що входить» / «Команда в дорозі» / «3 формати» (варіює)
│
├─ 5.  Для кого / Коли  (cream, 2 cards)  ← на більшості сторінок
│       ├─ Card 1: «Для кого» (list з → bullets)
│       └─ Card 2: «Коли замовляти»
│       ↳ Per-page варіації:
│           • pakety-dokumentiv  → «Коли пакет, а коли індивідуалка»
│           • dokumentatsiia-pb  → «Який формат підійде вам» (3-tier cards)
│           • deklaratsiia-dsns  → «Кому обов'язково подавати» (ПОТРІБНА / НЕ ПОТРІБНА)
│           • rozsliduvannia-nv  → «Коли потрібен супровід НВ» (numbered, для emergency)
│
├─ 6.  Problem/Solution VS  (dark bg) — опційно
│       └─ 2 col: «Без нас» (червоні —) vs «З RACIO» (бежеві ✓)
│
├─ 7.  Process · timeline  (default beige)
│       └─ 4-5 horizontal steps з num + title + time + опис
│
├─ 8.  Deliverables  (cream bg)
│       └─ Vertical list з → arrow + H4 + опис (до 6 пунктів)
│
├─ 9.  SEO-B numbered list  (default beige)  ← унікальна цінність
│       ├─ Sec-head + lead-вступ
│       ├─ 5-8 пунктів з Playfair italic цифрами
│       └─ Lead-висновок
│       ↳ Приклади: «8 типових порушень», «7 категорій ризиків», «6 типових сценаріїв»
│
├─ 10. (опційно) KPI strip / pricing-deep / спеціальний компонент
│       ↳ audit.html       → «Скільки коштує аудит» (pricing prose)
│       ↳ deklaratsiia-dsns → «Замір опору ізоляції — елемент декларації»
│       ↳ autsorsynh-pb    → KPI strip
│
├─ 11. Testimonials  (cream або default)
│       ├─ Sec-head
│       ├─ Logos strip (8 brand-name spans)
│       ├─ 2 testimonial cards (italic H3 quote + body + author)
│       └─ Footer-link на /kliyenty-ta-keysu/
│
├─ 12. Quiz / Calculator  (cream bg, id="quiz")
│       ├─ Progress bar
│       └─ 5-step wizard: 4 контентні питання + крок 5 з contact fields
│
├─ 13. FAQ  (default beige, max-width 880px)
│       └─ 6-10 details/summary з + / × toggle, з inline-посиланнями у відповідях
│
├─ 14. Blog cards  (cream)
│       ├─ Sec-head
│       └─ 3 cards: kicker (caps red) + H3 + «Читати →»
│
└─ 15. Final CTA  (dark або red bg)
        ├─ Sec-head center
        ├─ H2 з <em> + 1 коротке речення
        └─ 2 кнопки (primary + ghost)
```

**На рівні CTA-точок:** 4 momentum-зони на сторінці = Hero (2 кнопки) → SEO desc (1 кнопка) → Quiz (форма-калькулятор) → Final CTA (2 кнопки). **Без зайвих proximity-конфліктів.**

### 3.1 Hero SVG — спільний стиль

- Viewport: **600 × 600**
- Stroke: `#0A0A0A`, `stroke-width: 1.6`, `linecap: round`, `linejoin: round`
- Fill accent: `#E8DCC4` (beige) або `#FAF6EC` (cream)
- Color accent: `#A63737` (red — для штампів, бейджів, акцентів)
- Бренд-маркер «RACIO» дрібно вмонтовано в одну деталь
- Ground reference dashed line знизу
- Текст у SVG: Manrope (labels), Playfair Display italic (emphasis)

**Унікальні предмети** на кожну сервісну (по фазі 3):
- Аутсорсинг ОП → класична каска з RACIO-бейджем
- Аудит ОП → планшет з AUDIT звітом + лупа + MOCK-штамп
- Документація → стос документів + ЗАТВЕРДЖЕНО + перо
- Пакети → ряд папок з галузевими tabs + READY-штамп
- Тренінги ОП → дошка з топіками + групка учасників
- Розслідування НВ → годинник з 24/7-бейджем + календар
- Супровід Держпраці → ваги + щит + документи
- Аутсорсинг ПБ → будівля з планом евакуації + вогнегасник + ДСНС-значок
- Аудит ПБ → планшет з fire checklist + MOCK-штамп
- Документація ПБ → план евакуації на стіні + ЗАТВЕРДЖЕНО
- Тренінги ПБ → людина з вогнегасником + полум'я + EXIT
- Декларація ДСНС → двері з замком + ДСНС ✓ табличка
- Оцінка ризиків → матриця 5×5 з heat-map
- Цивільний захист → будівля з укриттям + тривога
- Тренінги безпеки → медитуюча фігура + концентричні кола + heart-rate

---

## 4. Сторінки — унікальна структура

### 4.1 Головна (`index.html`) — 18 блоків

```
1.  Hero (triptych SVG: каска + вогнегасник + планшет)
2.  Brand-line (ISO + stats одним рядком, caps)
3.  Logos strip
4.  «Хто такі RACIO» (про компанію, grid 1.3/1 + 3 stat-cards)
5.  4 напрями (grid-4: ОП/ПБ/К.Р./Тренінги)
6.  Problem → Solution (dark, .vs)
7.  KPI strip (red, 4 metrics)
8.  Тарифи (3 pricing cards + CTA «Порівняти всі пакети →»)
9.  Повний каталог (3 колонки: ОП 7 / ПБ 5 / К.Р. 3)
10. Process (4 steps)
11. Галузі (4×2 grid 8 карток + CTA «Клієнти та кейси →»)
12. Тренінги-хаби (3 cards)
13. Кейси (4 картки + CTA «Всі кейси →»)
14. FAQ (6 топ-питань)
15. Чому не самостійно? (2 колонки + inline lead-форма)
16. Quiz (калькулятор)
17. Блог (3 picked articles)
18. Final CTA (dark)
```

### 4.2 Про компанію (`pro-kompaniyu.html`) — 12 блоків

```
1.  Hero (badge SVG)
2.  SEO intro «Що робить RACIO різним»
3.  Timeline 2012-2026 (8 років)
4.  Команда (8 members + 8 більше)
5.  Methodology «Як ми працюємо з клієнтом»
6.  Values (4 принципи)
7.  Licenses (6 awards)
8.  KPI strip (red)
9.  RSS секція з id="rss" (RACIO Safety Standard)
10. Partners / memberships (6 card-cards)
11. FAQ
12. Final CTA
```

### 4.3 Клієнти та кейси (`kliyenty-ta-keysu.html`) — 11 блоків

```
1.  Hero (trophy SVG)
2.  KPI strip
3.  Logo wall (24 brands)
4.  SEO methodology «Як читати ці кейси»
5.  3 featured cases (повний writeup кожен: AstraZeneca · Glovo · Edem)
6.  9 highlight metrics (cases short)
7.  6 testimonials
8.  Industries cross-section (8 cards)
9.  FAQ (6 items)
10. Final CTA
```

### 4.4 Галузі (`halusi.html`) — 9 блоків

```
1.  Hero
2.  SEO intro «Чому 8 галузей — 8 різних продуктів»
3.  8 industry cards (grid-2, deep info: НПАОП + клієнти + досвід)
4.  SEO numbered list «6 речей, які робимо інакше»
5.  Comparison table (галузь × специфіка × виклик × стартова послуга)
6.  3 featured cases
7.  FAQ
8.  Final CTA
```

### 4.5 Тарифи (`tarify.html`) — 13 блоків

```
1.  Hero (3 boxes SVG)
2.  SEO intro «Логіка START / SMART / FULL»
3.  8 tabs (по категоріях послуг) — кожен з .prices grid
4.  Comparison matrix (13 параметрів × 3 пакети)
5.  Galuzevi nadbavky (SEO prose)
6.  Quiz
7.  Discounts (8 cards)
8.  «Що не входить» (6 окремих платних)
9.  FAQ (8 items)
10. Final CTA
```

### 4.6 Контакти (`kontakty.html`) — мінімалістична

```
1.  Hero
2.  Contacts grid (телефон + email + адреса + графік)
3.  Form
4.  (опц.) карта
5.  Final CTA
```

### 4.7 Блог (`blog.html`) і Корисне (`koryisne.html`) — рубрикатори

```
1.  Hero
2.  Category filters
3.  Featured article / material
4.  Articles / Materials grid
5.  Pagination
6.  Newsletter signup
7.  Final CTA
```
Статті як окремі URL — поза scope цього документа.

---

## 5. Повторювані UI-компоненти (CSS classes у `racio.css`)

| Клас | Призначення |
|---|---|
| `.container` | Max-width wrapper з padding |
| `.hero-grid` | 60/40 split для hero |
| `.sec-head` | Section header (eyebrow + h2 з italic) |
| `.grid-2/.grid-3/.grid-4` | Стандартні grid layouts |
| `.card` | Стандартна картка (white bg, num red italic) |
| `.cream/.dark/.red` | Section background modifiers |
| **`.seo-desc/.seo-desc-card/.seo-desc-text`** | **Новий блок «Опис послуги»** (2-колонкова) |
| `.vs/.vs-col.bad/.vs-col.good` | Dark 2-col порівняння (problem/solution) |
| `.vs-col-light/.vs-diy` | Light 2-col порівняння (home «не самостійно») |
| `.process/.step` | Horizontal timeline |
| `.deliv` | Vertical list з → arrows |
| `.num-list` | Numbered SEO list (Playfair italic цифри) |
| `.compare/.cmp` | Comparison tables |
| `.kpi` | Red metric strip |
| `.logos/.testi` | Trust indicators |
| `.quiz/.quiz-step` | 5-step wizard |
| `.faq` + `<details>` | Accordion |
| `.blog/.post` | Blog cards |
| `.catalog-grid/.catalog-col` | Home full catalog (3 cols) |
| `.about-grid/.about-stats` | Home about + stats |
| `.hub-tiles/.hub` | 3-card category selectors |
| `.industries/.ind` | 4×2 industry grid |
| `.prices/.price` | Tariff cards (.anchor = picked) |
| `.tabs/.tab-panel` | Tab switcher (на тарифах) |
| `.timeline/.tl-item/.tl-year` | History timeline (про компанію) |
| `.team/.member/.avatar` | Team grid (про компанію) |
| `.awards/.award` | Licenses grid |
| `.cases/.case` | Cases grid |
| `.crumbs` | Breadcrumb nav |
| `.qform` | ❌ Quick form (видалено зі сервісних) |
| `.seo-prose` | SEO-A prose (видалено зі сервісних, лишилось на audit/deklaratsiia-dsns як спеціалізовані) |
| `.finalcta` | Final CTA block |

---

## 6. Кольорова палітра

- **Beige-домінанта:** `#E8DCC4` (brand bg), `#FAF6EC` (cream), `#EFE5D1` (beige-2)
- **Ink:** `#0A0A0A` (текст), `var(--muted)` `#6B6258` (приглушений)
- **Accent red:** `#A63737` (CTA, emphasis, штампи, бейджі)
- **Hairline:** `var(--line)` (тонкі розділювачі)
- **Dark sections:** `#0F0D0A` (background), `#C9B998` (accent text)

---

## 7. Типографіка

- **Manrope** 400/500/600/700 — sans-serif основа
- **Playfair Display italic** 400/500 — для `<em>` у заголовках і акцентних цифрах
- **H1:** `clamp(40px, 5vw, 72px)`, Manrope 500-600
- **H2:** `clamp(28px, 3.5vw, 48px)`
- **H3:** 20-32px (Playfair italic для деяких блоків)
- **Body:** 15-17px, line-height 1.6-1.7
- **Eyebrow:** 11-13px, caps, letter-spacing 0.14em, red

---

## 8. Мобільна адаптація

Breakpoint **≤860px**:
- `.hero-grid` → 1 колонка (SVG під текстом)
- `.grid-4 → .grid-2 → 1` колонка
- `.vs/.vs-diy/.catalog-grid/.seo-desc` → 1 колонка
- `.cases` → 1 колонка
- `.prices` → стек
- Sticky CTA з'являється знизу
- Header: dropdown → burger overlay

---

## 9. Користувацькі сценарії

1. **Organic SEO → service landing → quiz** (основний для ОП/ПБ/КР)
2. **Main nav → dropdown → service → cross-link → related** (лабіринт)
3. **Home catalog → direct landing** (для тих хто знає що шукає)
4. **Home «Хто ми → Кейси» → конкретний кейс → service** (trust-flow)
5. **Emergency: dropdown → розслідування НВ з phone-CTA** (24/7 red final CTA)

---

## 10. Статус сторінок (всі затверджені)

| Категорія | Сторінок | Статус |
|---|---:|---|
| Сервісні (15) | 15 | ✅ 13-блокова структура зафіксована |
| Головна | 1 | ✅ 18 блоків |
| Про нас (3) | 3 | ✅ pro-kompaniyu (12 бл.) · kliyenty (11 бл.) · halusi (9 бл.) |
| Контакти | 1 | ✅ мінімалістична (норма) |
| Тарифи | 1 | ✅ 13 блоків |
| Блог + Корисне | 2 | ✅ рубрикатори (наповнюватимуться статтями) |

**Всі сторінки готові до дизайн-проходу й верстки фінального макета.**

---

_Кінець документа. Тексти й копі — у `copy-for-copywriter.md`._
