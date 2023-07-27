from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    '''
    Пользовательский класс пагинации,
    который расширяет класс PageNumberPagination
    из Django REST Framework.
    '''
    page_size_query_param = 'limit'
