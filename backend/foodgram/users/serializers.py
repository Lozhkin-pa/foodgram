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
            user=request.user,
            author=obj
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


class SubscriptionsSerializer(serializers.ModelSerializer):
    """
    Данные пользователя (автора), на которого подписан текущий пользователь.
    В выдачу добавляются рецепты.
    """
    #recipes = serializers.RecipeSerializer(many=True, read_only=True)
    # recipes_count = serializers.SerializerMethodField(read_only=True)
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscriptions
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            # 'recipes',
            # 'recipes_count'
        )
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Subscriptions.objects.filter(
            user=request.user,
            author=obj.author
        ).exists()
    
    # def get_recipes_count(self, obj):
    #     return obj.recipes.count()
