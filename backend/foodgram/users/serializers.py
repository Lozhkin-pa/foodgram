from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import User, Subscriptions



class CustomUserSerializer(UserSerializer):
    is_subscribed222 = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed222'
        )

    def get_is_subscribed222(self, obj):
        request = self.context.get('request')
        return Subscriptions.objects.filter(
            user=request.user,
            author=obj
        ).exists()


class CustomUserCreateSerializer(UserCreateSerializer):

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
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Subscriptions
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscriptions.objects.all(),
                fields=('user', 'author')
            )
        ]

    def validate_author(self, value):
        if value == self.context.get('request').user:
            raise serializers.ValidationError(
                'Невозможно подписаться на самого себя!'
            )
        return value


class SubscriptionsListSerializer(serializers.ModelSerializer):
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
