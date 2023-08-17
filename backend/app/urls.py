from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import RecipeViewSet, TagViewSet


router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
# router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
#                   RecipeViewSet, basename='shopping_cart')
router.register('tags', TagViewSet, basename='tags')


urlpatterns = [
    path('', include(router.urls)),
]
