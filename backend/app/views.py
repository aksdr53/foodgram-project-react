from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import Recipe, Tag, Shopping_cart
from .serializers import RecipeSerializer, TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(methods=['post', 'delete'], detail=True, url_path=r'(?P<recipe_id>\d+)/shopping_cart')
    def shopping_cart(self, request):
        id=self.kwargs.get('recipe_id')
        recipe = Recipe.objects.get(id=id)
        user=self.user
        if user.is_authenticated:

            if self.action == 'post':
                if recipe and not Shopping_cart.objects.filter(user=user, recipe=recipe).exists():
                    add_to_shopping_cart = Shopping_cart.objects.create(user=user, recipe=recipe)
                    return Response(status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if self.action == 'delete':
                if Shopping_cart.objects.filter(user=user, recipe=recipe).exists():
                    Shopping_cart.objects.filter(user=user, recipe=recipe).delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ListRetrieveViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer