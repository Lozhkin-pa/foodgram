from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from .models import User, Subscriptions


class CustomUserSerializer(UserSerializer):
    """
    Переопределяем набор полей сериализатора пользователя из djoser.
    """
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Subscriptions.objects.filter(
            user=request.user.id,
            author=obj.id
        ).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Переопределяем набор полей сериализатора создания пользователя из djoser.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
