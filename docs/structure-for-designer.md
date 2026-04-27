# RACIO — структура сайту для дизайнера

**Версія:** 2026-04-24
**Покриття:** 24 сторінки, 1 шаблон сервісної сторінки, глобальні компоненти
**Формат:** структурний (дерево блоків + CTA + SVG-описи). Типографіка / кольори / spacing — у design-system.

---

## 1. Sitemap

```
/
├── /ohorona-pratsi/            (категорія — dropdown, без окремої сторінки)
│   ├── /autsorsynh/            — Аутсорсинг ОП
│   ├── /audit/                 — Аудит ОП
│   ├── /dokumentatsiia/        — Розробка документації ОП
│   ├── /pakety-dokumentiv/     — Пакети документів ОП
│   ├── /treningy-z-op/         — Тренінги з ОП (hub з 5 темами)
│   ├── /rozsliduvannia-nv/     — Розслідування НВ
│   └── /suprovid-derzhpratsi/  — Супровід перевірок Держпраці
├── /pozhezhna-bezpeka/         (категорія — dropdown)
│   ├── /autsorsynh/            — Аутсорсинг ПБ
│   ├── /audit/                 — Аудит ПБ
│   ├── /dokumentatsiia/        — Документація ПБ (merged: розробка + пакети + інструкції)
│   ├── /treningy-z-pb/         — Тренінги з ПБ (hub з 2 темами)
│   └── /deklaratsiia-dsns/     — Декларація ДСНС (+ секція «Замір опору ізоляції»)
├── /keruvannia-ryzykamy/       (категорія — dropdown)
│   ├── /otsinka-ryzykiv/       — Оцінка ризиків
│   ├── /tsyvilnyi-zakhyst/     — Цивільний захист
│   └── /treningy-z-bezpeky-pratsi/ — Тренінги з безпеки праці (hub з 2 темами: Вигорання, Стрес-менеджмент)
├── /pro-nas/                   (категорія — dropdown)
│   ├── /pro-kompaniyu/         — Про компанію (з RSS-секцією)
│   ├── /kliyenty-ta-keysu/     — Клієнти та кейси
│   └── /kontakty/              — Контакти
├── /blog/                      — Блог (рубрикатор)
│   └── /koryisne/              — Корисне (шаблони, чек-листи)
└── [footer-only, не в dropdown]
    ├── /halusi/                — Галузі (20+ галузей)
    ├── /tarify/                — Тарифи (START/SMART/FULL + матриця)
    └── /rss/                   — RACIO Safety Standard
```

**Усього: 24 сторінки** (0 сторінок-рубрикаторів категорій — вони тільки як dropdown'и в меню).

---

## 2. Глобальні компоненти

### 2.1 Header (nav)

Структура (injected via `racio.js` у `<header id="site-header">`):

```
┌────────────────────────────────────────────────────────────────────────────┐
│ [LOGO "RACIO"]  [Охорона праці ▾] [Пожежна безпека ▾] [Керування ризиками ▾]│
│                  [Про нас ▾] [Блог ▾]     [+380 ... ] [UA|EN]  [CTA →]     │
└────────────────────────────────────────────────────────────────────────────┘
```

- **Logo** → `/` (головна)
- **5 dropdown-меню:**
  - ОП — 7 пунктів
  - ПБ — 5 пунктів
  - К.Р. — 3 пункти
  - Про нас — 3 пункти
  - Блог — 2 пункти
- **Праворуч:**
  - Phone link (tel:)
  - Language switcher (UA активна, EN — заглушка)
  - Primary CTA button → `#quiz` (або `#form` на сторінках-екстрених як rozsliduvannia)

**Mobile:** burger → overlay drawer з усіма dropdown як collapsed `<details>`.

### 2.2 Footer (foot)

Injected via `racio.js` у `<footer id="site-footer">`:

```
┌────────────────────────────────────────────────────────────────────────────┐
│ [LOGO + адреса]    [Охорона праці]   [Пожежна безпека]      [Про нас]       │
│                    [7 посилань]       [5 посилань +          [3 посилання]  │
│                                        Керування ризиками: 3]              │
│                                                            [Ще: 3 пункти]   │
│                                                            [Блог: 2]        │
├────────────────────────────────────────────────────────────────────────────┤
│ [Телефон] [Email] [Адреса] [Графік роботи]                                   │
├────────────────────────────────────────────────────────────────────────────┤
│ © 2026 RACIO       [Політика конф.] [Cookies] [Договір] [Мапа]  [LI][FB][YT]│
└────────────────────────────────────────────────────────────────────────────┘
```

**«Ще» (EXTRA_LINKS в racio.js):**
- Галузі → `/halusi/`
- Тарифи → `/tarify/`
- RACIO Safety Standard → `/rss/`

### 2.3 Sticky mobile CTA

Фіксована внизу на мобільних розмірах — primary button «Отримати прорахунок →» до `#quiz`.

---

## 3. Шаблон типової сервісної сторінки

Усі 15 сервісних сторінок (ОП + ПБ + К.Р. + 3 хаби тренінгів) слідують спільному шаблону з незначними відхиленнями.

### 3.1 Послідовність блоків (13-18 блоків)

```
┌─ [1]  Breadcrumb: Головна › Категорія › Поточна сторінка
│
├─ [2]  Hero (split 60/40)
│       ├─ Ліва колонка:
│       │   ├─ Eyebrow (маленька caps-стрічка з метадатою)
│       │   ├─ H1 (з <em> для italic emphasis)
│       │   ├─ Sub-headline (2-3 речення, з inline-посиланнями)
│       │   ├─ CTA pair (primary + secondary/ghost)
│       │   └─ Trust markers (3 short chips)
│       └─ Права колонка: line-art SVG 600×600 (унікальний для кожної сторінки)
│
├─ [3]  Quick form (стрічка)
│       ├─ Ліва частина: H3 + hint-текст
│       └─ Права частина: 3-4 inputs + submit button
│
├─ [4]  «Що входить» — grid-3 або grid-6
│       ├─ Sec-head: eyebrow + H2
│       └─ 6 карток з num (01-06) + H3 + короткий опис
│
├─ [5]  «Для кого · Коли» — grid-2 (cream bg)
│       ├─ Ліва: «Для кого» (list з → bullets)
│       └─ Права: «Коли замовляти» (list з → bullets)
│
├─ [6]  SEO-A prose (max-width 820px)
│       ├─ Sec-head
│       └─ 3-4 параграфи прози з вплетеними inline-лінками (labyrinth)
│
├─ [7]  Process (horizontal timeline, 4-5 кроків)
│       ├─ Sec-head
│       └─ .process grid з .step блоками (num + H3 + time + опис)
│
├─ [8]  Deliverables (vertical list з arrows, cream bg)
│       ├─ Sec-head
│       └─ .deliv ul з → іконкою + H4 + підпис
│
├─ [9]  SEO-B numbered list (5-8 items)
│       ├─ Sec-head
│       ├─ Lead-параграф
│       └─ ol.num-list: Playfair italic цифри + H4 + опис з inline-лінками
│
├─ [10] KPI strip (red section) — опційно, є на частині сторінок
│       └─ 4 великі метрики в row
│
├─ [11] Testimonials + logos (cream або default bg)
│       ├─ Sec-head
│       ├─ Logos strip (8 логотипів flex-wrap)
│       ├─ 2 testimonial cards (H3 з italic-акцентом + опис + author)
│       └─ Footer-link на «всі кейси» → /kliyenty-ta-keysu/
│
├─ [12] Quiz/calculator (5-step wizard)
│       ├─ Sec-head center
│       ├─ Progress bar зверху
│       └─ Крок 1-4: питання + кнопки варіантів; крок 5: contact fields + submit
│
├─ [13] FAQ (accordion, 6-10 items, max-width 880px)
│       ├─ Sec-head center
│       └─ details/summary з + / × toggle, відповіді з inline-лінками
│
├─ [14] Blog cards (grid-3, cream bg)
│       ├─ Sec-head
│       ├─ 3 картки: kicker (caps) + H3 + «Читати →»
│       └─ Blog-foot з inline-лінками на блог і суміжне
│
└─ [15] Final CTA (dark або red section)
        ├─ Sec-head center
        ├─ H2 з <em>
        ├─ Коротке речення
        └─ 2 кнопки (primary + ghost)
```

### 3.2 Hero SVG (line-art) — спільний стиль

- Viewport: 600 × 600
- Stroke: `#0A0A0A`, `stroke-width: 1.6`, `linecap: round`, `linejoin: round`
- Fill acc.: `#E8DCC4` (beige light) або `#FAF6EC` (cream)
- Accent color: `#A63737` (red — для печаток, акцентних деталей, червоних smells)
- Ground reference: `path d="M 20 585 L 580 585"` з `dasharray 4 6` (тонка dashed лінія знизу як підкладка)
- Текст у SVG: Manrope for labels, Playfair Display italic для emphasis

Приклади предметів в hero кожної сторінки:
- Аутсорсинг ОП → класична каска з RACIO-бейджем
- Аудит ОП → планшет з AUDIT REPORT звітом + лупа + MOCK-штамп
- Документація ОП → стос документів + ЗАТВЕРДЖЕНО-печатка + перо
- Пакети документів → ряд папок з галузевими tab-ярликами + READY-штамп
- Тренінги з ОП → дошка з топіками + групка учасників
- Розслідування НВ → годинник з 24/7-бейджем + календар
- Супровід Держпраці → ваги + щит + документи
- Аутсорсинг ПБ → будівля з планом евакуації + вогнегасник + ДСНС-значок
- Аудит ПБ → планшет з чек-листом + MOCK-штамп + вогнегасник
- Документація ПБ → план евакуації на стіні + ЗАТВЕРДЖЕНО-печатка
- Тренінги з ПБ → людина з вогнегасником + полум'я + EXIT-знак
- Декларація ДСНС → двері з замком + ДСНС ✓ табличка
- Оцінка ризиків → матриця 5×5 з heat-map
- Цивільний захист → будівля з укриттям + тривога
- Тренінги з безпеки праці → медитуюча фігура + концентричні кола + heart-rate лінія

---

## 4. Сторінки — унікальна структура

### 4.1 Головна (`index.html`) — 18 блоків

Відрізняється від шаблону сервісної сторінки — служить як hub.

```
[1]  Hero (triptych SVG: каска + вогнегасник + планшет)
[2]  Brand-line (ISO + stats одним рядком, caps)
[3]  Logos strip
[4]  «Хто такі RACIO» (про компанію, grid 1.3/1 + 3 stat-cards)
[5]  4 напрями (grid-4 картки — ОП/ПБ/К.Р./Тренінги)
[6]  Problem → Solution (dark, .vs)
[7]  KPI strip (red, 4 metrics)
[8]  Тарифи (3 pricing cards + CTA «Порівняти всі пакети →»)
[9]  Повний каталог (3 колонки: ОП 7 / ПБ 5 / К.Р. 3 з вертикальними списками посилань)
[10] Process (4 steps)
[11] Галузі (4×2 grid 8 карток + CTA «Клієнти та кейси →»)
[12] Тренінги-хаби (3 cards — лінки на хаби-landings)
[13] Кейси (4 картки + CTA «Всі кейси →»)
[14] FAQ (6 топ-питань)
[15] Чому не самостійно? (2 колонки порівняння + inline lead-форма)
[16] Quiz (калькулятор)
[17] Блог (3 picked articles, різні суміжні сторінки як таргети)
[18] Final CTA (dark)
```

### 4.2 Про компанію (`pro-kompaniyu.html`) — ⚠ ПОТРЕБУЄ РОЗГОРТАННЯ

**Поточно 423 слова.** Є коректна структура, але блоки короткі. За ТЗ потрібно:

```
[1]  Breadcrumb
[2]  Hero (H1 + subheadline + CTA)
[3]  Timeline «Наша історія» (14 років у 10-15 подій)
[4]  Команда «Люди, які роблять RACIO» (grid-cards профайлами)
[5]  Values «Чому нам довіряють» (4 картки принципів)
[6]  Ліцензії та сертифікати
[7]  RSS-секція (Reputation / Sustainability / Social — R·S·S брендовий стандарт)
[8]  Partners / логотипи
[9]  Final CTA «Хочете познайомитись?»
```

### 4.3 Клієнти та кейси (`kliyenty-ta-keysu.html`) — ⚠ ПОТРЕБУЄ РОЗГОРТАННЯ

**Поточно 371 слово.** За ТЗ — 5-7 повних кейсів з конкретикою.

```
[1]  Breadcrumb + Hero (з H1 + sub)
[2]  Filters (галузі: фарма, IT, вир., рітейл, лог., фін., ін.)
[3]  Case-cards grid (8-12 карток, клік → detail-view)
[4]  Featured case (розгорнутий з метриками, цитатою, фото)
[5]  Testimonials (4-6 одиниць)
[6]  Logos all clients (~40 логотипів)
[7]  Final CTA
```

### 4.4 Контакти (`kontakty.html`) — ⚠ ТОНКА (нормально для контактів)

```
[1]  Breadcrumb + Hero «Контакти»
[2]  Contacts grid (phone, email, address, schedule — 4 картки)
[3]  Form (name, phone, email, message, topic-dropdown)
[4]  Map embed
[5]  Банківські реквізити (опц., якщо потрібно)
[6]  Final CTA
```

### 4.5 Галузі (`halusi.html`) — ⚠ ПОТРЕБУЄ РОЗГОРТАННЯ

**Поточно 281 слово.** Стратегічна сторінка — на неї з сервісних ~15+ посилань.

```
[1]  Breadcrumb + Hero «Галузі»
[2]  Intro (pozitioning: 20+ галузей, 500+ клієнтів)
[3]  Industries grid (4×5 або 8×3 cards), кожна картка:
      ├─ Icon
      ├─ H3 назва галузі
      ├─ Short description
      ├─ Список ключових нормативних вимог
      └─ Link на детальний блок нижче
[4]  Per-industry deep blocks (секція на кожну галузь 100-150 слів):
      — Фарма (GMP, GDP, чисті кімнати)
      — MilTech (дозвільні, секретність)
      — IT / офіс (ISO 45001, ергономіка)
      — HoReCa (ПТМ, газ, ДСНС)
      — Ритейл (мережі, сезонні)
      — Виробництво (НПАОП, ЗІЗ)
      — Логістика (ВРР, склади A)
      — Фінанси / Банкінг (BCP, дані)
      — Інші 12+ галузей
[5]  Cases per industry (featured кейс для топ-6 галузей)
[6]  Final CTA
```

### 4.6 Тарифи (`tarify.html`) — ⚠ ПОТРЕБУЄ РОЗГОРТАННЯ

**Поточно 528 слів.** Стратегічна — посилання з усіх сервісних.

```
[1]  Breadcrumb + Hero «Тарифи»
[2]  3 pricing cards (START / SMART / FULL) з цінами і ключовими «включає»
[3]  Full comparison table (матриця — всі фічі × 3 пакети з ✓/✗)
[4]  Галузеві надбавки (модуль «якщо фарма +N%, якщо виробництво +M%»)
[5]  Калькулятор вартості (quiz 5-step)
[6]  FAQ про тарифи
[7]  CTA «Зв'яжіться для індивідуальної пропозиції»
```

### 4.7 RACIO Safety Standard (`rss.html`) — ⚠ ТОНКА (279 слів, standalone)

```
[1]  Breadcrumb + Hero «RACIO Safety Standard»
[2]  Что таке RSS — 3 картки R / S / S
[3]  Принципи (6-8 принципів детально)
[4]  Звітність (приклад звіту)
[5]  Для кого (enterprise клієнти)
[6]  Testimonials від клієнтів-прихильників
[7]  Final CTA «Дізнатись деталі»
```

**Тут є дилема:** Розгорнутий RSS-блок уже є в `pro-kompaniyu.html`. Потрібно або вилучити з `pro-kompaniyu` → залишити лише на `rss.html`, або синхронізувати контент.

### 4.8 Блог (`blog.html`) — ⚠ РУБРИКАТОР

**Поточно 363 слова.** Статей немає.

```
[1]  Breadcrumb + Hero «Блог»
[2]  Category filters (ОП / ПБ / КР / Тренінги / Законодавство / Кейси)
[3]  Featured article (1 картка-анонс великого формату)
[4]  Articles grid (12-18 останніх)
[5]  Pagination
[6]  Newsletter signup
[7]  Final CTA
```

Статті (кожна — окремий `/blog/<slug>/` URL) — не в scope цього документа.

### 4.9 Корисне (`koryisne.html`) — ⚠ РУБРИКАТОР

**Поточно 345 слів.** Матеріалів немає.

```
[1]  Breadcrumb + Hero «Корисне»
[2]  Type filters (чек-листи / шаблони / гайди / інфографіка)
[3]  Featured material
[4]  Materials grid (з іконкою типу + download-кнопкою)
[5]  CTA «Підпишіться, щоб отримувати нові»
```

---

## 5. Відхилення сервісних сторінок від шаблону

| Сторінка | Унікальні блоки / відхилення |
|---|---|
| **Аутсорсинг ОП** | + VS-блок «Без нас / З RACIO» (dark) · + SEO-C comparison table (Штатний vs Аутсорсинг) · + SEO-D — 8 критеріїв вибору підрядника · FAQ 10 питань (замість типових 6) |
| **Аудит ОП** | Блок 5 = 2-cards «Для кого + Коли» злиті (замість типових grid-3/6) · SEO-C про pricing замість comparison |
| **Документація ОП** | + Comparison table «Розробка vs Пакет» (.cmp) · Process 5 кроків (замість 4) · Section 3.2 «Для кого» як grid-3 (замість grid-2) |
| **Пакети документів ОП** | + Industries-overview block (grid-4 з галузями наявних пакетів) · Process 4 кроки з «Супровід 12 міс.» як останній крок |
| **Тренінги з ОП** | hub з 5 training-cards (замість grid-3 «Що входить») + dashed-placeholder card «Нова тема під запит» · без processed FAQ |
| **Розслідування НВ** | **Red final CTA замість dark** · 24/7 hero-акцент · «Когда викликати» .numlist inline · Quiz 3-step (не 5) · Екстрений режим форми зверху |
| **Супровід Держпраці** | + KPI strip (red) — унікальні метрики: 80% виграних справ, 2-5× зниження штрафу · Grid-3 «Підготовча / День X / Після» · «Для кого + Що не робимо» як окремий блок |
| **Аутсорсинг ПБ** | Hero з будівлею + вогнегасником (не каска) · Посилання на `deklaratsiia-dsns` як primary secondary-CTA |
| **Аудит ПБ** | Hero — планшет з fire checklist замість OP-checklist |
| **Документація ПБ (merged)** | + «3 формати» block з tier-cards (300 ₴ інструкція / 4900 ₴ пакет / 12000 ₴ розробка) замість типового 6-card grid |
| **Тренінги з ПБ** | Grid-2 training cards + dashed placeholders · Polygon-акцент у deliverables |
| **Декларація ДСНС** | **+ окрема секція «Замір опору ізоляції»** (як компонент) між deliverables і quiz · Hero — двері з ДСНС-ключем замість типової ілюстрації |
| **Оцінка ризиків** | Hero — матриця 5×5 heat-map · + блок «5 категорій ризиків» (numbered list із фізичних → психосоц.) · Контекст «атестація → оцінка» як SEO-A |
| **Цивільний захист** | Hero — будівля з укриттям · «ПНО-блок» у «Що входить» · Акцент на воєнний стан + Постанова КМУ №1200 |
| **Тренінги з безпеки праці** | Hero — медитуюча фігура (психологічний напрям) · Process 5 кроків (+ follow-up через 1 міс.) · Акцент «психолог vs коуч vs тренер» у SEO-A |

---

## 6. Повторювані UI-компоненти (CSS classes у `racio.css`)

| Клас | Призначення | Виглядає як |
|---|---|---|
| `.container` | Max-width wrapper, padding | Стандарт |
| `.hero-grid` | 60/40 split для hero | Ліва колонка текст, права — SVG |
| `.sec-head` | Секційний заголовок (eyebrow + h2 + italic) | Центрований або ліворуч (.center модифікатор) |
| `.grid-2, .grid-3, .grid-4` | Grid layouts | Cards |
| `.card` | Стандартна картка | White bg, border 1px, num в italic red |
| `.cream, .dark, .red` | Section background modifiers | Beige, black, accent-red |
| `.vs` + `.vs-col.bad/.good` | Dark 2-column comparison | Dark bg — для Problem/Solution |
| `.vs-col-light` + `.vs-diy` | Light 2-column comparison | White cards — для DIY-comparison на home |
| `.process, .step` | Horizontal timeline | Step-cards з num, time, опис |
| `.deliv` | Vertical list з arrows | Italic red → bullet |
| `.num-list` | Numbered SEO list | Playfair italic цифра лівою колонкою |
| `.compare, .cmp` | Comparison tables | Table з header-left ink-color, right-col red-accent |
| `.kpi` | Red metric strip | 4 великі числа в ряд |
| `.logos` | Client logos strip | Flex-wrap text-logos |
| `.testi` | Testimonial cards | 2 cards grid з H3 italic |
| `.quiz, .quiz-step` | Wizard | 5 steps з progress bar |
| `.faq` + `<details>` | Accordion | Plus-toggle, 45° at open |
| `.blog, .post` | Blog cards | 3-grid з kicker (caps) + H3 + «Читати →» |
| `.catalog-grid, .catalog-col` | Home page services catalog | 3 колонки з вертикальними списками |
| `.about-grid, .about-stats` | Home page about block | Split 1.3/1 + 3 stat-cards |
| `.vs-diy, .vs-diy-cta` | Home page DIY comparison | 2 cards + inline lead-form |
| `.hub-tiles, .hub` | 3-card category selectors | Large cards з num-italic |
| `.industries, .ind` | 4×2 industry grid | Small icon + H4 + опис |
| `.prices, .price` | Tariff cards | 3 cards, .anchor = середня picked |
| `.finalcta` | Final CTA block | Dark bg, centered H2 з italic |
| `.timeline, .tl-item, .tl-year` | History timeline | Vertical з dots |
| `.tabs` | Category tabs | Horizontal scrollable |

---

## 7. Кольорова палітра (довідково)

- **Beige-домінанта:** `#E8DCC4` (brand primary background), `#FAF6EC` (cream), `#EFE5D1` (beige-2)
- **Ink / типографіка:** `#0A0A0A` (черний), `var(--ink-2)` (темно-сірий), `var(--muted)` (#6B6258 — мідл-сірий)
- **Accent:** `#A63737` (rhubarb-red — для CTA, emphasis)
- **Hairline:** `var(--line)` — тонкі розділювачі

## 8. Типографіка (довідково)

- **Основа:** Manrope 400/500/600/700 (sans-serif)
- **Emphasis / Italic:** Playfair Display italic 400/500 — для `<em>` у заголовках і акцентних цифр
- **H1:** clamp(40px, 5vw, 72px), Manrope 500 або 600
- **H2:** clamp(28px, 3.5vw, 48px)
- **H3:** 20-24px зазвичай
- **Body:** 15-17px, line-height 1.6-1.7
- **Eyebrow:** 11-13px, caps, letter-spacing 0.14em, colored-red для accent

## 9. Статус сторінок — пріоритет для дизайн/розробки

| Статус | Кількість | Дії |
|---|---:|---|
| ✅ Повний лендинг (13+ блоків, 1000+ слів) | **17** | Готові до дизайн-проходу |
| ⚠ Тонка / потребує розгортання за ТЗ | **7** | **Спочатку** — довести до повного лендингу, потім дизайн |

**Тонкі (пріоритет розгортання):**
1. `halusi.html` — критично, на цю сторінку ~15+ внутрішніх посилань
2. `tarify.html` — критично, ~12 посилань
3. `kliyenty-ta-keysu.html` — важливо, ~10 посилань
4. `pro-kompaniyu.html` — важливо, менеджерська сторінка
5. `kontakty.html` — OK (контактна — сама по собі лаконічна)
6. `rss.html` — опційно (частково дублюється з `pro-kompaniyu`)
7. `blog.html` + `koryisne.html` — рубрикатори, наповнюватимуться статтями

---

## 10. Мобільна адаптація

Усі сторінки responsive — на розмірі **≤860px:**
- `.hero-grid` згортається в 1 колонку (SVG переходить під текст)
- `.grid-4` → `.grid-2` → 1 колонка
- `.vs`, `.vs-diy`, `.catalog-grid` — 1 колонка
- `.cases` — 1 колонка замість 3-4
- `.prices` — 1 колонка зі стеком
- Sticky CTA з'являється внизу екрана
- Header: dropdown → burger overlay

## 11. Типові user flows

1. **Organic SEO → landing → quiz** (основний flow для ОП/ПБ/КР сервісних сторінок)
2. **Main nav → dropdown → service page → cross-link → related service** (лабіринт-навігація)
3. **Home page catalog → direct landing** (для тих, хто вже знає що шукає)
4. **Home page «Хто ми → Клієнти та кейси» → конкретний кейс → service** (trust-flow)
5. **Emergency: Головна → dropdown ОП/ПБ → рядок екстрених (розслідування НВ) з phone-CTA** (24/7-flow, червоний final CTA)

---

_Кінець документа. Для копі-роботи — див. `copy-for-copywriter.md`._
