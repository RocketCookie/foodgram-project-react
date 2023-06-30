from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    color = models.CharField(verbose_name='Цвет в HEX',
                             max_length=7,
                             null=True)
    slug = models.SlugField(verbose_name='Уникальный слаг',
                            max_length=200,
                            unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):

    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Список ингредиентов')
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Список id тегов')
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name='Картинка, закодированная в Base64',
        upload_to='recipes/images/')
    name = models.CharField(verbose_name='Название', max_length=200)
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   verbose_name='Ингридиент',
                                   on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингридиент рецепте'
        verbose_name_plural = 'Ингридиенты в рецепте'

    def __str__(self):
        return (f'{self.ingredient.name} {self.amount}'
                f'{self.ingredient.measurement_unit}')


class RecipeInFavorite(models.Model):

    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'is_favorited'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        return (f'{self.recipe.name} в избранном у '
                f'{self.user.get_username}')


class RecipeIsInShoppingCart(models.Model):

    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'is_in_shopping_cart'
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (f'{self.recipe.name} в избранном у '
                f'{self.user.get_username}')
