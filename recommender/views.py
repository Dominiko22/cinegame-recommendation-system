from django.shortcuts import get_object_or_404, render

from .models import Games, Movies


def home(request):
    movies = Movies.objects.all().order_by("title")[:4]
    games = Games.objects.all().order_by("title")[:4]

    context = {
        "movies": movies,
        "games": games,
    }

    return render(request, "recommender/home.html", context)

def movie_list(request):
    query = request.GET.get("q", "").strip()

    movies = Movies.objects.all().order_by("title")

    if query:
        movies = movies.filter(title__icontains=query)

    return render(
        request,
        "recommender/movie_list.html",
        {
            "movies":movies,
            "query":query,
        },
    )


def game_list(request):
    query = request.GET.get("q", "").strip()

    games = Games.objects.all().order_by("title")

    if query:
        games = games.filter(title__icontains=query)

    return render(
        request,
        "recommender/game_list.html",
        {
            "games": games,
            "query": query,
        },
    )

def movie_detail(request, movie_id):
    movie = get_object_or_404(
        Movies,
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
        Games,
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
