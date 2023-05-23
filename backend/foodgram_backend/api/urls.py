from api.views import (RecipeViewSet,
                       TagViewSet,
                       IngredientViewSet, UserCustomViewSet)
from django.urls import include, path
from rest_framework import routers
from djoser.views import UserViewSet

app_name = 'api'


router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('users', UserCustomViewSet, basename='users')



urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
