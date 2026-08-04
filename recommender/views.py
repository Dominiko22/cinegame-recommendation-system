from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Games, Interactions, Movies, Ratings
from .forms import MovieRatingForm

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

    is_favorite = False
    user_rating = None
    rating_form = MovieRatingForm()

    if request.user.is_authenticated:
        user_rating = request.user.ratings.filter(movie=movie).first()

    if user_rating:
        rating_form = MovieRatingForm(instance=user_rating)

    if request.user.is_authenticated:
        is_favorite = request.user.interactions.filter(
            movie=movie,
            interaction_type=Interactions.InteractionType.FAVORITE,
        ).exists()

        

    context = {
        "movie": movie,
        "is_favorite": is_favorite,
        "user_rating": user_rating,
        "rating_form": rating_form,
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


@login_required
def profile(request):
    ratings = request.user.ratings.select_related(
        "movie", "game").order_by("-rated_at")[:10]

    favorites = request.user.interactions.filter(
        interaction_type="favorite"
    ).select_related("movie", "game").order_by("-created_at")[:10]

    watchlist = request.user.interactions.filter(
        interaction_type="watchlist"
    ).select_related("movie", "game").order_by("-created_at")[:10]

    context = {
        "ratings": ratings,
        "favorites": favorites,
        "watchlist": watchlist,
    }

    return render(request, "recommender/profile.html", context)


@login_required
def toggle_movie_favorite(request, movie_id):
    movie = get_object_or_404(Movies, movie_id=movie_id)

    interaction, created = Interactions.objects.get_or_create(
        user=request.user,
        movie=movie,
        interaction_type=Interactions.InteractionType.FAVORITE,
        defaults={
            "game": None,
        },
    )

    if not created:
        interaction.delete()

    return redirect("recommender:movie_detail", movie_id=movie.movie_id)


@login_required
def rate_movie(request, movie_id):
    movie = get_object_or_404(Movies, movie_id=movie_id)

    rating = request.user.ratings.filter(movie=movie).first()

    if rating is None:
        rating = Ratings(
            user=request.user,
            movie=movie,
            game=None,
        )

    if request.method == "POST":
        form = MovieRatingForm(request.POST, instance=rating)

        if form.is_valid():
            form.save()

    return redirect("recommender:movie_detail", movie_id=movie.movie_id)

