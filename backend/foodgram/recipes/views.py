from rest_framework import mixins, viewsets
from .models import Tag, Ingredient, Recipe, TagRecipe, IngredientRecipe, Favorite, Shopping_cart
from .serializers import TagSerializer, IngredientSerializer


class ListRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer