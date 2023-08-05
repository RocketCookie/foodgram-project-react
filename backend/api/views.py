from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.conf import settings as djoser_settings
from djoser.utils import login_user
from djoser.views import TokenCreateView, UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilter, CustomSearchFilter
from api.mixins import ListRetrieveViewSet
from api.pagination import CustomPageNumberPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (
    IngredientSerializer,
    RecipeMinifiedSerializer,
    RecipeSerializer,
    TagSerializer,
    UserWithRecipesSerializer,
)
from api.utilities import MESSAGES
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.models import Subscription

User = get_user_model()


# как упростить и использовать сразу на 3 представления?
# В данный момент работает с избранным и корзиной.
# Но для подписки надо добавить еще один(или более) параметр,
# так как названия полей в модели разное.
# Subscription.objects.create(user=user, subscribing=queryset)
# Как перенести subscribing=queryset в аргументы?
def handle_action(request, pk, model, miniserializer, error_name: str):
    '''
    Обрабатывает добавление или удаление рецепта в определенные
    списки (избранное или корзина покупок).
    '''
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user

    if request.method == 'POST':
        if model.objects.filter(recipe=recipe, user=user).exists():
            return Response(
                {'errors': MESSAGES[error_name]['cr_error']},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            model.objects.create(recipe=recipe, user=user)
            serializer = miniserializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        try:
            item = model.objects.get(recipe=recipe, user=user)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except model.DoesNotExist:
            return Response(
                {'errors': MESSAGES[error_name]['del_error']},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomTokenCreateView(TokenCreateView):
    '''
    Представление для создания токена.
    '''

    def _action(self, serializer):
        token = login_user(self.request, serializer.user)
        token_serializer_class = djoser_settings.SERIALIZERS.token

        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED,
        )


class TagViewSet(ListRetrieveViewSet):
    '''
    Представление для работы с тегами.
    Отображает список и детали тегов.
    '''

    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    '''
    Представление для работы с ингредиентами.
    Отображает список и детали ингредиентов.
    Поддерживает поиск по имени ингредиента.
    '''

    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (CustomSearchFilter,)
    search_fields = '^name'


class RecipeViewSet(viewsets.ModelViewSet):
    '''
    Представление для работы с рецептами.
    Позволяет создавать, просматривать, обновлять и удалять рецепты.
    Реализует функциональность добавления и удаления рецепта из избранного
    и корзины покупок пользователя.
    Поддерживает фильтрацию рецептов.
    '''

    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        '''
        Выполняет сохранение рецепта с указанием автора.
        '''
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        '''
        Добавляет или удаляет рецепт из избранного пользователя.
        '''
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        if request.method == 'POST':
            if Favorite.objects.filter(recipe=recipe, user=user).exists():
                return Response(
                    {'errors': MESSAGES['favorite']['cr_error']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                Favorite.objects.create(recipe=recipe, user=user)
                serializer = RecipeMinifiedSerializer(recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        elif request.method == 'DELETE':
            try:
                item = Favorite.objects.get(recipe=recipe, user=user)
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Favorite.DoesNotExist:
                return Response(
                    {'errors': MESSAGES['favorite']['del_error']},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        '''
        Добавляет или удаляет рецепт из корзины покупок пользователя.
        '''
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        if request.method == 'POST':
            if ShoppingCart.objects.filter(recipe=recipe, user=user).exists():
                return Response(
                    {'errors': MESSAGES['shopping_cart']['cr_error']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                ShoppingCart.objects.create(recipe=recipe, user=user)
                serializer = RecipeMinifiedSerializer(recipe)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        elif request.method == 'DELETE':
            try:
                item = ShoppingCart.objects.get(recipe=recipe, user=user)
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ShoppingCart.DoesNotExist:
                return Response(
                    {'errors': MESSAGES['shopping_cart']['del_error']},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request, pk=None):
        '''
        Скачивает содержимое корзины покупок пользователя
        и сохраняет его в TXT файл.
        '''
        ingredients = (
            IngredientInRecipe.objects.filter(
                recipe__is_in_shopping_cart__user=request.user
            )
            .values('ingredient')
            .annotate(sum_amount=Sum('amount'))
            .values_list(
                'ingredient__name',
                'sum_amount',
                'ingredient__measurement_unit',
            )
        )

        content = 'Список покупок:\n'
        for i, ingredient in enumerate(ingredients, start=1):
            content += (
                f'{i}. {ingredient[0]} - '
                f'{ingredient[1]} '
                f'{ingredient[2]}\n'
            )
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; ' 'filename="shopping_list.txt"'
        )
        return response


class CustomUserViewSet(UserViewSet):
    '''
    Кастомный пользователь.
    '''

    queryset = User.objects.all()

    @action(
        methods=['get'],
        detail=False,
        pagination_class=CustomPageNumberPagination,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        '''
        Получить пагинированный список пользователей,
        на которых подписан текущий пользователь.
        '''
        user = request.user

        queryset = User.objects.filter(subscribing__user=user)
        paginator = self.pagination_class()

        result_page = paginator.paginate_queryset(queryset, request)
        serializer = UserWithRecipesSerializer(
            result_page, many=True, context={'request': request}
        )
        return paginator.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id=None):
        queryset = get_object_or_404(User, id=id)
        print(queryset)
        user = request.user
        print(user)

        if request.method == 'POST':
            if Subscription.objects.filter(
                user=user, subscribing=queryset
            ).exists():
                return Response(
                    {'errors': MESSAGES['subscribe']['cr_error']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                Subscription.objects.create(user=user, subscribing=queryset)
                serializer = UserWithRecipesSerializer(
                    queryset, context={'request': request}
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        elif request.method == 'DELETE':
            try:
                item = Subscription.objects.get(
                    user=user, subscribing=queryset
                )
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Subscription.DoesNotExist:
                return Response(
                    {'errors': MESSAGES['subscribe']['del_error']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
