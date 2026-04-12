# 🧠 SUBIT-NOUS v4.0.0 – Повний Туторіал

## Вступ

**SUBIT-NOUS** — це формальна алгебраїчна система координат для сенсу, яка перетворює будь-яку папку або файл у **обчислюваний граф знань** з 256 архетипів. 

Цей туторіал проведе вас через всі можливості системи: від базового аналізу до нейронної класифікації, агентів, пошуку, візуалізації та інтеграції з AI-асистентами.

---

## 📋 Зміст

1. [Встановлення](#1-встановлення)
2. [Базовий аналіз тексту](#2-базовий-аналіз-тексту)
3. [Нейронна класифікація](#3-нейронна-класифікація)
4. [Агенти та генерація тексту](#4-агенти-та-генерація-тексту)
5. [Гібридний пошук](#5-гібридний-пошук)
6. [Візуалізація графа знань](#6-візуалізація-графа-знань)
7. [Запити до графа](#7-запити-до-графа)
8. [Continuous SUBIT (Soft вектори)](#8-continuous-subit-soft-вектори)
9. [Веб-інтерфейс](#9-веб-інтерфейс)
10. [API сервер](#10-api-сервер)
11. [Інтеграція з AI-асистентами](#11-інтеграція-з-ai-асистентами)
12. [Експорт та документація](#12-експорт-та-документація)
13. [Наступні кроки](#13-наступні-кроки)

---

## 1. Встановлення

### 1.1 Встановлення з PyPI

```bash
pip install subit-nous
```

### 1.2 Встановлення з GitHub (для останньої версії)

```bash
pip install git+https://github.com/sciganec/subit-nous.git
```

### 1.3 Встановлення з додатковими залежностями

```bash
pip install subit-nous[all]  # включає ML, LLM, тестування
```

### 1.4 Перевірка встановлення

```bash
nous version
# Вивід: SUBIT-NOUS version 4.0.0
```

---

## 2. Базовий аналіз тексту

### 2.1 Аналіз окремого файлу

```bash
# Створіть текстовий файл
echo "I think logically about the east in spring" > test.txt

# Проаналізуйте його
nous analyze test.txt --output output

# Відкрийте результат
start output/graph.html
```

### 2.2 Аналіз папки з документами

```bash
# Створіть папку з різними текстами
mkdir my_docs
echo "I think logically about the east in spring" > my_docs/micro.txt
echo "We trust our community in the south during summer" > my_docs/macro.txt
echo "You feel the beauty of autumn in the west" > my_docs/meso.txt
echo "They exert power in the north during winter" > my_docs/meta.txt

# Аналіз всієї папки
nous analyze my_docs --output my_knowledge
```

### 2.3 Розуміння результатів

Після аналізу ви отримаєте:

| Файл | Опис |
|------|------|
| `graph.html` | Інтерактивний 3D граф знань |
| `report.md` | Текстовий звіт зі статистикою |
| `obsidian/` | Нотатки для Obsidian |
| `graph.json` | Машиночитний граф |

---

## 3. Нейронна класифікація

### 3.1 Класифікація тексту

```bash
# Класифікуйте будь-який текст
nous classify "I think logically about the east"

# Вивід:
# SUBIT: 170 (10101010)
# Archetype: MICRO mode
# Mode: STATE
# Who: ME
```

### 3.2 Класифікація з ймовірностями

```bash
nous classify "We trust our community" --probs

# Вивід покаже топ-5 передбачень з відсотками впевненості
```

### 3.3 Порівняння з маркерним методом

```bash
# Старий метод (ключові слова)
python -c "from subit_nous.core import text_to_subit; print(text_to_subit('We trust'))"

# Новий метод (нейронна мережа, 87.8% accuracy)
nous classify "We trust"
```

### 3.4 Демонстраційний скрипт

```bash
python examples/classifier_demo.py
```

---

## 4. Агенти та генерація тексту

### 4.1 Запуск агента (потребує Ollama)

```bash
# Встановіть та запустіть Ollama
ollama pull llama3.2:3b
ollama serve

# Запустіть агента в різних режимах
nous agent "Explain what is solar energy" --mode STATE
nous agent "The sunset is beautiful" --mode FORM
nous agent "We must win the market" --mode FORCE --who WE
```

### 4.2 Автоматичне визначення режиму

```bash
nous agent "I think logically about this problem" --mode auto
nous agent "The beautiful colors of autumn" --mode auto
```

### 4.3 Багатоагентний пайплайн

```bash
# Послідовна обробка тексту кількома агентами
nous pipeline "Solar energy is good" --modes STATE,FORM,FORCE
```

### 4.4 Інтерактивне керування через Web UI

```bash
nous ui --port 8501
# Відкрийте вкладку "🎮 Control" для налаштування knobs
```

---

## 5. Гібридний пошук

### 5.1 Індексація папки

```bash
nous index my_docs
```

### 5.2 Пошук без фільтрів

```bash
nous search "climate change"
```

### 5.3 Пошук з фільтрацією за MODE

```bash
nous search "energy" --mode STATE
nous search "community" --mode VALUE
nous search "beauty" --mode FORM
nous search "power" --mode FORCE
```

### 5.4 Пошук з фільтрацією за WHO

```bash
nous search "solution" --who ME
nous search "together" --who WE
nous search "you can" --who YOU
nous search "they will" --who THEY
```

### 5.5 Комбіновані фільтри

```bash
nous search "climate" --mode STATE --who WE --top 10 --alpha 0.7
```

---

## 6. Візуалізація графа знань

### 6.1 3D граф

```bash
nous analyze my_docs --output knowledge
start knowledge/graph.html
```

### 6.2 UMAP проекція (семантична топологія)

```bash
nous umap knowledge/graph.json --output umap.html
start umap.html
```

### 6.3 Clifford Torus (всі 256 станів)

```bash
nous torus knowledge/graph.json --output torus.html
start torus.html
```

### 6.4 Семантичні кластери

```bash
nous clusters knowledge/graph.json --max-dist 2 --output clusters.json
```

---

## 7. Запити до графа

### 7.1 Пошук шляху між архетипами

```bash
nous query "MICRO mode" "MACRO mode"
# Вивід покаже шлях: MICRO → ETHOS_WE_EAST_SPRING → MACRO
```

### 7.2 Пошук всіх шляхів

```bash
nous query 170 255 --all --depth 4
```

### 7.3 Пошук спільних зв'язків

```bash
nous query 170 255 --common
```

### 7.4 Запит з текстом

```bash
nous query "I think logically" "We trust our community"
```

---

## 8. Continuous SUBIT (Soft вектори)

### 8.1 Отримання soft-профілю

```bash
nous soft my_docs --output profile.json
```

### 8.2 Косинусна подібність

```bash
nous soft --sim1 my_docs/micro.txt --sim2 my_docs/macro.txt
```

### 8.3 Інтерполяція між текстами

```bash
nous soft --interp1 my_docs/micro.txt --interp2 my_docs/macro.txt --alpha 0.3
```

### 8.4 Радарна діаграма

```bash
nous soft --radar profile.json --output radar.html
```

---

## 9. Веб-інтерфейс

### 9.1 Запуск UI

```bash
nous ui --port 8501
```

Відкрийте `http://localhost:8501`

### 9.2 Вкладки інтерфейсу

| Вкладка | Функція |
|---------|---------|
| 🔍 Analyze | Аналіз тексту (маркерний) |
| 🤖 Agents | Генерація тексту агентами |
| 🔎 Search | Гібридний пошук |
| 📊 Profile | Soft-профіль та радарна діаграма |
| 🎮 Control | Інтерактивне керування knobs |
| 🧠 Classify | Нейронна класифікація |
| 🧩 Clusters | Семантичні кластери |
| 🌀 Torus | 3D візуалізація тора |
| 🗺️ UMAP | UMAP проекція |
| 🎚️ Interpolation | Плавний перехід між архетипами |

### 9.3 Темна тема

Перемикайте тему в сайдбарі (🎨 Theme → Light/Dark)

### 9.4 Presets

Використовуйте готові налаштування:
- 📊 Analyst (STATE/ME)
- 🎨 Poet (FORM/YOU)
- ⚡ Leader (FORCE/WE)
- 🤝 Mediator (VALUE/WE)

---

## 10. API сервер

### 10.1 Запуск сервера

```bash
nous serve --port 8000
```

### 10.2 Ендпоінти

| Метод | Ендпоінт | Опис |
|-------|----------|------|
| GET | `/health` | Перевірка стану |
| POST | `/analyze/text` | Аналіз тексту |
| POST | `/classify` | Нейронна класифікація |
| POST | `/search` | Гібридний пошук |
| POST | `/agent` | Запуск агента |

### 10.3 Приклади запитів

```bash
# Health check
curl http://localhost:8000/health

# Аналіз тексту
curl -X POST http://localhost:8000/analyze/text \
  -H "Content-Type: application/json" \
  -d '{"text": "I think logically"}'

# Класифікація
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "We trust our community"}'
```

### 10.4 WebSocket для реального часу

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/live");
ws.onmessage = (e) => console.log(JSON.parse(e.data));
ws.send("I think logically about the east");
```

---

## 11. Інтеграція з AI-асистентами

### 11.1 Встановлення інтеграцій

```bash
nous integrate all --output nous_output
```

### 11.2 Що створюється

| Файл | Призначення |
|------|-------------|
| `CLAUDE.md` | Інструкції для Claude Code |
| `.cursor/rules/subit-nous.mdc` | Правило для Cursor IDE |
| `GEMINI.md` | Інструкції для Gemini CLI |

### 11.3 Видалення інтеграцій

```bash
nous integrate uninstall
```

---

## 12. Експорт та документація

### 12.1 Експорт в різні формати

```bash
# GraphML (для Gephi, yEd)
nous export graph.json --format graphml --output graph.graphml

# Cypher (для Neo4j)
nous export graph.json --format cypher --output graph.cypher

# JSON з confidence та sources
nous export graph.json --format json --output enhanced.json

# Obsidian vault
nous export graph.json --format obsidian --output my_vault/
```

### 12.2 Генерація Wiki документації

```bash
nous wiki graph.json --output wiki
```

Створюється структура:
```
wiki/
├── index.md           # Головна сторінка
├── nodes/             # Сторінки архетипів
└── communities/       # Сторінки спільнот
```

### 12.3 Звіт у форматі Markdown

```bash
cat nous_output/report.md
```

Містить:
- Статистику архетипів
- Профіль модусів (ASCII смужки)
- Бог-вузли
- Неочікувані зв'язки
- Рекомендовані питання

---

## 13. Наступні кроки

### 13.1 Поглиблене вивчення

| Ресурс | Посилання |
|--------|-----------|
| Документація API | `docs/api.md` |
| Специфікація SUBIT | `SUBIT_v3.md` |
| Приклади коду | `examples/` |
| Тести | `tests/` |

### 13.2 Розширення можливостей

| Завдання | Команда |
|----------|---------|
| Тренування класифікатора | `python scripts/train_classifier.py` |
| Генерація датасету | `python scripts/generate_classifier_data.py` |
| Моніторинг тренування | `python scripts/monitor_training.py` |

### 13.3 Корисні команди

```bash
# Отримати довідку
nous --help

# Отримати версію
nous version

# Автоматичне оновлення графа при змінах
nous watch my_docs --output live_output

# Git hooks для автоматичного аналізу
nous hooks install .
```

---

## 🎯 Підсумок

**SUBIT-NOUS v4.0.0** надає:

- ✅ **Алгебраїчне ядро** – 256 архетипів, операції XOR, Hamming distance
- ✅ **Нейронний класифікатор** – 87.8% accuracy, з ймовірностями
- ✅ **Агенти** – генерація тексту в 4 різних стилях
- ✅ **Гібридний пошук** – семантика + архетипні фільтри
- ✅ **Візуалізація** – 3D граф, UMAP, Torus, радарні діаграми
- ✅ **Веб-інтерфейс** – 10 вкладок, темна тема, presets, knobs
- ✅ **API** – REST + WebSocket для інтеграцій
- ✅ **SDK** – Python бібліотека для розробників
- ✅ **Інтеграції** – Claude Code, Cursor, Gemini CLI

---

## 📚 Додаткові ресурси

- **GitHub:** https://github.com/sciganec/subit-nous

---

**Лабораторія сенсу. Почніть досліджувати вже сьогодні! 🧠🚀**