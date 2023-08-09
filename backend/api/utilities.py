MESSAGES = {
    'shopping_cart': {
        'cr_error': (
            'Ошибка добавления в список покупок. ' 'Рецепт уже есть в списке.'
        ),
        'del_error': (
            'Ошибка удаления из списка покупок. ' 'Рецепт не найден в списке.'
        ),
    },
    'favorite': {
        'cr_error': (
            'Ошибка добавления в список избранного. '
            'Рецепт уже есть в списке.'
        ),
        'del_error': (
            'Ошибка удаления из списка избранного. '
            'Рецепт не найден в списке.'
        ),
    },
    'subscribe': {
        'cr_error': (
            'Ошибка добавления в список избранного. '
            'Рецепт уже есть в списке.'
        ),
        'del_error': (
            'Ошибка удаления из списка избранного. '
            'Рецепт не найден в списке.'
        ),
    },
}


def is_item_linked_to_user(self, obj, model, related_field):
    '''
    Проверяет, является ли объект связанным
    с пользователем в базе данных.
    '''
    request = self.context.get('request')
    user = request.user

    if request and user.is_authenticated:
        return model.objects.filter(user=user, **{related_field: obj}).exists()
    return False
