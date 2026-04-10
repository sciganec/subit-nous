Ось покрокова інструкція, як **запустити та протестувати все** в SUBIT‑NOUS v3.0 після встановлення.

## 1. Підготовка середовища

```bash
# Перейдіть у папку проекту
cd C:\Users\sciga\subit-nous

# Активуйте віртуальне середовище (якщо ще не активовано)
.\venv\Scripts\Activate.ps1

# Встановіть пакет у режимі розробки (якщо ще не зробили)
pip install -e .
```

## 2. Створіть тестову папку з файлами

```bash
# Якщо папки demo немає – створіть
New-Item -ItemType Directory -Force -Path demo

# Додайте чотири файли для різних модусів
"I think logically about the east in spring" | Out-File -FilePath demo\micro.txt -Encoding utf8
"We trust our community in the south during summer" | Out-File -FilePath demo\macro.txt -Encoding utf8
"You feel the beauty of autumn in the west" | Out-File -FilePath demo\meso.txt -Encoding utf8
"They exert power in the north during winter" | Out-File -FilePath demo\meta.txt -Encoding utf8
```

## 3. Запустіть базовий аналіз (CLI)

```bash
nous analyze demo --output test_output
```

**Очікуваний вивід:**  
- Граф з 4 вузлами, 3 переходами  
- Файли `test_output/graph.html`, `test_output/report.md`, `test_output/obsidian/`

**Перевірте:** відкрийте `test_output/graph.html` у браузері – має бути 3D граф з 4 кольоровими точками.

## 4. Протестуйте Continuous SUBIT (soft-вектори)

```bash
# Середній soft-профіль папки
nous soft demo --output demo_soft.json

# Косинусна подібність між двома файлами
nous soft --sim1 demo\micro.txt --sim2 demo\macro.txt

# Інтерполяція
nous soft --interp1 demo\micro.txt --interp2 demo\macro.txt --alpha 0.3

# Радарна діаграма (після створення demo_soft.json)
nous soft --radar demo_soft.json
```

**Очікуваний вивід:**  
- Косинусна подібність близька до 0 (різні модуси)  
- Інтерполяція видасть 8 чисел  
- Радарна діаграма збережена як `soft_output_radar.html`

## 5. Протестуйте локальний LLM контроль (Ollama)

### 5.1 Встановіть та запустіть Ollama (якщо ще ні)

```bash
# Завантажте та встановіть Ollama з https://ollama.com
# Після встановлення переконайтеся, що сервер працює:
ollama list
```

### 5.2 Завантажте модель (якщо немає)

```bash
ollama pull llama3.2:3b
```

### 5.3 Запустіть команду контролю

```bash
nous control "I think logically about the east" STATE --model llama3.2:3b
```

**Очікуваний вивід:** модель перепише ваше речення в стилі STATE (логічний, фактологічний). Спробуйте також `VALUE`, `FORM`, `FORCE`.

## 6. Запустіть API сервер та перевірте ендпоінти

У першому терміналі:

```bash
nous serve --port 8000
```

У другому терміналі (або через браузер):

```bash
# Health check
curl http://localhost:8000/health

# Аналіз тексту
curl -X POST http://localhost:8000/analyze/text -H "Content-Type: application/json" -d "{\"text\": \"I think logically about the east\"}"
```

**Очікуваний вивід:** JSON з `subit_id`, `archetype_name`, `mode`, `coordinates`.

## 7. Протестуйте Git hooks (опціонально)

```bash
# У корені вашого Git-репозиторію (наприклад, сам проект)
nous hooks install .

# Зробіть будь-яку зміну, додайте та закомітьте
git add .
git commit -m "Test hooks"
```

Після коміту автоматично запуститься `nous analyze .` – ви побачите повідомлення про побудову графа.

## 8. Запустіть формальні тести (pytest)

```bash
pytest tests/ -v
```

Якщо тестів ще мало, ви можете створити простий тест алгебри:

```python
# tests/test_algebra.py
from subit_nous.subit_algebra import Subit

def test_xor():
    a = Subit(0b10101010)
    b = Subit(0b11111111)
    assert a.xor(b).bits == 0b01010101
```

## 9. Переконайтеся, що всі команди доступні

```bash
nous --help
```

Має показати: `analyze`, `watch`, `serve`, `hooks`, `export`, `soft`, `control`.

## 10. (Опціонально) Видаліть тестові артефакти

```bash
rm -r -fo test_output, demo_soft.json, soft_output.json, soft_output_radar.html
```

## Підсумок

Якщо всі кроки виконані успішно, SUBIT‑NOUS v3.0 працює повністю:

- ✅ Алгебраїчне ядро (XOR, distance, flip, permute)
- ✅ Continuous SUBIT (soft, similarity, interpolation, radar)
- ✅ Локальний LLM контроль через Ollama
- ✅ API сервер
- ✅ Git hooks
- ✅ Інтерактивний граф та Obsidian експорт

