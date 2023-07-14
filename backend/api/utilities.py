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
