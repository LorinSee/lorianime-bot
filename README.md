# Anime Bot

Telegram-бот для любителей аниме: случайные тайтлы, рандом по жанру, поиск по названию, описания, жанры, профиль, избранное. С подпиской и расширенными функциями.

## Возможности

### Бесплатно
- Случайное аниме с постером, жанрами и оценкой
- Рандом по жанру
- Профиль
- Избранное
- Изменение имени и "О себе"
- Краткое описание
- Поиск по названию
- Карточка аниме со ссылкой на Shikimori
- 
## Стек

- Python 3.12
- aiogram 3
- aiohttp
- Shikimori GraphQL API
- SQLite + aiosqlite

## Установка

1. Клонируй репозиторий:

   ```
   git clone https://github.com/LorinSee/lorianime-bot.git
   cd lorianime-bot
   ```

2. Создай виртуальное окружение:

   ```
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # Linux/Mac
   ```

3. Установи зависимости:

   ```
   pip install -r requirements.txt
   ```

4. Создай `.env` на основе `.env.example` и вставь свой токен:

   ```
   BOT_TOKEN=твой_токен_от_BotFather
   ```

5. Запусти:

   ```
   python main.py
   ```

## Структура проекта

```
LoriAnimeBot/
├── main.py                
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── app/
    ├── __init__.py
    ├── routes.py           # склейка роутеров
    ├── db.py               # SQLite: users, статистика
    ├── api.py              # запросы к Shikimori API
    ├── utils.py            # утилиты: форматирование, чистка описаний
    ├── keyboards.py        # все клавиатуры
    ├── sender.py           # отправка карточек аниме
    └── handlers/
        ├── __init__.py
        ├── random.py       # /start + рандом + кнопка «Ещё аниме»
        ├── search.py       # поиск с FSM
        ├── description.py  # описание + кнопка «Назад»
        ├── favorites.py    # Избранное
        └── profile.py      # профиль пользователя
```

## Лицензия

MIT
