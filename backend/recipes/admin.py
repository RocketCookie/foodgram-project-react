from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)

admin.site.register(Ingredient)
admin.site.register(IngredientInRecipe)
admin.site.register(Recipe)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(Tag)
