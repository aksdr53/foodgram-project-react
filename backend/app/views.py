from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Recipe, Tag, Shopping_cart, Favorites, Ingredient
from .serializers import (RecipeSerializer,
                          TagSerializer,
                          Shopping_cartSerializer,
                          IngredientSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        recipe = Recipe.objects.get(id=pk)
        user = request.user
        if user.is_authenticated:
            if self.action == 'post':
                if recipe and not Shopping_cart.objects.filter(
                    user=user,
                    recipe=recipe
                ).exists():
                    Shopping_cart.objects.create(user=user, recipe=recipe)
                    serializer = Shopping_cartSerializer(recipe)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if self.action == 'delete':
                if Shopping_cart.objects.filter(user=user,
                                                recipe=recipe).exists():
                    Shopping_cart.objects.filter(user=user,
                                                 recipe=recipe).delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        recipe = Recipe.objects.get(id=pk)
        user = request.user
        if user.is_authenticated:
            if self.action == 'post':
                if recipe and not Favorites.objects.filter(
                    user=user,
                    recipe=recipe
                ).exists():
                    Favorites.objects.create(user=user, recipe=recipe)
                    serializer = Shopping_cartSerializer(recipe)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if self.action == 'delete':
                if Favorites.objects.filter(user=user,
                                            recipe=recipe).exists():
                    Favorites.objects.filter(user=user,
                                             recipe=recipe).delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
