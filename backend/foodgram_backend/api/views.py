from django.shortcuts import get_object_or_404
from requests import Response
from api.serializers import RecipeListSerializer, RecipeSerializer, TagSerializer, IngredientSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from recipes.models import Recipes, Tag, Ingredient, Favourite


class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            if (Favourite.objects.filter(user=request.user, recipe__id=pk)).exists():
                return Response({'errors': 'Рецепт уже добавлен!'},
                                status=status.HTTP_400_BAD_REQUEST)
            recipe = get_object_or_404(Recipes, id=pk)
            Favourite.objects.create(user=request.user, recipe=recipe)
            serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)