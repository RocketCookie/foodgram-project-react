from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'get_favorite_count')
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author__username')
    inlines = (IngredientInRecipeInline,)

    def get_favorite_count(self, obj):
        '''
        Возвращает количество добавлений в избранное для рецепта.
        '''
        return obj.is_favorited.count()

    get_favorite_count.short_description = 'Добавления в избранное'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')
    list_editable = ('recipe', 'user')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')
    list_editable = ('recipe', 'user')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_editable = ('name', 'measurement_unit')
