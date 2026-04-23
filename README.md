# JOJ Comic Generator

Генератор коміксів про кар'єрний ріст в ЗСУ на основі гри [JOJ](https://github.com/redukr/JOJ-GAME-NEW) та [ai-comic-factory](https://github.com/jbilcke-hf/ai-comic-factory).

## 🏗️ Архітектура

Гібридне рішення:
- **Backend**: Python FastAPI (робота з LLM Studio, ComfyUI, JOJ даними)
- **Frontend**: Next.js React (UI для генерації та перегляду коміксів)

## 🚀 Швидкий старт

### Передумови

1. [LLM Studio](http://localhost:1234) запущено локально
2. [ComfyUI](http://127.0.0.1:8188) запущено локально
3. [JOJ GAME](https://github.com/redukr/JOJ-GAME-NEW) клоновано поруч (`../JOJ-GAME-NEW`)
4. Node.js 18+ та Python 3.10+

### Встановлення

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend  
cd ../frontend
npm install
```

### Запуск

```bash
# Terminal 1: Backend
cd backend
python main.py
# API доступний за адресою http://localhost:8000

# Terminal 2: Frontend
cd frontend
npm run dev
# UI доступний за адресою http://localhost:3000
```

## 📁 Структура проєкту

```
comix-images/
├── backend/              # Python FastAPI
│   ├── main.py           # Точка входу
│   ├── services/         # LLM, ComfyUI, JOJ сервіси
│   └── requirements.txt  # Python залежності
├── frontend/             # Next.js
│   ├── src/              # React компоненти
│   ├── package.json      # Node залежності
│   └── next.config.js    # Next.js конфіг
├── workflows/            # ComfyUI workflows
│   └── comic_api.json    # Базовий workflow
├── data/                 # JOJ дані (символічні посилання)
│   ├── joj-ranks.json    # → JOJ-GAME-NEW/database/shared-ranks.json
│   └── joj-cards.json    # → JOJ-GAME-NEW/database/shared-deck-template.json
└── README.md
```

## 🔌 API Endpoints

### JOJ Data
- `GET /api/joj/ranks` — Список рангів ЗСУ
- `GET /api/joj/cards?category=X` — Карти за категорією
- `GET /api/joj/cards-by-rank/{rank_id}` — Карти для рангу

### LLM (через LLM Studio)
- `POST /api/llm/story` — Генерація сюжету коміксу
- `POST /api/llm/dialog` — Генерація діалогу

### ComfyUI
- `POST /api/comfy/generate` — Генерація зображення
- `GET /api/comfy/status` — Статус ComfyUI

### Comic Builder
- `POST /api/comic/build` — Повний пайплайн
- `GET /api/comic/status/{job_id}` — Статус генерації

## 🎯 Як використовувати

1. Відкрийте `http://localhost:3000`
2. Оберіть початковий та кінцевий ранги (наприклад, від Рекрута до Генерала)
3. Натисніть "Згенерувати комікс"
4. AI генерує сюжет через LLM Studio
5. Система підбирає або генерує зображення
6. Переглядайте результат та експортуйте в PDF

## 🛠️ Розробка

### Додавання нових workflow для ComfyUI

1. Збережіть workflow з ComfyUI як API JSON
2. Покладіть в `workflows/`
3. Оновіть `ComfyService._load_workflow()`

### Кастомізація промптів LLM

Редагуйте методи в `backend/services/llm_service.py`:
- `generate_comic_story()` — структура сюжету
- `generate_dialog()` — стиль діалогів

## 📝 Ліцензія

Apache-2.0 (як і оригінальний ai-comic-factory)

## 🙏 Подяки

- [ai-comic-factory](https://github.com/jbilcke-hf/ai-comic-factory) за базову архітектуру
- [JOJ GAME](https://github.com/redukr/JOJ-GAME-NEW) за ігровий всесвіт та ассети
