from django.contrib.auth.decorators import login_required
from django_filters import BooleanFilter, FilterSet, ModelMultipleChoiceFilter
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    '''Фильтр для модели Recipe.'''
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug')
    favorite = BooleanFilter(method='filter_in_favorite')
    shopping_card = BooleanFilter(
        method='filter_is_in_shopping_card')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    @login_required
    def filter_in_favorite(self, queryset, name, value):
        ''' Фильтрует рецепты по наличию в избранном пользователя.'''
        user = self.request.user
        if value:
            return queryset.filter(in_favorite__user=user)
        return queryset.exclude(is_favorited__user=user)

    @login_required
    def filter_is_in_shopping_card(self, queryset, name, value):
        '''Фильтрует рецепты по наличию в корзине покупок пользователя.'''
        user = self.request.user
        if value:
            return queryset.filter(is_in_shopping_card__user=user)
        return queryset.exclude(is_in_shopping_cart__user=user)


class CustomSearchFilter(SearchFilter):
    '''
    Кастомный фильтр поиска с переопределенным параметром поиска на name.
    '''
    search_param = 'name'
