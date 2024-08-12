from django.urls import include, path
from rest_framework import routers

from .views import (
    IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet, short_link
)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet)
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/get-link/', short_link, name='get-link'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
