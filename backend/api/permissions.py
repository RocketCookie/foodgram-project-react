from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorOrReadOnly(BasePermission):
    '''
    Правило доступа, позволяющее только автору объекта изменять его,
    в то время как остальным разрешены только безопасные методы
    (GET, HEAD, OPTIONS).
    '''

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

# взял из исходников IsAuthenticatedOrReadOnly
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )
