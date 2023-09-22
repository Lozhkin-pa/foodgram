from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Tag, Ingredient, Recipe, TagRecipe, IngredientRecipe, Favorite, Shopping_cart
from users.serializers import CustomUserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class TagsRecipesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='tag.id', read_only=True)
    name = serializers.CharField(source='tag.name', read_only=True)
    color = serializers.CharField(source='tag.color', read_only=True)
    slug = serializers.SlugField(source='tag.slug', read_only=True)

    class Meta:
        model = TagRecipe
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipesReadSerializer(serializers.ModelSerializer):
    tags = TagsRecipesSerializer(source='recipe_tags', many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientsRecipeSerializer(source='recipe_ingredients', many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return Favorite.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return Shopping_cart.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()
