from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from djoser.views import UserViewSet

from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework import status
from rest_framework.response import Response

from api.serializers import RecipeListSerializer, RecipeSerializer, TagSerializer, IngredientSerializer
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.pagination import CustomPageNumberPagination
from users.models import Follow, User
from recipes.models import Recipes, Tag, Ingredient, Favourite
from .serializers import CustomUserCreateSerializer, CustomUserSerializer, FollowSerializer, SetPasswordSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('subscriptions', 'subscribe'):
            return FollowSerializer
        if self.action in ('list', 'retrieve', 'me'):
            return CustomUserSerializer
        if self.action == 'set_password':
            return SetPasswordSerializer
        return CustomUserCreateSerializer

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(
        detail=False,
        methods=['POST'],
        permission_classes=[IsAuthenticated]
    )
    def set_password(self, request):
        user = request.user
        data = request.data
        serializer = self.get_serializer(user=user, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(
            {
                'detail': 'Пароль успешно изменен'
            },
            status=status.HTTP_204_NO_CONTENT
        )


class FollowViewSet(APIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def post(self, request,  *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user_id:
            return Response(
                {'error': 'Нельзя подписаться на себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(
            user=request.user,
            author_id=user_id
        ).exists():
            return Response(
                {'error': 'Вы же подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, id=user_id)
        Follow.objects.create(
            user=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request,  *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        subscription = Follow.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'error': 'Вы не подписаны на данного пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )


class FollowListView(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


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
    
