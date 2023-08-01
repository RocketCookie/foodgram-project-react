from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe

MESSAGES = {
    'shopping_cart': {
        'cr_error': ('Ошибка добавления в список покупок. '
                     'Рецепт уже есть в списке.'),
        'del_error': ('Ошибка удаления из списка покупок. '
                      'Рецепт не найден в списке.'),
    },
    'favorite': {
        'cr_error': ('Ошибка добавления в список избранного. '
                     'Рецепт уже есть в списке.'),
        'del_error': ('Ошибка удаления из списка избранного. '
                      'Рецепт не найден в списке.'),
    },
    'subscribe': {
        'cr_error': ('Ошибка добавления в список избранного. '
                     'Рецепт уже есть в списке.'),
        'del_error': ('Ошибка удаления из списка избранного. '
                      'Рецепт не найден в списке.'),
    }
}


def check_model(self, obj, model, related_field):
    '''
    Проверяет, является ли объект связанным
    с пользователем в базе данных.
    '''
    request = self.context.get('request')
    user = self.context['request'].user

    if request and request.user.is_authenticated:
        return model.objects.filter(user=user, **{related_field: obj}).exists()
    return False


# def handle_action(request, pk, model, miniserializer, error_name: str):
#     '''
#     Обрабатывает добавление или удаление рецепта в определенные
#     списки (избранное или корзина покупок).
#     '''
#     recipe = get_object_or_404(Recipe, pk=pk)
#     user = request.user

#     if request.method == 'POST':
#         if model.objects.filter(recipe=recipe, user=user).exists():
#             return Response(
#                 {'errors': MESSAGES[error_name]['cr_error']},
#                 status=status.HTTP_400_BAD_REQUEST)
#         else:
#             model.objects.create(recipe=recipe, user=user)
#             serializer = miniserializer(recipe)
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED)

#     elif request.method == 'DELETE':
#         try:
#             item = model.objects.get(recipe=recipe, user=user)
#             item.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except model.DoesNotExist:
#             return Response(
#                 {'errors': MESSAGES[error_name]['del_error']},
#                 status=status.HTTP_400_BAD_REQUEST)
