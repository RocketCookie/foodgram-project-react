from rest_framework.permissions import AllowAny

from .mixins import ListRetrieveViewSet
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from recipes.models import Ingredient, Recipe, Tag


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer


class RecipeViewSet(ListRetrieveViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None
    serializer_class = RecipeSerializer
