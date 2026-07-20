from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .forms import RegisterForm
from .models import Games, Genres, MovieGenres, Movies, Ratings


class CatalogViewsTests(TestCase):
    def setUp(self):
        self.movie = Movies.objects.create(
            title="Matrix",
            release_year=1999,
            director="Lana Wachowski, Lilly Wachowski",
            duration_min=136,
        )
        self.game = Games.objects.create(
            title="The Witcher 3",
            release_year=2015,
            developer="CD Projekt Red",
        )

    def test_home_page_displays_movies_and_games(self):
        response = self.client.get(reverse("recommender:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie.title)
        self.assertContains(response, self.game.title)

    def test_movie_search_filters_by_title(self):
        Movies.objects.create(title="Inception", release_year=2010)

        response = self.client.get(
            reverse("recommender:movie_list"),
            {"q": "mat"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Matrix")
        self.assertNotContains(response, "Inception")

    def test_movie_detail_displays_related_genres(self):
        genre = Genres.objects.create(name="Science fiction")
        MovieGenres.objects.create(movie=self.movie, genre=genre)

        response = self.client.get(
            reverse(
                "recommender:movie_detail",
                kwargs={"movie_id": self.movie.movie_id},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Science fiction")


class RegistrationFormTests(TestCase):
    def test_register_form_rejects_duplicate_email(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username="existing",
            email="test@example.com",
            password="example-password-123",
        )

        form = RegisterForm(
            data={
                "username": "new-user",
                "email": "TEST@example.com",
                "password1": "example-password-123",
                "password2": "example-password-123",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class RatingModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="reader",
            password="example-password-123",
        )
        self.movie = Movies.objects.create(title="Interstellar")
        self.game = Games.objects.create(title="Portal 2")

    def test_rating_must_reference_exactly_one_item(self):
        invalid_rating = Ratings(user=self.user, score=8)

        with self.assertRaises(ValidationError):
            invalid_rating.full_clean()

        invalid_rating.movie = self.movie
        invalid_rating.game = self.game

        with self.assertRaises(ValidationError):
            invalid_rating.full_clean()

    def test_movie_rating_is_valid(self):
        rating = Ratings(user=self.user, movie=self.movie, score=9)

        rating.full_clean()
