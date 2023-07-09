from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from .views import


v1_router = DefaultRouter()


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
