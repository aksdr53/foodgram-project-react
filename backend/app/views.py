import io

from rest_framework import viewsets, mixins, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import (Recipe,
                     Tag,
                     Shopping_cart,
                     Favorites, Ingredient,
                     Ingredients_amount)
from .serializers import (RecipeListSerializer,
                          RecipeCreateSerializer,
                          TagSerializer,
                          Shopping_cartSerializer,
                          IngredientSerializer)
from .filters import RecipeFilter
from users.utils import PermissionPolicyMixin
from .permissions import IsAdminOrAuthor


class RecipeViewSet(PermissionPolicyMixin, viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    pagination_class = PageNumberPagination
    permission_classes_per_method = {
        "list": [AllowAny, ],
        "retrieve": [IsAuthenticated, ],
        "create": [IsAuthenticated, ],
        "partial_update": [IsAdminOrAuthor, ],
        "destroy": [IsAdminOrAuthor, ]

    }

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return RecipeListSerializer
        if self.action == "create" or self.action == "partial_update":
            return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated, ])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if user.is_authenticated:
            if request.method == 'POST':
                if recipe and not Shopping_cart.objects.filter(
                    user=user,
                    recipe=recipe
                ).exists():
                    Shopping_cart.objects.create(user=user, recipe=recipe)
                    serializer = Shopping_cartSerializer(recipe)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if request.method == 'DELETE':
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
            if request.method == 'POST':
                if recipe and not Favorites.objects.filter(
                    user=user,
                    recipe=recipe
                ).exists():
                    Favorites.objects.create(user=user, recipe=recipe)
                    serializer = Shopping_cartSerializer(recipe)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if request.method == 'DELETE':
                if Favorites.objects.filter(user=user,
                                            recipe=recipe).exists():
                    Favorites.objects.filter(user=user,
                                             recipe=recipe).delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated, ])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = Ingredients_amount.objects.filter(
            recipe__recipe_in_users_shopping_cart__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            amount=Sum('amount')
        )
        buffer = io.BytesIO()
        pdf_object = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
        pdf_object.setFont('Verdana', 14)
        pdf_object.drawCentredString(100, 800, "Список покупок")
        text_height = 700
        for ingredient in shopping_cart:
            pdf_object.drawString(
                100, text_height,
                f'{ingredient["ingredient__name"]} -'
                f'{ingredient["amount"]},'
                f'{ingredient["ingredient__measurement_unit"]}'
            )
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
    pagination_class = None
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    http_method_names = ["get", ]
