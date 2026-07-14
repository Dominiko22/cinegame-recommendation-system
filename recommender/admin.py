from django.contrib import admin

# Register your models here.
from .models import (
    Games,
    Genres,
    Interactions,
    MlModels,
    Movies,
    Platforms,
    Ratings,
    RecommendationItems,
    Recommendations,
)

admin.site.register(Movies)
admin.site.register(Games)
admin.site.register(Genres)
admin.site.register(Platforms)
admin.site.register(Ratings)
admin.site.register(Interactions)
admin.site.register(MlModels)
admin.site.register(Recommendations)
admin.site.register(RecommendationItems)
