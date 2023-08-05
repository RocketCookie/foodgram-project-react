from django.urls import include, path, re_path
from djoser.views import TokenDestroyView
from rest_framework.routers import DefaultRouter

from api.views import (
    CustomTokenCreateView,
    CustomUserViewSet,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
)

v1_router = DefaultRouter()
v1_router.register(r'users', CustomUserViewSet, basename='users')
v1_router.register(r'tags', TagViewSet, basename='tags')
v1_router.register(r'ingredients', IngredientViewSet, basename='ingredients')
v1_router.register(r'recipes', RecipeViewSet, basename='recipes')

auth_urls = [
    re_path(r"^token/login/?$", CustomTokenCreateView.as_view(), name="login"),
    re_path(r"^token/logout/?$", TokenDestroyView.as_view(), name="logout"),
]

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include(auth_urls)),
]
