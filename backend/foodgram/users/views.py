from djoser.views import UserViewSet
from .serializers import CustomUserSerializer, SubscriptionsSerializer, SubscriptionsListSerializer
from .models import Subscriptions, User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


# class FollowViewSet(UserViewSet):
#     serializer_class = SubscriptionsSerializer

#     def get_queryset(self):
#         return Subscriptions.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class CustomUserViewSet(UserViewSet):
    # queryset = User.objects.all()
    pagination_class = PageNumberPagination

    @action(
        detail=True,
        methods=['post', 'delete'],
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        
        if request.user == author:
            return Response(
                {'errors': 'Действия с собственным профилем невозможны!'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.method == 'POST':
            if Subscriptions.objects.filter(user=request.user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на данного пользователя!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscription_obj = Subscriptions.objects.create(user=request.user, author=author)

            serializer = SubscriptionsListSerializer(
                subscription_obj, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not Subscriptions.objects.filter(user=request.user, author=author).exists():
                return Response(
                    {'errors': 'Вы не подписаны на данного пользователя!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscription_obj = get_object_or_404(
                Subscriptions, user=request.user, author=author
            )
            subscription_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
    )
    def subscriptions(self, request):
        user = request.user
        # queryset = user.subscriptions.all()
        queryset = Subscriptions.objects.filter(user=user)
        # subscriptions = User.objects.filter(subscribers__user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionsListSerializer(pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)
    
        # obj = User.objects.filter(author=request.user)
        # serializer = SubscriptionsListSerializer(data=obj)
        # serializer.is_valid()
        # return Response(serializer.data)
