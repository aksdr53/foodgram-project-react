from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .views import RecipeViewSet


router = SimpleRouter()
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]