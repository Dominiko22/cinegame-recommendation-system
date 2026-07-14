# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.conf import settings

# =========================================================
# WALIDATORY
# =========================================================

def validate_exactly_one_item(movie_id, game_id):
    """Wymaga wskazania dokładnie jednego obiektu: filmu albo gry."""
    if (movie_id is None) == (game_id is None):
        raise ValidationError(
            "Należy wskazać dokładnie jeden obiekt: film albo grę."
        )


# =========================================================
# UŻYTKOWNICY
# =========================================================

class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    preferences_json = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "users"

    def __str__(self):
        return self.email


# =========================================================
# SŁOWNIKI
# =========================================================

class Genres(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "genres"

    def __str__(self):
        return self.name


class Platforms(models.Model):
    platform_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "platforms"

    def __str__(self):
        return self.name


# =========================================================
# FILMY I GRY
# =========================================================

class Movies(models.Model):
    movie_id = models.BigAutoField(primary_key=True)
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

    genres = models.ManyToManyField(
        "Genres",
        through="MovieGenres",
        related_name="movies",
    )

    class Meta:
        managed = False
        db_table = "movies"

    def __str__(self):
        return self.title


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
        "Genres",
        through="GameGenres",
        related_name="games",
    )
    platforms = models.ManyToManyField(
        "Platforms",
        through="GamePlatforms",
        related_name="games",
    )

    class Meta:
        managed = False
        db_table = "games"

    def __str__(self):
        return self.title


# =========================================================
# MODELE UCZENIA MASZYNOWEGO
# =========================================================

class MlModels(models.Model):
    model_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    version = models.CharField(max_length=50)
    algorithm_type = models.CharField(max_length=50)
    metrics_json = models.JSONField(blank=True, null=True)
    trained_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ml_models"
        unique_together = (("name", "version"),)

    def __str__(self):
        return f"{self.name} {self.version}"


# =========================================================
# TABELE POŚREDNIE
# =========================================================

class MovieGenres(models.Model):
    pk = models.CompositePrimaryKey("movie_id", "genre_id")

    movie = models.ForeignKey(
        "Movies",
        on_delete=models.CASCADE,
        db_column="movie_id",
        related_name="genre_links",
    )
    genre = models.ForeignKey(
        "Genres",
        on_delete=models.CASCADE,
        db_column="genre_id",
        related_name="movie_links",
    )

    class Meta:
        managed = False
        db_table = "movie_genres"

    def __str__(self):
        return f"{self.movie} - {self.genre}"


class GameGenres(models.Model):
    pk = models.CompositePrimaryKey("game_id", "genre_id")

    game = models.ForeignKey(
        "Games",
        on_delete=models.CASCADE,
        db_column="game_id",
        related_name="genre_links",
    )
    genre = models.ForeignKey(
        "Genres",
        on_delete=models.CASCADE,
        db_column="genre_id",
        related_name="game_links",
    )

    class Meta:
        managed = False
        db_table = "game_genres"

    def __str__(self):
        return f"{self.game} - {self.genre}"


class GamePlatforms(models.Model):
    pk = models.CompositePrimaryKey("game_id", "platform_id")

    game = models.ForeignKey(
        "Games",
        on_delete=models.CASCADE,
        db_column="game_id",
        related_name="platform_links",
    )
    platform = models.ForeignKey(
        "Platforms",
        on_delete=models.CASCADE,
        db_column="platform_id",
        related_name="game_links",
    )

    class Meta:
        managed = False
        db_table = "game_platforms"

    def __str__(self):
        return f"{self.game} - {self.platform}"


# =========================================================
# OCENY I INTERAKCJE
# =========================================================

class Ratings(models.Model):
    rating_id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="ratings",
    )
    movie = models.ForeignKey(
        "Movies",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="ratings",
    )
    game = models.ForeignKey(
        "Games",
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
        managed = False
        db_table = "ratings"
        unique_together = (
            ("user", "movie"),
            ("user", "game"),
        )

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
        "Movies",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="interactions",
    )
    game = models.ForeignKey(
        "Games",
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
        managed = False
        db_table = "interactions"

    def clean(self):
        super().clean()
        validate_exactly_one_item(self.movie_id, self.game_id)

    def __str__(self):
        item = self.movie or self.game
        return f"{self.user} - {self.interaction_type} - {item}"


# =========================================================
# REKOMENDACJE
# =========================================================

class Recommendations(models.Model):
    recommendation_id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="recommendations",
    )
    model = models.ForeignKey(
        "MlModels",
        on_delete=models.RESTRICT,
        related_name="recommendations",
    )

    generated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = "recommendations"

    def __str__(self):
        return f"Rekomendacja {self.recommendation_id} dla {self.user}"


class RecommendationItems(models.Model):
    recommendation_item_id = models.BigAutoField(primary_key=True)

    recommendation = models.ForeignKey(
        "Recommendations",
        on_delete=models.CASCADE,
        related_name="items",
    )
    movie = models.ForeignKey(
        "Movies",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="recommendation_items",
    )
    game = models.ForeignKey(
        "Games",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="recommendation_items",
    )

    predicted_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    position = models.SmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        managed = False
        db_table = "recommendation_items"
        unique_together = (
            ("recommendation", "position"),
            ("recommendation", "movie"),
            ("recommendation", "game"),
        )

    def clean(self):
        super().clean()
        validate_exactly_one_item(self.movie_id, self.game_id)

    def __str__(self):
        item = self.movie or self.game
        return f"{self.position}. {item} ({self.predicted_score:.3f})"
