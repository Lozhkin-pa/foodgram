from rest_framework import mixins, viewsets, status
from .models import Tag, Ingredient, Recipe, Favorite, Shopping_cart
from .serializers import TagSerializer, IngredientSerializer, RecipesReadSerializer, RecipeCreateUpdateSerializer, RecipeSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RecipeFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404, HttpResponse
from django.db.models import Sum


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
    filter_backends = (SearchFilter,)
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
            if Favorite.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в избранное!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
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
            if not Favorite.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт не добавлен в избранное!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
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
            if Shopping_cart.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в список покупок!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Shopping_cart.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = RecipeSerializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            if not Shopping_cart.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                return Response(
                    {'errors': 'Рецепт не добавлен в список покупок!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            favorite_obj = get_object_or_404(
                Shopping_cart,
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
        if not Shopping_cart.objects.filter(
            user=request.user
        ).exists:
            return Response(
                    {'errors': 'Список покупок пуст!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        ingredients = Shopping_cart.objects.filter(
            user=request.user
        ).values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
        ).annotate(
            amount = Sum('recipe__recipe_ingredients__amount')
        )

        txt_file = []
        txt_file.append(f'"Список продуктов"')
        number = 1
        for ingredient in ingredients:
            txt_file.append(
                (
                    f'#{number} {ingredient.get("recipe__ingredients__name")} '
                    f'({ingredient.get("recipe__ingredients__measurement_unit")}) - '
                    f'{ingredient.get("amount")}'
                )
            )
            number += 1
        response = HttpResponse(
            content='\n'.join(txt_file),
            content_type='text/plain; charset=UTF-8',
        )
        response['Content-Disposition'] = (
            f'attachment; filename=Shopping_list.txt'
        )
        return response
