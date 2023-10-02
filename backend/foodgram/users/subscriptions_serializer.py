"""
SubscriptionsSerializer вынес в отдельный файл для избежания циклического
импорта между users.serializers и recipes.serializers.
"""
from rest_framework import serializers
from .models import Subscriptions
# from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
# from rest_framework.response import Response


class SubscriptionsSerializer(serializers.ModelSerializer):
    """
    Данные пользователя (автора), на которого подписан текущий пользователь.
    В выдачу добавляются рецепты.
    """
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    def validate(self, data):
        request = self.context.get('request')
        author = data.get('author')
        if request.user == author:
            return serializers.ValidationError(
                'Действия с собственным профилем невозможны!'
            )
        return data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return obj.subscribers.filter(user=request.user).exists()
        # return Subscriptions.objects.filter(
        #     user=request.user,
        #     author=obj.author
        # ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        # recipes = Recipe.objects.filter(author=obj.author)
        recipes = obj.recipes.filter(author=obj.author)
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        # recipes = Recipe.objects.filter(author=obj.author)
        recipes = obj.recipes.filter(author=obj.author)
        return recipes.count()

    class Meta:
        model = Subscriptions
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
