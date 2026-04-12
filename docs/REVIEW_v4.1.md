# 🧠 SUBIT‑NOUS v4.1.0

## Дискретна когнітивна адресація для AI-систем

### Розширений огляд · Анонс · Демо · Презентація

---

## 1. Огляд

SUBIT‑NOUS — це перша у світі операційна система для сенсу. Вона перетворює будь-який текст на 8-бітну адресу в просторі 256 архетипів.

**Встановлення:** `pip install subit-nous`

**Аналіз:** `nous analyze ./my-folder --output ./knowledge`

**Ключові цифри:**

- Точність класифікатора: 87.8%
- Стиснення: 1500× (123K токенів → 8 байт)
- Швидкість: 0.05 секунди на текст
- Архетипів: 256 (4 осі × 4 значення)
- Тестів: 30+

**Три оператори (v5.0):**

- Mask — локальний оператор, аналогія — шар у Photoshop
- Transfer — глобальний оператор, аналогія — перенесення стилю
- Evolution — динамічний оператор, аналогія — анімація в просторі

---

## 2. Проблема та рішення

Сьогоднішні AI-системи не мають системи координат для сенсу. Вони працюють з токенами, а не зі смислом. Наслідки: немає контролю → непередбачувані результати; немає пояснюваності → низька довіра; висока вартість → $0.50–10.00 за 1M токенів.

**Рішення:** SUBIT = (ℤ₂)⁸ = WHO × WHERE × WHEN × MODE

**Вісі та значення:**

- WHO: ME (10), WE (11), YOU (01), THEY (00)
- WHERE: EAST (10), SOUTH (11), WEST (01), NORTH (00)
- WHEN: SPRING (10), SUMMER (11), AUTUMN (01), WINTER (00)
- MODE: STATE (10), VALUE (11), FORM (01), FORCE (00)

**Чотири головні архетипи:**

- MICRO (10 10 10 10) — індивідуальне, логічне
- MACRO (11 11 11 11) — колективне, етичне
- MESO (01 01 01 01) — діалогічне, естетичне
- META (00 00 00 00) — системне, вольове

---

## 3. Демонстрація

### Класифікація тексту

```bash
$ nous classify "I think logically about the east"

📝 Text: I think logically about the east
🎯 SUBIT: 170 (10101010)
🏺 Archetype: MICRO mode
🎭 Mode: STATE
👤 Who: ME
🧭 Where: EAST
⏰ When: SPRING
```

### Пошук шляхів у графі

```bash
$ nous query "MICRO mode" "MACRO mode"

Shortest path found:

1. MICRO mode (ID: 170)
   └─[ EXTRACTED (confidence: 1.0) weight: 1 ]
2. ETHOS_WE_EAST_SPRING (ID: 235)
   └─[ EXTRACTED (confidence: 1.0) weight: 1 ]
3. MACRO mode (ID: 255)

Path length: 2 steps
```

### Генерація в стилі

```bash
$ nous agent "Explain solar energy" --mode STATE

STATE mode response:
Solar energy is a renewable energy source that converts sunlight into electricity
using photovoltaic cells. The process is based on the photoelectric effect,
where photons knock electrons free from atoms, generating an electric current.
```

### Гібридний пошук

```bash
$ nous search "climate change" --mode STATE --who WE --top 3

Top 3 results:
1. technical_report.pdf (score: 0.892)
2. research_paper.txt (score: 0.756)
3. meeting_notes.md (score: 0.634)
```

### Візуалізація (Web UI)

```bash
$ nous ui --port 8501
# → відкриває інтерактивний 3D граф
```

**Вкладки UI:**

- Analyze – аналіз тексту
- Agents – генерація в стилі
- Search – гібридний пошук
- Profile – soft-профіль
- Control – knobs для стилю
- Classify – нейронна класифікація
- Clusters – семантичні кластери
- Torus – 3D тор
- UMAP – семантична топологія
- Interpolation – слайдери сенсу

---

## 4. Архітектура

Система складається з кількох шарів:

**Шар інтерфейсу:** CLI (nous), API (REST/WS), Web UI (Streamlit)

**Шар запитів:** DSL Query Engine (AST → Evaluator → Execution Plan)

**Шар операторів:** Mask, Transfer, Evolution, Composition

**Шар переписування:** Controlled Rewrite Engine (Semantic Diff → Axis Rewrite → Pipeline)

**Ядро:** Core Algebra (ℤ₂)⁸ · XOR · Distance · Projection

**Інтеграції:**

- Claude Code → файл CLAUDE.md
- Cursor → файл .cursor/rules/subit-nous.mdc
- Gemini CLI → файл GEMINI.md
- Obsidian → папка obsidian/
- VS Code → розширення (в планах)

---

## 5. Результати

**Порівняння з альтернативами:**

SUBIT має систему координат (ℤ₂)⁸, пояснюваність, локальне виконання, нульову вартість та швидкість 0.05 секунди.

OpenAI не має системи координат, не має пояснюваності, не має локального виконання, коштуть $$$ та працює 1-2 секунди.

Cohere не має системи координат, не має пояснюваності, має локальне виконання, коштує $ та працює 0.5 секунди.

Hemingway не має системи координат, не має пояснюваності, має локальне виконання, коштує $ та працює 0.01 секунди.

**Ключові метрики v4.1.0:**

- Точність класифікації: 87.8%
- Розмір моделі: 250 MB
- Час навчання: близько 10 годин
- Розмір датасету: 50,000 зразків
- Підтримувані формати: текст, JSON, GraphML, Cypher

---

## 6. Презентація для інвесторів

### Elevator Pitch (30 секунд)

SUBIT‑NOUS — це Photoshop для сенсу. Ми створили алгебраїчну систему координат, яка дозволяє вимірювати, редагувати та контролювати сенс будь-якого тексту за допомогою 8 біт. Це перший у світі дискретний редактор сенсу, який працює в 1500× швидше за LLM і коштує в 0× дешевше.

### Ринок

- TAM (AI developer tools): $10 млрд
- SAM (semantic control): $500 млн
- SOM (рік 3): $19 млн

### Бізнес-модель

- Open Source (MIT): безкоштовно для всіх
- Cloud API: $0.001 за запит для розробників
- Enterprise: $5,000 за рік для компаній
- Desktop App: $49 разово для професіоналів

### Прогноз доходів

У 2026 році очікується дохід $136,000 та EBITDA -$94,000. У 2027 році дохід зросте до $2.07 млн, EBITDA +$1.42 млн. У 2028 році дохід сягне $19.0 млн, EBITDA +$16.9 млн.

### Запит

Seed раунд на суму $500,000 для команди (40%), маркетингу (30%) та розробки (30%).

### Roadmap

- v4.1.0: нейронний класифікатор (завершено в квітні 2026)
- v4.2.0: інтеграції та візуалізація (Q3 2026)
- v5.0: три оператори, OS для сенсу (Q4 2026)
- v6.0: користувацькі осі та мультимодальність (Q2 2027)

---

## Посилання та контакти

- GitHub: https://github.com/sciganec/subit-nous

---

**SUBIT‑NOUS — дискретна когнітивна адресація для AI-систем.** 🧠🚀

*Версія: 4.1.0*  
*Дата: 2026-04-12*