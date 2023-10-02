from django.contrib import admin
from .models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientRecipe,
    TagRecipe,
    Favorite,
    ShoppingCart
)


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'image',
        'text',
        'cooking_time',
    )
    search_fields = ('author', 'name', 'tags__name',)
    list_filter = ('author', 'name', 'tags__name',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name',)
    list_filter = ('recipe__name', 'ingredient__name',)


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'tag',)
    search_fields = ('recipe__name', 'tag__name')
    list_filter = ('recipe__name', 'tag__name')


@admin.register(Favorite)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)
    search_fields = ('recipe__name', 'user__username')
    list_filter = ('recipe__name', 'user__username')


@admin.register(ShoppingCart)
class Shopping_cartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)
    search_fields = ('recipe__name', 'user__username')
    list_filter = ('recipe__name', 'user__username')
