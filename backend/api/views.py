from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from api.mixins import ListRetrieveViewSet
from api.permissions import AuthorOrReadOnly
from api.serializers import (IngredientSerializer, MiniRecipeSerializer,
                             RecipeSerializer, TagSerializer)
from api.utilities import handle_action
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)

User = get_user_model()


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        return handle_action(request, pk, Favorite,
                             MiniRecipeSerializer, 'favorite')

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        return handle_action(request, pk, ShoppingCart,
                             MiniRecipeSerializer, 'shopping_cart')

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request, pk=None):
        """
        Скачивает содержимое корзины покупок пользователя
        и сохраняет его в TXT файл.
        """
        ingredients = (
            IngredientInRecipe.objects
            .filter(recipe__is_in_shopping_cart__user=request.user)
            .values('ingredient')
            .annotate(sum_amount=Sum('amount'))
            .values_list('ingredient__name',
                         'sum_amount',
                         'ingredient__measurement_unit'))

        content = 'Список покупок:\n'
        for i, ingredient in enumerate(ingredients, start=1):
            content += (f'{i}. {ingredient[0]} - '
                        f'{ingredient[1]} '
                        f'{ingredient[2]}\n')

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.txt"')
        return response
