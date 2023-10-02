from djoser.views import UserViewSet
from .subscriptions_serializer import SubscriptionsSerializer
from .models import Subscriptions, User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class CustomUserViewSet(UserViewSet):
    """
    Переопределен вьюсет из djoser.
    Добавлены специальные маршрутизируемые методы для работы с подписками.
    """

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        """
        Подписаться/отписаться от пользователя.
        """
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            # if Subscriptions.objects.filter(
            #     user=request.user,
            #     author=author
            # ).exists():
            #     return Response(
            #         {'errors': 'Вы уже подписаны на данного пользователя!'},
            #         status=status.HTTP_400_BAD_REQUEST
            #     )
            subscriptions_obj = Subscriptions.objects.create(
                user=request.user,
                author=author
            )
            serializer = SubscriptionsSerializer(
                subscriptions_obj,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            # if not Subscriptions.objects.filter(
            #     user=request.user,
            #     author=author
            # ).exists():
            #     return Response(
            #         {'errors': 'Вы не подписаны на данного пользователя!'},
            #         status=status.HTTP_400_BAD_REQUEST
            #     )
            subscriptions_obj = get_object_or_404(
                Subscriptions,
                user=request.user,
                author=author
            )
            subscriptions_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        """
        Возвращает пользователей (авторов), на которых подписан текущий
        пользователь.
        """
        subscriptions_list = Subscriptions.objects.filter(user=request.user)
        pages = self.paginate_queryset(subscriptions_list)
        serializer = SubscriptionsSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
