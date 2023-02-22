from api.views import (TagViewSet, IngredientViewSet)
from django.urls import include, path
from rest_framework import routers

app_name = 'api'


router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),
]