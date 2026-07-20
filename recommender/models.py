from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


def validate_exactly_one_item(movie_id, game_id):
    """Wymaga wskazania dokładnie jednego obiektu: filmu albo gry."""
    if (movie_id is None) == (game_id is None):
        raise ValidationError(
            "Należy wskazać dokładnie jeden obiekt: film albo grę."
        )


class Genres(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        db_table = "genres"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Platforms(models.Model):
    platform_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        db_table = "platforms"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Movies(models.Model):
    movie_id = models.BigAutoField(primary_key=True)
    tmdb_id = models.PositiveIntegerField(
        unique=True,
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1888), MaxValueValidator(2100)],
    )
    director = models.CharField(max_length=150, blank=True, null=True)
    duration_min = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
    )
    description = models.TextField(blank=True, null=True)

    poster_path = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    genres = models.ManyToManyField(
        Genres,
        through="MovieGenres",
        related_name="movies",
        blank=True,
    )
    

    class Meta:
        db_table = "movies"
        ordering = ["title"]

    def __str__(self):
        return self.title
    
    @property
    def poster_url(self):
        if not self.poster_path:
            return None

        return f"https://image.tmdb.org/t/p/w500{self.poster_path}"


class Games(models.Model):
    game_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1950), MaxValueValidator(2100)],
    )
    developer = models.CharField(max_length=150, blank=True, null=True)
    publisher = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    genres = models.ManyToManyField(
        Genres,
        through="GameGenres",
        related_name="games",
        blank=True,
    )
    platforms = models.ManyToManyField(
        Platforms,
        through="GamePlatforms",
        related_name="games",
        blank=True,
    )

    class Meta:
        db_table = "games"
        ordering = ["title"]

    def __str__(self):
        return self.title


class MlModels(models.Model):
    model_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    version = models.CharField(max_length=50)
    algorithm_type = models.CharField(max_length=50)
    metrics_json = models.JSONField(blank=True, null=True)
    trained_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "ml_models"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "version"],
                name="unique_ml_model_name_version",
            )
        ]
        ordering = ["name", "version"]

    def __str__(self):
        return f"{self.name} {self.version}"


class MovieGenres(models.Model):
    movie = models.ForeignKey(
        Movies,
        on_delete=models.CASCADE,
        db_column="movie_id",
        related_name="genre_links",
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        db_column="genre_id",
        related_name="movie_links",
    )

    class Meta:
        db_table = "movie_genres"
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "genre"],
                name="unique_movie_genre",
            )
        ]

    def __str__(self):
        return f"{self.movie} - {self.genre}"


class GameGenres(models.Model):
    game = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
        db_column="game_id",
        related_name="genre_links",
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        db_column="genre_id",
        related_name="game_links",
    )

    class Meta:
        db_table = "game_genres"
        constraints = [
            models.UniqueConstraint(
                fields=["game", "genre"],
                name="unique_game_genre",
            )
        ]

    def __str__(self):
        return f"{self.game} - {self.genre}"


class GamePlatforms(models.Model):
    game = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
        db_column="game_id",
        related_name="platform_links",
    )
    platform = models.ForeignKey(
        Platforms,
        on_delete=models.CASCADE,
        db_column="platform_id",
        related_name="game_links",
    )

    class Meta:
        db_table = "game_platforms"
        constraints = [
            models.UniqueConstraint(
                fields=["game", "platform"],
                name="unique_game_platform",
            )
        ]

    def __str__(self):
        return f"{self.game} - {self.platform}"


class Ratings(models.Model):
    rating_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="ratings",
    )
    movie = models.ForeignKey(
        Movies,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="ratings",
    )
    game = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="ratings",
    )
    score = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    rated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "ratings"
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(movie__isnull=False, game__isnull=True)
                    | models.Q(movie__isnull=True, game__isnull=False)
                ),
                name="rating_has_exactly_one_item",
            ),
            models.UniqueConstraint(
                fields=["user", "movie"],
                condition=models.Q(movie__isnull=False),
                name="unique_user_movie_rating",
            ),
            models.UniqueConstraint(
                fields=["user", "game"],
                condition=models.Q(game__isnull=False),
                name="unique_user_game_rating",
            ),
        ]

    def clean(self):
        super().clean()
        validate_exactly_one_item(self.movie_id, self.game_id)

    def __str__(self):
        item = self.movie or self.game
        return f"{self.user} - {item}: {self.score}/10"


class Interactions(models.Model):
    class InteractionType(models.TextChoices):
        VIEW = "view", "Wyświetlenie"
        CLICK = "click", "Kliknięcie"
        LIKE = "like", "Polubienie"
        DISLIKE = "dislike", "Brak polubienia"
        FAVORITE = "favorite", "Ulubione"
        WATCHLIST = "watchlist", "Lista do obejrzenia"
        WATCH = "watch", "Obejrzenie"
        PLAY = "play", "Uruchomienie gry"
        SKIP = "skip", "Pominięcie"

    interaction_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="interactions",
    )
    movie = models.ForeignKey(
        Movies,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="interactions",
    )
    game = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="interactions",
    )
    interaction_type = models.CharField(
        max_length=30,
        choices=InteractionType.choices,
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "interactions"
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(movie__isnull=False, game__isnull=True)
                    | models.Q(movie__isnull=True, game__isnull=False)
                ),
                name="interaction_has_exactly_one_item",
            )
        ]

    def clean(self):
        super().clean()
        validate_exactly_one_item(self.movie_id, self.game_id)

    def __str__(self):
        item = self.movie or self.game
        return f"{self.user} - {self.interaction_type} - {item}"


class Recommendations(models.Model):
    recommendation_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="recommendations",
    )
    model = models.ForeignKey(
        MlModels,
        on_delete=models.RESTRICT,
        related_name="recommendations",
    )
    generated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "recommendations"
        ordering = ["-generated_at"]

    def __str__(self):
        return f"Rekomendacja {self.recommendation_id} dla {self.user}"


class RecommendationItems(models.Model):
    recommendation_item_id = models.BigAutoField(primary_key=True)
    recommendation = models.ForeignKey(
        Recommendations,
        on_delete=models.CASCADE,
        related_name="items",
    )
    movie = models.ForeignKey(
        Movies,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="recommendation_items",
    )
    game = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="recommendation_items",
    )
    predicted_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    position = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        db_table = "recommendation_items"
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(movie__isnull=False, game__isnull=True)
                    | models.Q(movie__isnull=True, game__isnull=False)
                ),
                name="recommendation_item_has_exactly_one_item",
            ),
            models.UniqueConstraint(
                fields=["recommendation", "position"],
                name="unique_recommendation_position",
            ),
            models.UniqueConstraint(
                fields=["recommendation", "movie"],
                condition=models.Q(movie__isnull=False),
                name="unique_recommendation_movie",
            ),
            models.UniqueConstraint(
                fields=["recommendation", "game"],
                condition=models.Q(game__isnull=False),
                name="unique_recommendation_game",
            ),
        ]
        ordering = ["position"]

    def clean(self):
        super().clean()
        validate_exactly_one_item(self.movie_id, self.game_id)

    def __str__(self):
        item = self.movie or self.game
        return f"{self.position}. {item} ({self.predicted_score:.3f})"
