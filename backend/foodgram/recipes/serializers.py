from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from .utils import Base64ImageField
from users.serializers import CustomUserSerializer
from .models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientRecipe
)

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
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class IngredientsRecipeReadSerializer(serializers.ModelSerializer):
    """
    Сериализотор для выбора конкретных ингредиентов при чтении рецепта.
    """
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipesReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения рецепта.
    """
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientsRecipeReadSerializer(
        source='recipe_ingredients',
        many=True
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return obj.favorites.filter(user=request.user.id).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return obj.shopping_cart.filter(user=request.user.id).exists()

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


class IngredientsRecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализотор для записи ингредиентов к конкретному рецепту.
    """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount'
        )


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализотор для создания и редактирования рецепта.
    """
    ingredients = IngredientsRecipeCreateUpdateSerializer(
        source='recipe_ingredients',
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    def validate(self, data):
        if 'recipe_ingredients' not in data:
            raise serializers.ValidationError(
                {'errors': 'Отсутствуют ингредиенты!'}
            )
        if 'tags' not in data:
            raise serializers.ValidationError(
                {'errors': 'Отсутствуют теги!'}
            )
        return data

    def __add_ingredients(self, recipe, ingredients_data):
        IngredientRecipe.objects.bulk_create(
            IngredientRecipe(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients_data
        )

    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        tags_data = validated_data.pop('tags')
        if Recipe.objects.filter(
            name=validated_data.get('name'),
            text=validated_data.get('text')
        ).exists():
            raise serializers.ValidationError(
                {'errors': 'Такой рецепт уже существует!'}
            )
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        self.__add_ingredients(recipe, ingredients_data)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        ingredients_data = validated_data.pop('recipe_ingredients')
        tags_data = validated_data.pop('tags')

        recipe_obj = IngredientRecipe.objects.filter(recipe=instance)
        recipe_obj.delete()
        instance.tags.set(tags_data)
        self.__add_ingredients(instance, ingredients_data)
        instance.save()
        return instance

    def to_representation(self, obj):
        request = self.context.get('request')
        serializer = RecipesReadSerializer(
            obj,
            context={'request': request}
        )
        return serializer.data

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )
