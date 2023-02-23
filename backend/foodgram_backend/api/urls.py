from api.views import (RecipeViewSet, TagViewSet, IngredientViewSet)
from django.urls import include, path
from rest_framework import routers

app_name = 'api'


router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
]