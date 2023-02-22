from djoser.views import UserViewSet
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework import status
from rest_framework.response import Response

from api.pagination import CustomPageNumberPagination
from users.models import Follow, User
from .serializers import CustomUserSerializer, FollowSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


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


class FollowingViewSet(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
