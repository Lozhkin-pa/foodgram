from django.contrib import admin
from .models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientRecipe,
    TagRecipe,
    Favorite,
    Shopping_cart
)


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


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


class TagsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__name',)
    list_filter = ('recipe__name', 'ingredient__name',)


class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'tag',)
    search_fields = ('recipe__name', 'tag__name')
    list_filter = ('recipe__name', 'tag__name')


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)
    search_fields = ('recipe__name', 'user__username')
    list_filter = ('recipe__name', 'user__username')


class Shopping_cartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)
    search_fields = ('recipe__name', 'user__username')
    list_filter = ('recipe__name', 'user__username')


admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Tag, TagsAdmin)
admin.site.register(Ingredient, IngredientsAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(TagRecipe, TagRecipeAdmin)
admin.site.register(Favorite, FavoritesAdmin)
admin.site.register(Shopping_cart, Shopping_cartAdmin)
