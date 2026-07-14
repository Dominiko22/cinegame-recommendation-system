from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .forms import LoginForm
from .auth_views import register_view

app_name = "recommender"

urlpatterns = [
    path("", views.home, name="home"),

    # Konta użytkowników
    path(
        "register/",
        register_view,
        name="register",
    ),
    path(
        "login/",
        LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(
            next_page="recommender:home",
        ),
        name="logout",
    ),

    # Filmy
    path("movies/", views.movie_list, name="movie_list"),
    path(
        "movies/<int:movie_id>/",
        views.movie_detail,
        name="movie_detail",
    ),

    # Gry
    path("games/", views.game_list, name="game_list"),
    path(
        "games/<int:game_id>/",
        views.game_detail,
        name="game_detail",
    ),
]
