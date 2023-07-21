import django_filters

from recipes.models import Recipe, Tag

# from rest_framework import filters
# class IngredientFilter(filters.SearchFilter):


# class IngredientFilter(django_filters.FilterSet):
#     name = django_filters.CharFilter(field_name='name',
#                                      lookup_expr='istartswith')

#     class Meta:
#         model = Ingredient
#         fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags_slug',
        queryset=Tag.objects.all(),
        to_field_name='slug')
    in_favorite = django_filters.BooleanFilter(method='filter_in_favorite')
    is_in_shopping_card = django_filters.BooleanFilter(
        method='filter_is_in_shopping_card')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    def filter_in_favorite(self, queryset, name, value):
        if value:
            return queryset.filter(in_favorite__user=self.request.user)
        return queryset

    def filter_is_in_shopping_card(self, queryset, name, value):
        if value:
            return queryset.filter(is_in_shopping_card__user=self.request.user)
        return queryset
