from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True,
        blank=False)
    color = models.CharField(
        verbose_name='Цвет в HEX',
        max_length=7,
        unique=True,
        blank=False)
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        max_length=200,
        unique=True,
        blank=False)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(
        max_length=200,
        blank=False)
    measurement_unit = models.CharField(
        max_length=200,
        blank=False)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):

    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        related_name='recipe_ingredients')
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список id тегов',
        related_name='recipe_tags')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipe_author',
        on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name='Картинка, закодированная в Base64',
        upload_to='recipes/images/',
        blank=False)
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        blank=False)
    text = models.TextField(
        verbose_name='Описание',
        blank=False)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        blank=False)
    create_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    class Meta:
        ordering = ('-create_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингридиент',
        related_name='ingredient_in_recipe',
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='recipe_with_ingredients',
        on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        blank=False)

    class Meta:
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецепте'

    def __str__(self):
        return (f'{self.ingredient.name} {self.amount} '
                f'{self.ingredient.measurement_unit}')


class RecipeInFavorite(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
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

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.PROTECT)
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'is_in_shopping_cart'
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (f'{self.recipe.name} в избранном у '
                f'{self.user.get_username}')
