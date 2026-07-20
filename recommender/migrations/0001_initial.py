# Generated for a Django-managed project schema.

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Games",
            fields=[
                ("game_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                (
                    "release_year",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1950),
                            django.core.validators.MaxValueValidator(2100),
                        ],
                    ),
                ),
                ("developer", models.CharField(blank=True, max_length=150, null=True)),
                ("publisher", models.CharField(blank=True, max_length=150, null=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "games",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Genres",
            fields=[
                ("genre_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=150, unique=True)),
            ],
            options={
                "db_table": "genres",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="MlModels",
            fields=[
                ("model_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=150)),
                ("version", models.CharField(max_length=50)),
                ("algorithm_type", models.CharField(max_length=50)),
                ("metrics_json", models.JSONField(blank=True, null=True)),
                ("trained_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "ml_models",
                "ordering": ["name", "version"],
            },
        ),
        migrations.CreateModel(
            name="Movies",
            fields=[
                ("movie_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                (
                    "release_year",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1888),
                            django.core.validators.MaxValueValidator(2100),
                        ],
                    ),
                ),
                ("director", models.CharField(blank=True, max_length=150, null=True)),
                (
                    "duration_min",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "movies",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Platforms",
            fields=[
                ("platform_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=150, unique=True)),
            ],
            options={
                "db_table": "platforms",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="GameGenres",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        db_column="game_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="genre_links",
                        to="recommender.games",
                    ),
                ),
                (
                    "genre",
                    models.ForeignKey(
                        db_column="genre_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="game_links",
                        to="recommender.genres",
                    ),
                ),
            ],
            options={
                "db_table": "game_genres",
            },
        ),
        migrations.CreateModel(
            name="GamePlatforms",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        db_column="game_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="platform_links",
                        to="recommender.games",
                    ),
                ),
                (
                    "platform",
                    models.ForeignKey(
                        db_column="platform_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="game_links",
                        to="recommender.platforms",
                    ),
                ),
            ],
            options={
                "db_table": "game_platforms",
            },
        ),
        migrations.CreateModel(
            name="MovieGenres",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "genre",
                    models.ForeignKey(
                        db_column="genre_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="movie_links",
                        to="recommender.genres",
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        db_column="movie_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="genre_links",
                        to="recommender.movies",
                    ),
                ),
            ],
            options={
                "db_table": "movie_genres",
            },
        ),
        migrations.CreateModel(
            name="Interactions",
            fields=[
                (
                    "interaction_id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                (
                    "interaction_type",
                    models.CharField(
                        choices=[
                            ("view", "Wyświetlenie"),
                            ("click", "Kliknięcie"),
                            ("like", "Polubienie"),
                            ("dislike", "Brak polubienia"),
                            ("favorite", "Ulubione"),
                            ("watchlist", "Lista do obejrzenia"),
                            ("watch", "Obejrzenie"),
                            ("play", "Uruchomienie gry"),
                            ("skip", "Pominięcie"),
                        ],
                        max_length=30,
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "game",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interactions",
                        to="recommender.games",
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interactions",
                        to="recommender.movies",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interactions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "interactions",
            },
        ),
        migrations.CreateModel(
            name="Ratings",
            fields=[
                ("rating_id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "score",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ]
                    ),
                ),
                ("rated_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "game",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="recommender.games",
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="recommender.movies",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "ratings",
            },
        ),
        migrations.CreateModel(
            name="Recommendations",
            fields=[
                (
                    "recommendation_id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("generated_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="recommendations",
                        to="recommender.mlmodels",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recommendations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "recommendations",
                "ordering": ["-generated_at"],
            },
        ),
        migrations.CreateModel(
            name="RecommendationItems",
            fields=[
                (
                    "recommendation_item_id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                (
                    "predicted_score",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(1.0),
                        ]
                    ),
                ),
                (
                    "position",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recommendation_items",
                        to="recommender.games",
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="recommendation_items",
                        to="recommender.movies",
                    ),
                ),
                (
                    "recommendation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="recommender.recommendations",
                    ),
                ),
            ],
            options={
                "db_table": "recommendation_items",
                "ordering": ["position"],
            },
        ),
        migrations.AddField(
            model_name="games",
            name="genres",
            field=models.ManyToManyField(
                blank=True,
                related_name="games",
                through="recommender.GameGenres",
                to="recommender.genres",
            ),
        ),
        migrations.AddField(
            model_name="games",
            name="platforms",
            field=models.ManyToManyField(
                blank=True,
                related_name="games",
                through="recommender.GamePlatforms",
                to="recommender.platforms",
            ),
        ),
        migrations.AddField(
            model_name="movies",
            name="genres",
            field=models.ManyToManyField(
                blank=True,
                related_name="movies",
                through="recommender.MovieGenres",
                to="recommender.genres",
            ),
        ),
        migrations.AddConstraint(
            model_name="mlmodels",
            constraint=models.UniqueConstraint(
                fields=("name", "version"),
                name="unique_ml_model_name_version",
            ),
        ),
        migrations.AddConstraint(
            model_name="gamegenres",
            constraint=models.UniqueConstraint(
                fields=("game", "genre"),
                name="unique_game_genre",
            ),
        ),
        migrations.AddConstraint(
            model_name="gameplatforms",
            constraint=models.UniqueConstraint(
                fields=("game", "platform"),
                name="unique_game_platform",
            ),
        ),
        migrations.AddConstraint(
            model_name="moviegenres",
            constraint=models.UniqueConstraint(
                fields=("movie", "genre"),
                name="unique_movie_genre",
            ),
        ),
        migrations.AddConstraint(
            model_name="interactions",
            constraint=models.CheckConstraint(
                condition=(
                    models.Q(("game__isnull", True), ("movie__isnull", False))
                    | models.Q(("game__isnull", False), ("movie__isnull", True))
                ),
                name="interaction_has_exactly_one_item",
            ),
        ),
        migrations.AddConstraint(
            model_name="ratings",
            constraint=models.CheckConstraint(
                condition=(
                    models.Q(("game__isnull", True), ("movie__isnull", False))
                    | models.Q(("game__isnull", False), ("movie__isnull", True))
                ),
                name="rating_has_exactly_one_item",
            ),
        ),
        migrations.AddConstraint(
            model_name="ratings",
            constraint=models.UniqueConstraint(
                condition=models.Q(("movie__isnull", False)),
                fields=("user", "movie"),
                name="unique_user_movie_rating",
            ),
        ),
        migrations.AddConstraint(
            model_name="ratings",
            constraint=models.UniqueConstraint(
                condition=models.Q(("game__isnull", False)),
                fields=("user", "game"),
                name="unique_user_game_rating",
            ),
        ),
        migrations.AddConstraint(
            model_name="recommendationitems",
            constraint=models.CheckConstraint(
                condition=(
                    models.Q(("game__isnull", True), ("movie__isnull", False))
                    | models.Q(("game__isnull", False), ("movie__isnull", True))
                ),
                name="recommendation_item_has_exactly_one_item",
            ),
        ),
        migrations.AddConstraint(
            model_name="recommendationitems",
            constraint=models.UniqueConstraint(
                fields=("recommendation", "position"),
                name="unique_recommendation_position",
            ),
        ),
        migrations.AddConstraint(
            model_name="recommendationitems",
            constraint=models.UniqueConstraint(
                condition=models.Q(("movie__isnull", False)),
                fields=("recommendation", "movie"),
                name="unique_recommendation_movie",
            ),
        ),
        migrations.AddConstraint(
            model_name="recommendationitems",
            constraint=models.UniqueConstraint(
                condition=models.Q(("game__isnull", False)),
                fields=("recommendation", "game"),
                name="unique_recommendation_game",
            ),
        ),
    ]
