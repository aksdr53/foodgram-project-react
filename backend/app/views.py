import io

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.db.models import Sum

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

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        recipes = user.users_shopping_cart.recipe
        shopping_cart = recipes.ingredient_amount_in_recipe.values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            amount=Sum('amount')
        )
        buffer = io.BytesIO
        pdf_object = canvas.Canvas(buffer)
        pdf_object.setFont('Times-Roman', 14)
        pdf_object.drawCentredString(100, 100, "Список покупок")
        text_height = 700
        for ingredient in shopping_cart:
            pdf_object.drawString(100, text_height,
                                  f'{ingredient.name} -'
                                  f' {ingredient.amount},'
                                  f'{ingredient.measurement_unit}')
            text_height -= 20
            if text_height <= 40:
                text_height = 800
                pdf_object.showPage()
                pdf_object.setFont('Times-Roman', 14)
        pdf_object.showPage()
        pdf_object.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='shopping_cart.pdf')


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
