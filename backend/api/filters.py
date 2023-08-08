from django_filters import BooleanFilter, FilterSet, ModelMultipleChoiceFilter
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    '''Фильтр для модели Recipe.'''

    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorite = BooleanFilter(method='filter_in_favorite')
    is_in_shopping_card = BooleanFilter(method='filter_is_in_shopping_card')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorite', 'is_in_shopping_card')

    def filter_in_favorite(self, queryset, name, value):
        '''Фильтрует рецепты по наличию в избранном пользователя.'''
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(is_favorited__user=user)
        return queryset

    def filter_is_in_shopping_card(self, queryset, name, value):
        '''Фильтрует рецепты по наличию в корзине покупок пользователя.'''
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(is_in_shopping_card__recipe=user)
        return queryset


# /api/recipes/?page=1&limit=6&is_favorited=1&author=2&tags=red&tags=test


class CustomSearchFilter(SearchFilter):
    '''
    Кастомный фильтр поиска с переопределенным параметром поиска на name.
    '''

    search_param = 'name'
