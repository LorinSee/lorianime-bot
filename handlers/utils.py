import re
from html import escape

KIND_NAMES = {
    "tv": "Сериал",
    "movie": "Фильм",
    "ova": "OVA",
    "ona": "ONA",
    "special": "Спецвыпуск",
    "tv_special": "ТВ-спешл",
    "music": "Клип",
    "pv": "Промо",
}

STATUS_NAMES = {
    "released": "Вышло",
    "ongoing": "Выходит",
    "anons": "Анонс",
}


def plural_episodes(n):
    if n % 10 == 1 and n % 100 != 11:
        return f"{n} серия"
    if 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        return f"{n} серии"
    return f"{n} серий"


def get_episodes_text(kind, kind_text, status, episodes, episodes_aired):
    if kind in ("movie", "music", "pv"):
        return ""
    if episodes == 0 and episodes_aired == 0:
        return "\nКоличество серий: Неизвестно"
    if status == "anons":
        return f"\nКоличество серий: Анонс ({plural_episodes(episodes)} запланировано)"
    if status == "released":
        if episodes > 0:
            return f"\nКоличество серий: {plural_episodes(episodes)}"
        return "\nКоличество серий: Неизвестно"
    if episodes_aired > 0 and episodes > 0:
        return f"\nКоличество серий: {episodes_aired} из {episodes} (выходит)"
    if episodes > 0:
        return f"\nКоличество серий: Выходит ({plural_episodes(episodes)})"
    return "\nКоличество серий: Выходит"


def get_image_url(anime):
    image_data = anime.get("image", {})
    image_url = image_data.get("original") or image_data.get("preview")
    if not image_url or "missing_original" in image_url:
        return None
    if image_url.startswith("/"):
        image_url = "https://shikimori.one" + image_url
    return image_url


def get_genres_text(anime):
    genres = anime.get("genres", [])
    if not genres:
        return "Не указаны"
    return ", ".join(g.get("russian") or g.get("name", "") for g in genres)


def clean_description(text):
    if not text:
        return "Нет описания"
    text = re.sub(r"\[anime=\d+\](.*?)\[/anime\]", r"\1", text)
    text = re.sub(r"\[character=\d+\](.*?)\[/character\]", r"\1", text)
    text = re.sub(r"\[.*?\]", "", text)
    return text.strip()


def build_caption(anime):
    title = escape(anime.get("russian") or anime.get("name", "Нет названия"))
    score = anime.get("score", "unknown")
    status = anime.get("status", "unknown")
    status_text = escape(STATUS_NAMES.get(status, status))
    episodes = anime.get("episodes", 0)
    episodes_aired = anime.get("episodes_aired", 0)
    kind = anime.get("kind", "unknown")
    kind_text = escape(KIND_NAMES.get(kind, kind))

    genres_text = escape(get_genres_text(anime))
    episodes_text = escape(
        get_episodes_text(kind, kind_text, status, episodes, episodes_aired)
    )
    anime_url = "https://shikimori.one" + anime.get("url", "")

    return (
        f"<b>Название:</b> {title}\n\n"
        f"<b>Тип:</b> {kind_text}\n"
        f"<b>Статус:</b> {status_text}\n"
        f"<b>Жанры:</b> {genres_text}\n"
        f"<b>{episodes_text}</b>\n"
        f"<b>Оценка:</b> {score}\n\n"
        f"<b>Ссылка на аниме:</b> {anime_url}"
    )
