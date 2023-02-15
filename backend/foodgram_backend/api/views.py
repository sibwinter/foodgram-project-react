from api.serializers import TagSerializer
from recipes.models import Recipes, Tag
from rest_framework import filters, permissions, status, viewsets


class TagViewSet(viewsets.ModelViewSet):
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
