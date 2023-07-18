from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .utilities import check_model
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        return check_model(self, obj, Subscription, 'subscribing')


class TagSerializer(serializers.ModelSerializer):
    '''Тег'''
    class Meta:
        model = Tag
        fields = '__all__'
        # read_only_fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    '''Ингридиент'''
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    # id = serializers.IntegerField()
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    '''Получение рецепта'''
    # tags = TagSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        many=True, required=True, source='recipe')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    def to_representation(self, instance):
        '''
        Переопределение вывода и конвертация id
        тегов в сериализованные данные
        '''
        rep = super().to_representation(instance)
        tags_id = instance.tags.values_list('id', flat=True)
        tags = Tag.objects.filter(id__in=tags_id)
        # tags = Tag.objects.filter(
        #     id__in=[tag.id for tag in instance.tags.all()])
        rep['tags'] = TagSerializer(tags, many=True).data
        return rep

    # def to_internal_value(self, data):
    #     '''
    #     Переопределение ввода: конвертация
    #     id тегов в объекты модели Tag
    #     '''
    #     internal_value = super().to_internal_value(data)
    #     internal_value['tags'] = Tag.objects.filter(id__in=data['tags'])
    #     return internal_value

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        return check_model(self, obj, Favorite, 'recipe')

    def get_is_in_shopping_cart(self, obj):
        return check_model(self, obj, ShoppingCart, 'recipe')

    # def validate_tags(self, tags):
    #     """
    #     Пользовательский валидатор для поля 'tags'.
    #     Проверяет, что предоставленные идентификаторы тегов существуют.
    #     """
    #     print(tags)
    #     for tag_id in tags:
    #         try:
    #             Tag.objects.get(name=tag_id)
    #         except Tag.DoesNotExist:
    #             raise serializers.ValidationError(
    #                 'Недопустимый идентификатор тега: {}'.format(tag_id))

    #     return tags

    # def validate_ingredients(self, ingredients):
    #     """
    #     Пользовательский валидатор для поля 'tags'.
    #     Проверяет, что предоставленные идентификаторы тегов существуют.
    #     """
    #     print(ingredients)
    #     print(self.initial_data)
    #     for ingredient in ingredients:
    #         try:
    #             Ingredient.objects.get(id=ingredient['id'])
    #         except Ingredient.DoesNotExist:
    #             raise serializers.ValidationError(
    #                 'Недопустимый идентификатор тега: '
    #                  '{}'.format(ingredient['id']))

    #     return ingredients

    def create(self, validated_data):
        print(validated_data)

        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('recipe')
        # Создание рецепта
        recipe = Recipe.objects.create(**validated_data)

        # Добавление ингредиентов к рецепту
        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.get(
                id=ingredient_data['ingredient']['id'])
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredient_data['amount']
            )
        # Добавление тегов к рецепту
        for tag_id in tags_data:
            print(tag_id)
            tag = Tag.objects.get(name=tag_id)
            recipe.tags.add(tag)
        # tags = Tag.objects.filter(id__in=tags_data)
        # recipe.tags.set(tags)

        return recipe

    def update(self, instance, validated_data):
        # Обновление полей рецепта, если они присутствуют в validated_data
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)

        # Обновление ингредиентов рецепта
        ingredients_data = validated_data.get('recipe')
        print(validated_data)
        instance.ingredients.clear()  # Очистить существующие ингредиенты
        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.get(
                id=ingredient_data['ingredient']['id'])
            IngredientInRecipe.objects.create(
                recipe=instance,
                ingredient=ingredient,
                amount=ingredient_data['amount']
            )

        # Обновление тегов рецепта
        tags_data = validated_data.get('tags')
        instance.tags.clear()  # Очистить существующие теги рецепта
        for tag_id in tags_data:
            tag = Tag.objects.get(name=tag_id)
            instance.tags.add(tag)

        instance.save()
        return instance


class MiniRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
