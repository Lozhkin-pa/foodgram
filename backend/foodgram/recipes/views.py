from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, HttpResponse
from django.db.models import Sum
from .filters import RecipeFilter, IngredientFilter
from .models import Tag, Ingredient, Recipe, Favorite, ShoppingCart
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipesReadSerializer,
    RecipeCreateUpdateSerializer,
    RecipeSerializer
)


class ListRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Добавлены специальные маршрутизируемые методы для работы с избранным,
    списком покупок и выгрузкой файла.
    """
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesReadSerializer
        return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        """
        Добавляет/удаляет рецепт в избранное.
        """
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            Favorite.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = RecipeSerializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            favorite_obj = get_object_or_404(
                Favorite,
                user=request.user,
                recipe=recipe
            )
            favorite_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """
        Добавляет/удаляет рецепт в список покупок.
        """
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            ShoppingCart.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = RecipeSerializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            favorite_obj = get_object_or_404(
                ShoppingCart,
                user=request.user,
                recipe=recipe
            )
            favorite_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """
        Скачивает файл со списком покупок в формате txt.
        """
        if not ShoppingCart.objects.filter(
            user=request.user
        ).exists:
            return Response(
                {'errors': 'Список покупок пуст!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        ingredients = ShoppingCart.objects.filter(
            user=request.user
        ).values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
        ).annotate(
            amount=Sum('recipe__recipe_ingredients__amount')
        )
        txt_file = []
        txt_file.append('***СПИСОК ПРОДУКТОВ***')
        number = 1
        for obj in ingredients:
            txt_file.append((
                f'#{number} {obj.get("recipe__ingredients__name")} '
                f'({obj.get("recipe__ingredients__measurement_unit")}) - '
                f'{obj.get("amount")}'
            ))
            number += 1
        response = HttpResponse(
            content='\n'.join(txt_file),
            content_type='text/plain; charset=UTF-8',
        )
        response['Content-Disposition'] = (
            'attachment; filename=Shopping_list.txt'
        )
        return response
