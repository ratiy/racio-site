# RACIO — редизайн сайту

**Версія:** 2026-04-24 · **Статус:** 23 сторінки, всі з повним контентом · **Сумарно ~30 000 слів SEO-копії**

Цей файл — **handoff-документ** для старту нового чату у разі потреби. Читайте разом з `CLAUDE.md` у корені workspace (`/Users/oleksandrratiy/claude-code-design/CLAUDE.md`).

---

## Про проєкт

**Клієнт:** RACIO — українська компанія з охорони праці, пожежної безпеки та керування ризиками. 15 років на ринку, 16 інженерів, 500+ клієнтів (Scania, AstraZeneca, Oracle, DHL, Ciklum, Ferrero тощо).

**Задача:** редизайн сайту racio.ua з нуля — нова інформаційна архітектура, 23 HTML-сторінки з повним SEO-контентом (~30 000 слів), лабіринт-навігація, якісний voice/tone, передача дизайнеру + копірайтеру.

**Дизайн-підхід:** beige-домінанта (`#E8DCC4`, `#FAF6EC`), accent red (`#A63737`), типографіка Manrope (sans) + Playfair Display italic (emphasis). Line-art SVG hero на кожній сторінці. Structural approach — Claude Design taste rules (див. `CLAUDE.md`).

---

## Де переглянути

- **Live URL (auto-deploy):** https://candid-profiterole-017286.netlify.app/
- **GitHub repo:** https://github.com/ratiy/racio-site (private)
- **Локально:** `python3 -m http.server 4567` у `artifacts/racio/` → http://127.0.0.1:4567/

**Auto-deploy:** будь-який `git push` у `main` → Netlify оновлює сайт за 30-60 секунд на тому ж URL. Дизайнер/замовник бачать актуальний стан без додаткових дій.

**Git commits — без `Co-Authored-By` trailer.** Netlify рахує co-authors як окремих контрибуторів і блокує build на private-планах. Репо зараз public — обмеження не діє, але краще тримати коміти solo-author на майбутнє.

---

## Структура проєкту

```
artifacts/racio/
├── index.html                          ← головна (18 блоків, 1231 слів)
├── racio.css                           ← глобальні стилі (~500 CSS-класів)
├── racio.js                            ← header/footer/sticky injection + nav tabs + quiz logic
├── PROJECT.md                          ← цей файл
│
├── [ОХОРОНА ПРАЦІ — 7 сторінок]
│   ├── autsorsynh.html                 (2055w)
│   ├── audit.html                      (1522w)
│   ├── dokumentatsiia.html             (1274w)
│   ├── pakety-dokumentiv.html          (1120w)
│   ├── treningy-z-ohorony-pratsi.html  (1139w)  ← раніше navchannia.html
│   ├── rozsliduvannia-nv.html          (1201w)
│   └── suprovid-derzhpratsi.html       (1307w)
│
├── [ПОЖЕЖНА БЕЗПЕКА — 5 сторінок]
│   ├── autsorsynh-pojejna-bezpeka.html (1192w)
│   ├── audit-pojejna-bezpeka.html      (1103w)
│   ├── dokumentatsiia-pojejna-bezpeka.html (1276w, merged з 3 брифів)
│   ├── treningy-z-pojejnoi-bezpeky.html (1082w)  ← раніше navchannia-pojejna-bezpeka.html
│   └── deklaratsiia-dsns.html          (1402w, + секція «Замір опору ізоляції»)
│
├── [КЕРУВАННЯ РИЗИКАМИ — 3 сторінки]
│   ├── otsinka-ryzykiv.html            (1207w)
│   ├── tsyvilnyi-zakhyst.html          (1273w)
│   └── treningy-z-bezpeky-pratsi.html  (1067w)
│
├── [ПРО НАС — 3 сторінки]
│   ├── pro-kompaniyu.html              (1616w, + RSS-секція з id="rss")
│   ├── kliyenty-ta-keysu.html          (1440w)
│   └── kontakty.html                   (231w — базова, нормально для контактної)
│
├── [ЩЕ — у футері, не в dropdown]
│   ├── halusi.html                     (1581w)
│   └── tarify.html                     (1901w)
│
├── [БЛОГ]
│   ├── blog.html                       (363w — рубрикатор)
│   └── koryisne.html                   (345w — рубрикатор)
│
└── docs/                               ← документація для команди
    ├── structure-for-designer.md       (28 KB — архітектура для дизайнера)
    ├── copy-for-copywriter.md          (19 KB — індекс копірайтера)
    ├── _extract_copy.py                (скрипт для регенерації копі з HTML)
    └── copy/                           (23 per-page md-файли з повним текстом)
```

---

## Меню сайту (фінальне)

```
Охорона праці ▾ (7 пунктів)
  Аутсорсинг                      → autsorsynh.html
  Аудит ОП                        → audit.html
  Документація                    → dokumentatsiia.html
  Пакет документів                → pakety-dokumentiv.html
  Тренінги з ОП                   → treningy-z-ohorony-pratsi.html
  Розслідування НВ                → rozsliduvannia-nv.html
  Супровід перевірок Держпраці    → suprovid-derzhpratsi.html

Пожежна безпека ▾ (5 пунктів)
  Аутсорсинг ПБ                   → autsorsynh-pojejna-bezpeka.html
  Аудит ПБ                        → audit-pojejna-bezpeka.html
  Документація                    → dokumentatsiia-pojejna-bezpeka.html
  Тренінги з ПБ                   → treningy-z-pojejnoi-bezpeky.html
  Декларація ДСНС                 → deklaratsiia-dsns.html

Керування ризиками ▾ (3 пункти)
  Оцінка ризиків                  → otsinka-ryzykiv.html
  Цивільний захист                → tsyvilnyi-zakhyst.html
  Тренінги з безпеки праці        → treningy-z-bezpeky-pratsi.html

Про нас ▾ (3 пункти)
  Про компанію                    → pro-kompaniyu.html
  Клієнти та Кейси                → kliyenty-ta-keysu.html
  Контакти                        → kontakty.html

Блог ▾ (2 пункти)
  Статті                          → blog.html
  Корисне                         → koryisne.html

[Футер «Ще»] — 3 посилання:
  Галузі                          → halusi.html
  Тарифи                          → tarify.html
  RACIO Safety Standard           → pro-kompaniyu.html#rss (anchor)
```

**Було:** `navchannia.html`, `navchannia-pojejna-bezpeka.html`, `rss.html` як окремі сторінки.
**Стало:** перейменовано на `treningy-z-*.html` (тренінги, не навчання — бо офіційні посвідчення видає акредитований центр-партнер, а ми робимо корпоративні тренінги). `rss.html` — видалено, зміст інтегрований в `pro-kompaniyu.html#rss`.

---

## Хронологія зробленого (7 фаз)

### Фаза 1 — Лабіринт-навігація
Меню «Про нас» спрощене до 3 пунктів. Концепція: жодних bridge-блоків «Вам також буде цікаво» — всі внутрішні посилання **вплетені в прозу природно** (labyrinth rule).

### Фаза 2 — SEO-блоки на 7 сервісних сторінках ОП
Кожна сторінка отримала: SEO-A (проза), SEO-B (нумерований список), блог-картки, FAQ. Word count: 615-713 → 1120-2055.

### Фаза 3 — Пожежна безпека (5 сторінок)
Створено з нуля за ТЗ. Розробка / Пакети / Інструкції — мерджено в одну `dokumentatsiia-pojejna-bezpeka.html` з 3 tier-картками (300 ₴ / 4 900 ₴ / 12 000 ₴).

### Фаза 4 — Rename «Навчання» → «Тренінги з ...»
Причина: RACIO не проводить офіційне НАПБ-навчання (це робить акредитований центр). Переформатовано на корпоративні тренінги. Видалено `navchannia.html` і `navchannia-pojejna-bezpeka.html` після міграції посилань.

### Фаза 5 — Керування ризиками (3 сторінки)
`otsinka-ryzykiv.html` (на заміну атестації, матриця 5×5, ISO 45001), `tsyvilnyi-zakhyst.html` (документи ЦЗ, ПНО, воєнний стан), `treningy-z-bezpeky-pratsi.html` (вигорання + стрес-менеджмент з психологом).

### Фаза 6 — Головна (18 блоків)
Перероблено index.html: виправлено 5 broken links, додано 4 нові блоки — «Хто такі RACIO», повний каталог 15 послуг у 3 колонках, 3 training-hub cards, «Чому не самостійно?» з lead-формою, FAQ на головній.

### Фаза 7 — Thin-сторінки (4 сторінки)
Розгорнуто `halusi.html` (281 → 1581 слів, 8 галузей з глибоким описом), `tarify.html` (528 → 1901, 8 функціональних табів), `kliyenty-ta-keysu.html` (371 → 1440, 3 featured-кейси), `pro-kompaniyu.html` (423 → 1616, методологія + партнери + RSS-блок).

---

## Конвенції / правила (voice, tone, інфраструктура)

### Voice & Tone

- **Короткі речення, числа, конкретика.** «500+ клієнтів», «15 років», «16 інженерів» — не «широкий спектр».
- **Без маркетингового пафосу.** Факти > прикметники.
- **Українська — без кальки.** «Виконання робіт» → «роботи»; «поскольку» → «оскільки» (і то рідко, краще переформулювати).
- **Italic emphasis у заголовках** — через `<em>` з Playfair Display, 1-2 слова на фразу.
- **Без emoji.** Взагалі.
- **CTA formulas:** «Отримати прорахунок →», «Замовити аудит →», «Викликати команду →» (екстрені).

### Labyrinth rule (важливо)

Жодних блоків «Вам також буде цікаво», «Related pages», «Suggested for you». **Усі внутрішні посилання вплетені в прозу природно** — у контексті, числах, термінах послуг.

Щільність посилань:
- Сервісна сторінка (1000-2000 слів): 8-12 внутрішніх посилань
- Головна: 22+ посилань (охоплення всього каталогу)
- Thin-сторінки після розгортання: 10-15 посилань

### Transliteration (файли)

- **ОП-послуги** — короткі: `autsorsynh.html`, `audit.html`
- **ПБ-послуги** — з категорією: `autsorsynh-pojejna-bezpeka.html`
- **Тренінги-хаби** — повні: `treningy-z-ohorony-pratsi.html`
- **К.Р. сервіси** — короткі: `otsinka-ryzykiv.html`, `tsyvilnyi-zakhyst.html`

### CSS-компоненти (в `racio.css`)

Спільні класи для всіх сторінок:
- `.seo-prose` — обгортка SEO-text блоків з inline-лінками
- `.num-list` — нумерований SEO-список з Playfair italic цифрами
- `.compare` / `.cmp` — comparison tables
- `.card`, `.deliv`, `.vs`, `.vs-col-light`, `.kpi`, `.logos`, `.testi`, `.faq`, `.blog/.post`
- `.finalcta`, `.timeline`, `.process`, `.quiz`, `.prices`, `.hub-tiles`
- **Нові (з фази 6):** `.catalog-grid/.catalog-col`, `.about-grid/.about-stats`, `.vs-diy/.vs-col-light/.vs-diy-cta`

### Backup convention

Перед кожною значущою зміною (rewrite, file rename, великий expansion):

```bash
cp FILE.html /Users/oleksandrratiy/claude-code-design/.claude/backups/FILE-YYYY-MM-DD-pre-REASON.html
```

Всі бекапи в `.claude/backups/` — 10+ файлів з повною історією змін.

### Бренд-біблія (довідково)

**Цифри:** 15+ років · 500+ клієнтів (з них 110+ enterprise на FULL) · 16 інженерів · 20+ галузей · 98% перевірок без штрафу · 2500+ посвідчень · 290+ декларацій ДСНС

**Ключові клієнти:** Scania · AstraZeneca · Oracle · DHL · Decathlon · Michelin · Ferrero · Ciklum · Roche · Danone · PepsiCo · Glovo · Toyota · Credit Agricole · SEB · Silpo · Varus

**Ціни орієнтири:**
- Аутсорсинг ОП: 8 000 / 15 000 / 20 000 ₴/міс (START/SMART/FULL)
- Аутсорсинг ПБ: 12 900 / 19 900 / 34 900 ₴/міс
- Документація (разово): 15 000 / 35 000 / 80 000 ₴
- Аудит: 9 900 / 22 900 / 45 000 ₴
- Декларація ДСНС: 8 900 / 14 900 / 29 900 ₴
- Навчання: 290-1 290 ₴/особа
- Тренінги: 1 200-2 500 ₴/особа

**Регуляторні акти:**
- ЗУ «Про охорону праці» (не «Закон України...»)
- НАПБ А.01.001-2024 (нова редакція правил ПБ)
- НПАОП 0.00-4.12-05 (навчання з ОП)
- Постанова КМУ №1200 (категорування ЦЗ)
- ст. 41 КУпАП (штраф директору 5 100 ₴)
- ст. 172 КК України (кримінальна відповідальність за ОП)
- ст. 271-272 КК (НВ)

---

## Інфраструктура

- **Chrome DevTools MCP** — підключено для live-превью через `.claude/hooks/shrink-screenshot.sh` (auto-resize до 1600px)
- **Monolith CLI** — `/opt/homebrew/bin/monolith` для standalone HTML-bundling
- **Бекапи** — `.claude/backups/`
- **Скріншоти** — `.claude/*.png` (capacity-limit friendly, ≤1600px)
- **ТЗ оригінали** (у користувача): `/Users/oleksandrratiy/Desktop/Claude Cowork/Редизайн сайта/Фаза 2 — блочна база/{Охорона праці,Пожежна безпека,Керування ризиками}/*.md`

---

## Документація для команди (в `docs/`)

- **`structure-for-designer.md`** — архітектура для дизайнера. 11 розділів:
  - Sitemap
  - Глобальні компоненти (header, footer, sticky mobile)
  - Шаблон типової сервісної сторінки (13-15 блоків)
  - Унікальні сторінки (index + thin-сторінки)
  - Відхилення кожної сервісної від шаблону
  - CSS-компоненти
  - Палітра й типографіка
  - Статус пріоритетності
  - Мобільна адаптація
  - Типові user flows

- **`copy-for-copywriter.md`** — індекс для копірайтера. 9 розділів:
  - Таблиця всіх 23 сторінок зі шляхами
  - Пріоритет роботи
  - Voice & tone правила
  - Labyrinth linking rules
  - Бренд-біблія
  - Шаблон блок-за-блоком
  - Workflow

- **`copy/*.md`** — 23 per-page файли з повним текстом блок-за-блоком. Генеруються з HTML через `python3 docs/_extract_copy.py`.

---

## Як регенерувати `docs/copy/*.md` після змін у HTML

```bash
cd /Users/oleksandrratiy/claude-code-design/artifacts/racio
python3 docs/_extract_copy.py
```

Скрипт автоматично парсить усі 23 HTML, витягає eyebrow / heading / subtitle / CTAs / списки / FAQ / quiz-кроки / таблиці, і пише структурований markdown.

---

## Можливі наступні кроки

### 🟢 Готові до дизайн-проходу без змін
- Усі 17 повних лендингів (сервісні + головна)
- 4 розгорнуті thin-сторінки (halusi, tarify, kliyenty, pro-kompaniyu)

### 🟡 Можливі доробки
- **Наповнення блогу статтями** (окрема епопея — 10-20 матеріалів, кожен 500-1500 слів)
- **Наповнення «Корисне» шаблонами/чек-листами** (10-15 матеріалів, окрема епопея)
- **EN-версія сайту** — потребує перекладу 23 сторінок (велика задача)
- **Динамічні форми / back-end** — зараз усі форми з `onsubmit="event.preventDefault()"` як прототипи

### 🔵 Операційна доробка
- **Git-репо** — ініціалізувати для версіонування
- **Netlify / Cloudflare Pages** — постійний URL з auto-deploy
- **Google Analytics / Umami** — метрики
- **SEO-schema (JSON-LD)** — structured data для Google
- **OG-зображення** — для соц. мереж (зараз немає)

---

## Як почати новий чат з цим контекстом

1. **Надіслати у новому чаті посилання на цей файл:** `@artifacts/racio/PROJECT.md`
2. Claude прочитає файл і зрозуміє проєкт, поточний стан, конвенції
3. Якщо треба ще більше контексту — приклад сервісної сторінки: `@artifacts/racio/autsorsynh.html` (типовий повний лендинг)
4. ТЗ оригінальні у копірайтера / замовника є окремо на диску в `/Users/oleksandrratiy/Desktop/Claude Cowork/Редизайн сайта/`

---

## Корисні команди

```bash
# Змінити слова + targets по всіх сторінках:
cd /Users/oleksandrratiy/claude-code-design/artifacts/racio
python3 -c "
import re, os
for f in sorted([x for x in os.listdir('.') if x.endswith('.html')]):
    html = open(f).read()
    t = re.sub(r'<(script|style|svg)[^>]*>.*?</\1>', '', html, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    targets = sorted(set(re.findall(r'href=\"([a-z-]+)\.html', html)))
    print(f'{f:45s} {len(t.split()):5d}w  {len(targets)} targets')
"

# Регенерація копірайтинг-документів:
python3 docs/_extract_copy.py

# Бандлити одну сторінку у standalone HTML:
monolith index.html -o /tmp/racio-home.html

# ZIP для передачі:
cd /Users/oleksandrratiy/claude-code-design/artifacts/
zip -r racio-site.zip racio/ -x "racio/docs/*" "racio/.claude/*"

# Деплой на Netlify (через CLI):
cd /Users/oleksandrratiy/claude-code-design/artifacts/racio
npx netlify deploy --dir=. --prod
```

---

_Кінець. Для деталей — читайте `CLAUDE.md` в workspace root або `docs/structure-for-designer.md` / `docs/copy-for-copywriter.md`._
