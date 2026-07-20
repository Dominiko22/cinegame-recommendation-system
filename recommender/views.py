from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Games, Movies

ITEMS_PER_PAGE = 12


def home(request):
    movies = Movies.objects.all()[:4]
    games = Games.objects.all()[:4]

    context = {
        "movies": movies,
        "games": games,
    }

    return render(request, "recommender/home.html", context)


def movie_list(request):
    query = request.GET.get("q", "").strip()

    movies = Movies.objects.all()

    if query:
        movies = movies.filter(title__icontains=query)

    paginator = Paginator(movies, ITEMS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "recommender/movie_list.html",
        {
            "movies": page_obj,
            "page_obj": page_obj,
            "query": query,
            "total_count": paginator.count,
        },
    )


def game_list(request):
    query = request.GET.get("q", "").strip()

    games = Games.objects.all()

    if query:
        games = games.filter(title__icontains=query)

    paginator = Paginator(games, ITEMS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "recommender/game_list.html",
        {
            "games": page_obj,
            "page_obj": page_obj,
            "query": query,
            "total_count": paginator.count,
        },
    )


def movie_detail(request, movie_id):
    movie = get_object_or_404(
        Movies.objects.prefetch_related("genres"),
        movie_id=movie_id,
    )

    context = {
        "movie": movie,
    }

    return render(
        request,
        "recommender/movie_detail.html",
        context,
    )


def game_detail(request, game_id):
    game = get_object_or_404(
        Games.objects.prefetch_related("genres", "platforms"),
        game_id=game_id,
    )

    context = {
        "game": game,
    }

    return render(
        request,
        "recommender/game_detail.html",
        context,
    )
