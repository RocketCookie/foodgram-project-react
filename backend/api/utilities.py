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
