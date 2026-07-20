import requests
from django.conf import settings
from recommender.models import Genres, Movies

class TmdbApiError(Exception):
    pass

def search_movie(title, year=None):
    url = f"{settings.TMDB_API_BASE_URL}/search/movie"

    headers = {
        "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}",
        "accept": "application/json",
    }

    params = {
        "query": title,
        "language": settings.TMDB_LANGUAGE,
        "include_adult": "false",
        "page": 1,
    }

    if year:
        params["primary_release_year"] = year

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=20,
    )

    if response.status_code != 200:
        raise TmdbApiError(
            f"TMDb error {response.status_code}: {response.text}"
        )

    data = response.json()
    return data.get("results", [])


def get_movie_details(tmdb_id):
    url = f"{settings.TMDB_API_BASE_URL}/movie/{tmdb_id}"

    headers = {
        "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}",
        "accept": "application/json",
    }

    params = {
        "language": settings.TMDB_LANGUAGE,
        "append_to_response": "credits,external_ids",
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=20,
    )

    if response.status_code != 200:
        raise TmdbApiError(
            f"TMDb error {response.status_code}: {response.text}"
        )

    return response.json()


def parse_release_year(release_date):
    if not release_date:
        return None

    try:
        return int(release_date[:4])
    except ValueError:
        return None


def normalize_movie_data(movie):
    directors = [
        person["name"]
        for person in movie.get("credits", {}).get("crew", [])
        if person.get("job") == "Director"
    ]

    return {
        "tmdb_id": movie.get("id"),
        "title": movie.get("title") or movie.get("original_title"),
        "release_year": parse_release_year(movie.get("release_date")),
        "director": ", ".join(directors) or None,
        "duration_min": movie.get("runtime"),
        "description": movie.get("overview"),
        "poster_path": movie.get("poster_path"),
        "genres": [
            genre["name"]
            for genre in movie.get("genres", [])
        ],
    }


def save_movie(data):
    genre_names = data.pop("genres", [])

    movie = Movies.objects.create(
        title=data["title"],
        release_year=data["release_year"],
        director=data["director"],
        duration_min=data["duration_min"],
        description=data["description"],
    )

    for genre_name in genre_names:
        genre, created = Genres.objects.get_or_create(name=genre_name)
        movie.genres.add(genre)

    return movie


def save_movie(data):
    genre_names = data.pop("genres", [])

    movie, created = Movies.objects.update_or_create(
        tmdb_id=data["tmdb_id"],
        defaults={
            "title": data["title"],
            "release_year": data["release_year"],
            "director": data["director"],
            "duration_min": data["duration_min"],
            "description": data["description"],
            "poster_path": data["poster_path"],
        },
    )

    for genre_name in genre_names:
        genre, created = Genres.objects.get_or_create(name=genre_name)
        movie.genres.add(genre)

    return movie


def import_movie(title, year=None):
    results = search_movie(title, year=year)

    if not results:
        raise TmdbApiError(f"Nie znaleziono filmu: {title}")

    tmdb_id = results[0]["id"]
    details = get_movie_details(tmdb_id)
    data = normalize_movie_data(details)

    return save_movie(data)
