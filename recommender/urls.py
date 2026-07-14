from django.urls import path
from . import views

app_name = "recommender"

urlpatterns = [
    path("", views.home, name="home"),

    path("movies/", views.movie_list, name="movie_list"),
    path(
        "movies/<int:movie_id>/",
        views.movie_detail,
        name="movie_detail",
    ),

    path("games/", views.game_list, name="game_list"),
    path(
        "games/<int:game_id>/",
        views.game_detail,
        name="game_detail",
    ),
]