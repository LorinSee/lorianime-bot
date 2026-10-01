import random

import aiohttp

HEADERS = {"User-Agent": "AnimeBot (contact: lorinsee76@gmail.com)"}


ANIME_FIELDS = """
    id
    name
    russian
    description
    poster { originalUrl }
    url
    kind
    score
    status
    episodes
    episodesAired
    airedOn { year month day }
    genres { id name russian }
"""


async def graphql_request(query: str, variables: dict = None):
    url = "https://shikimori.one/api/graphql"
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=HEADERS) as resp:
            data = await resp.json()

    print("GRAPHQL RESPONSE:", data)
    return data.get("data", {})


def normalize_anime(anime):
    """Приводит GraphQL-ответ к формату REST API."""
    poster = anime.get("poster") or {}
    aired = anime.get("airedOn") or {}
    year = aired.get("year")
    aired_on = str(year) if year else None

    return {
        "id": anime.get("id"),
        "name": anime.get("name"),
        "russian": anime.get("russian"),
        "image": {"original": poster.get("originalUrl")},
        "url": anime.get("url"),
        "kind": anime.get("kind"),
        "score": anime.get("score"),
        "status": anime.get("status"),
        "episodes": anime.get("episodes", 0),
        "episodes_aired": anime.get("episodesAired", 0),
        "aired_on": aired_on,
        "released_on": None,
        "genres": anime.get("genres", []),
        "description": anime.get("description", ""),
    }


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

    return await fetch_anime_by_id(anime_id)


async def fetch_anime_by_id(anime_id: int):
    gql = f"""
    query($ids: String) {{
        animes(ids: $ids, limit: 1) {{
            {ANIME_FIELDS}
        }}
    }}
    """
    data = await graphql_request(gql, {"ids": str(anime_id)})
    animes = data.get("animes", [])
    if not animes:
        return None
    return normalize_anime(animes[0])


async def fetch_anime_search(query: str):
    gql = f"""
    query($search: String, $limit: Int) {{
        animes(search: $search, limit: $limit) {{
            {ANIME_FIELDS}
        }}
    }}
    """
    data = await graphql_request(gql, {"search": query, "limit": 10})
    animes = data.get("animes", [])
    if not animes:
        return None
    return [normalize_anime(a) for a in animes]


async def fetch_random_by_genre(genre_id: int):
    gql = f"""
    query($genre: String, $limit: Int) {{
        animes(genre: $genre, limit: $limit) {{
            {ANIME_FIELDS}
        }}
    }}
    """
    data = await graphql_request(gql, {"genre": str(genre_id), "limit": 50})
    animes = data.get("animes", [])
    print("DATA LEN:", len(animes))

    if not animes:
        return None

    return normalize_anime(random.choice(animes))


async def fetch_genres():
    gql = """
    query {
        genres(entryType: Anime) {
            id
            name
            russian
            kind
        }
    }
    """
    data = await graphql_request(gql)
    genres = data.get("genres", [])
    print("GENRES RAW:", len(genres))
    if not genres:
        return []
    genres = [g for g in genres if g.get("kind") == "genre"]
    print("GENRES FILTERED:", len(genres))
    return genres
