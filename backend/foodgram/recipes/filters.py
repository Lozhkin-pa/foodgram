from django.contrib.auth import get_user_model
from recipes.models import Tag, Recipe
from rest_framework import filters
from django_filters.rest_framework import (
    FilterSet,
    ModelMultipleChoiceFilter,
    BooleanFilter,
    ModelChoiceFilter
)

User = get_user_model()


class RecipeFilter(FilterSet):
    """
    Фильтрация рецептов по тегам (слагу тега), автору, избранному и списку
    покупок.
    """
    author = ModelChoiceFilter(
        queryset=User.objects.all()
    )
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = BooleanFilter(
        method='get_is_favorited',
    )
    is_in_shopping_cart = BooleanFilter(
        method='get_is_in_shopping_cart',
    )

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart'
        )


class IngredientFilter(filters.SearchFilter):
    search_param = 'name'
