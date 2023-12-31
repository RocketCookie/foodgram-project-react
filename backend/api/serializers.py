from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.utilities import is_item_linked_to_user
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели User.'''

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        return is_item_linked_to_user(self, obj, Subscription, 'subscribing')


class TagSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Tag.'''

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Ingredient.'''

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели IngredientInRecipe.'''

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор рецепта.'''

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        many=True, required=True, source='recipe_ingredients'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def to_representation(self, instance):
        '''
        Переопределение вывода и конвертация id
        тегов в сериализованные данные
        '''
        rep = super().to_representation(instance)
        tag_ids = instance.tags.all().values_list('id', flat=True)
        tags = Tag.objects.filter(id__in=tag_ids)
        serializer = TagSerializer(tags, many=True)
        rep['tags'] = serializer.data
        return rep

    def get_is_favorited(self, obj):
        '''
        Получение информации о том, добавлен ли рецепт
        в избранное у текущего пользователя.
        '''
        return is_item_linked_to_user(self, obj, Favorite, 'recipe')

    def get_is_in_shopping_cart(self, obj):
        '''
        Получение информации о том, добавлен ли рецепт
        в корзину покупок текущего пользователя.
        '''
        return is_item_linked_to_user(self, obj, ShoppingCart, 'recipe')

    def validate_tags(self, tags):
        '''
        Пользовательский валидатор для поля 'tags'.
        Проверяет, что предоставленные идентификаторы тегов существуют.
        '''
        if not tags:
            raise serializers.ValidationError(
                'Количество тегов должно быть 1 и более.'
            )
        for tag in tags:
            try:
                Tag.objects.get(id=tag.id)
            except Tag.DoesNotExist:
                raise serializers.ValidationError(
                    'Недопустимый идентификатор тега: {}'.format(tag.id)
                )
        return tags

    def validate_ingredients(self, ingredients):
        '''
        Пользовательский валидатор для поля 'ingredients'.
        '''
        # unique_id = set([ingredient.get('ingredient').get('id')
        #                 for ingredient in ingredients])
        # print(f'уникальный список {unique_id}')

        if not ingredients:
            raise serializers.ValidationError(
                'Количество ингредиентов должно быть 1 и более.'
            )
        for ingredient in ingredients:
            try:
                ingredient_id = ingredient.get('ingredient').get('id')
                Ingredient.objects.get(id=ingredient_id)
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    'Недопустимый идентификатор ингредиента: '
                    '{}'.format(ingredient_id)
                )
            amount = ingredient.get('amount')
            if amount <= 0:
                raise serializers.ValidationError(
                    'Недопустимое значение количества: ' '{}'.format(amount)
                )
        return ingredients

    def create(self, validated_data):
        '''
        Создание нового рецепта.
        '''
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('recipe_ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.get(
                id=ingredient_data['ingredient']['id']
            )
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredient_data['amount'],
            )
        for tag_data in tags_data:
            tag_id = tag_data.id
            tag = Tag.objects.get(id=tag_id)
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validated_data):
        '''
        Обновление существующего рецепта.
        '''
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )

        ingredients_data = validated_data.get('recipe_ingredients')
        instance.ingredients.clear()
        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.get(
                id=ingredient_data['ingredient']['id']
            )
            IngredientInRecipe.objects.create(
                recipe=instance,
                ingredient=ingredient,
                amount=ingredient_data['amount'],
            )
        tags_data = validated_data.get('tags')
        instance.tags.clear()
        for tag_id in tags_data:
            tag = Tag.objects.get(name=tag_id)
            instance.tags.add(tag)
        instance.save()
        return instance


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для мини-объектов рецептов.
    '''

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class UserWithRecipesSerializer(UserSerializer):
    '''
    Сериализатор для представления пользователя с его рецептами
    и их количеством.
    '''

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('recipes_count', 'recipes')

    def get_recipes_count(self, obj):
        '''
        Возвращает количество рецептов пользователя.
        '''
        return obj.recipes.count()

    def get_recipes(self, obj):
        '''
        Возвращает рецепты пользователя.
        '''
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit', None)

        recipes = obj.recipes.all()

        if recipes_limit:
            try:
                recipes_limit = int(recipes_limit)
            except ValueError:
                raise ValueError(
                    'Значение recipes_limit должно быть целым числом.'
                )
            recipes = recipes[: int(recipes_limit)]
        serializer = RecipeMinifiedSerializer(recipes, many=True)
        return serializer.data
