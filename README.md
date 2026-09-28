# Anime Bot

Telegram-бот для любителей аниме: случайные тайтлы, поиск по названию, описания, жанры. С подпиской и расширенными функциями.

## Возможности

### Бесплатно
- Случайное аниме с постером, жанрами и оценкой
- Краткое описание
- Поиск по названию
- Карточка аниме со ссылкой на Shikimori

### По подписке (в разработке)
- Без дневного лимита
- Списки: «Смотрю», «Буду смотреть», «Просмотрено»
- Избранное
- Уведомления о новых сериях
- Расширенные фильтры (жанр, год, тип)

## Стек

- Python 3.12
- aiogram 3
- aiohttp
- SQLite + SQLAlchemy (план)
- Telegram Stars (план, для оплаты)

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
├── README.md
├── bot.db                 
└── handlers/
    ├── __init__.py
    ├── routes.py           # склейка роутеров
    ├── random.py           # /start + рандом + кнопка «Ещё аниме»
    ├── search.py           # поиск с FSM
    ├── description.py      # описание + кнопка «Назад»
    ├── profile.py          # профиль пользователя
    ├── sender.py           # отправка карточек аниме
    ├── keyboards.py        # все клавиатуры
    ├── api.py              # запросы к Shikimori API
    ├── db.py               # SQLite: users, статистика
    └── utils.py            # утилиты: форматирование, чистка описаний
```

## Roadmap

- [x] Случайное аниме
- [x] Кнопка «Ещё аниме»
- [x] Жанры и описания
- [x] Поиск по названию
- [ ] Рандом по жанру
- [x] База данных (SQLite)
- [x] Регистрация / профиль
- [ ] Списки аниме
- [ ] Подписка через Telegram Stars
- [ ] Эксклюзивные функции для подписчиков

## Devlog

Прогресс разработки — в Telegram-канале: [L.S Devlog](https://t.me/твой_канал)

## Лицензия

MIT
