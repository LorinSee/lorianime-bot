import aiohttp

HEADERS = {"User-Agent": "AnimeBot (contact: lorinsee76@gmail.com)"}


async def fetch_random_anime():
    url = "https://shikimori.one/api/animes?order=random&limit=1"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            data = await resp.json()

        if not data or not isinstance(data, list):
            return None

        anime_id = data[0].get("id")
        if not anime_id:
            return None

        detail_url = (
            f"https://shikimori.one/api/animes/{anime_id}?include=genres,description"
        )
        async with session.get(detail_url, headers=HEADERS) as resp:
            detail = await resp.json()

    return detail


async def fetch_anime_by_id(anime_id):
    url = f"https://shikimori.one/api/animes/{anime_id}?include=genres,description"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            data = await resp.json()

    if not data or not isinstance(data, dict):
        return None
    return data


async def fetch_anime_search(query):
    url = f"https://shikimori.one/api/animes?search={query}&limit=10"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            data = await resp.json()

    if not data or not isinstance(data, list):
        return None
    return data
