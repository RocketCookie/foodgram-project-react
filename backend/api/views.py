from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .mixins import ListRetrieveViewSet
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, MiniRecipeSerializer,
                          RecipeSerializer, TagSerializer)
from .utilities import handle_action
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag

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
        ...
