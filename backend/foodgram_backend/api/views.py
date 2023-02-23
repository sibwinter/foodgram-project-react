from api.serializers import RecipeListSerializer, TagSerializer, IngredientSerializer
from recipes.models import Recipes, Tag, Ingredient
from rest_framework import filters, permissions, status, viewsets


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipeListSerializer