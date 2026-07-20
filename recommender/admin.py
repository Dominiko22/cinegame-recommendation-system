from django.contrib import admin

from .models import (
    GameGenres,
    GamePlatforms,
    Games,
    Genres,
    Interactions,
    MlModels,
    MovieGenres,
    Movies,
    Platforms,
    Ratings,
    RecommendationItems,
    Recommendations,
)


class MovieGenresInline(admin.TabularInline):
    model = MovieGenres
    extra = 1


class GameGenresInline(admin.TabularInline):
    model = GameGenres
    extra = 1


class GamePlatformsInline(admin.TabularInline):
    model = GamePlatforms
    extra = 1


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ("title", "tmdb_id", "release_year",
                    "director", "duration_min")
    list_filter = ("release_year",)
    search_fields = ("title", "director", "description", "tmdb_id")
    inlines = [MovieGenresInline]


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "developer", "publisher")
    list_filter = ("release_year",)
    search_fields = ("title", "developer", "publisher", "description")
    inlines = [GameGenresInline, GamePlatformsInline]


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Platforms)
class PlatformsAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Ratings)
class RatingsAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "game", "score", "rated_at")
    list_filter = ("score", "rated_at")
    search_fields = ("user__username", "movie__title", "game__title")


@admin.register(Interactions)
class InteractionsAdmin(admin.ModelAdmin):
    list_display = ("user", "interaction_type", "movie", "game", "created_at")
    list_filter = ("interaction_type", "created_at")
    search_fields = ("user__username", "movie__title", "game__title")


@admin.register(MlModels)
class MlModelsAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "algorithm_type", "trained_at")
    list_filter = ("algorithm_type",)
    search_fields = ("name", "version", "algorithm_type")


class RecommendationItemsInline(admin.TabularInline):
    model = RecommendationItems
    extra = 1


@admin.register(Recommendations)
class RecommendationsAdmin(admin.ModelAdmin):
    list_display = ("recommendation_id", "user", "model", "generated_at")
    list_filter = ("model", "generated_at")
    search_fields = ("user__username", "model__name")
    inlines = [RecommendationItemsInline]


@admin.register(RecommendationItems)
class RecommendationItemsAdmin(admin.ModelAdmin):
    list_display = (
        "recommendation",
        "position",
        "movie",
        "game",
        "predicted_score",
    )
    list_filter = ("recommendation__model",)
    search_fields = ("movie__title", "game__title")
