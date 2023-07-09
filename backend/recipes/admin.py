from django.contrib import admin

from .models import (Ingredient, Recipe, RecipeInFavorite,
                     RecipeIsInShoppingCart, Tag)

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeInFavorite)
admin.site.register(RecipeIsInShoppingCart)
admin.site.register(Tag)
