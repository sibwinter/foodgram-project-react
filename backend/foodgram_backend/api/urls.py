from api.views import (TagViewSet)
from django.urls import include, path
from rest_framework import routers

app_name = 'api'


router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')


urlpatterns = [
    path('', include(router.urls)),
]