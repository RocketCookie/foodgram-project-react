from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.filters import RecipeFilter
from api.mixins import ListRetrieveViewSet
from api.pagination import CustomPageNumberPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (IngredientSerializer, RecipeMinifiedSerializer,
                             RecipeSerializer, TagSerializer,
                             UserWithRecipesSerializer)
from api.utilities import handle_action
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)

# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404


User = get_user_model()


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
    filter_backends = (SearchFilter,)
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
        return handle_action(request, pk, Favorite,
                             RecipeMinifiedSerializer, 'favorite')

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        '''
        Добавляет или удаляет рецепт из корзины покупок пользователя.
        '''
        return handle_action(request, pk, ShoppingCart,
                             RecipeMinifiedSerializer, 'shopping_cart')

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request, pk=None):
        '''
        Скачивает содержимое корзины покупок пользователя
        и сохраняет его в TXT файл.
        '''
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


# class SubscriptionsViewSet(ListRetrieveViewSet):
#     '''
#     Представление для работы с подписками.
#     Позволяет создавать, просматривать, обновлять и удалять подписки.
#     '''
#     queryset = Subscription.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = SubscriptionSerializer

#     def get_queryset(self):
#         user = get_object_or_404(User, id=self.request.user.id)
#         return user.subscribing

#     def perform_create(self, serializer):
#         user = get_object_or_404(User, id=self.request.user.id)
#         serializer.save(user=user)

# class SubscriptionViewSet(UserViewSet):
#     # Действие для /users/subscriptions/
#     @action(detail=False, methods=['get'])
#     def subscriptions(self, request):
#         # Ваша логика обработки запроса
#         user = request.user
#         queryset = user.subscriber.all()
#         pages = self.paginate_queryset(queryset)
#         serializer = SubscriptionSerializer(
#             pages, many=True, context={'request': request})
#         return self.get_paginated_response(serializer.data)

    # @action(detail=True, methods=['post'])
    # def subscribe(self, request, pk=None):
    #     # Ваша логика обработки запроса
    #     user = self.get_object()
    #     # ...
    #     return Response({'message': 'Subscribed successfully'})

class CustomUserViewSet(UserViewSet):
    '''
    Кастомный пользователь.
    '''

    @action(methods=['get'],
            detail=False,
            pagination_class=CustomPageNumberPagination,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        '''
        Получить пагинированный список пользователей,
        на которых подписан текущий пользователь.
        '''
        user = request.user
        # recipes_limit = request.GET.get('recipes_limit', None)
        # print(recipes_limit, type(recipes_limit))

        queryset = User.objects.filter(subscribing__user=user)
        paginator = self.pagination_class()

        result_page = paginator.paginate_queryset(queryset, request)
        # print(result_page)

        # if recipes_limit:
        #     for user in result_page:
        #         recipes = user.recipes.all()[:int(recipes_limit)]
        #         print(recipes)
        #         print(user.recipes)
        #         user.recipes.set(recipes)
        #         print(user.recipes)

        serializer = UserWithRecipesSerializer(
            result_page,
            many=True,
            context={'request': request})
        return paginator.get_paginated_response(serializer.data)
