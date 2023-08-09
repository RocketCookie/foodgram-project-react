from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    '''
    Фильтр для модели Recipe.
    '''

    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    def filter_is_favorited(self, queryset, name, value):
        '''
        Фильтрует рецепты по наличию в избранном пользователя.
        '''
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(is_favorited__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        '''
        Фильтрует рецепты по наличию в корзине покупок пользователя.
        '''
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(is_in_shopping_cart__user=user)
        return queryset


class CustomSearchFilter(SearchFilter):
    '''
    Кастомный фильтр поиска с переопределенным параметром поиска на name.
    '''

    search_param = 'name'
