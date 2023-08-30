from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from colorfield.fields import ColorField

from .constants import RECIPES_NAME_MAX_LENGTH
from users.models import User


class Tag(models.Model):
    name = models.CharField(verbose_name='Имя', unique=True, blank=False)
    color = ColorField(default='#FF0000', verbose_name='Цвет')
    slug = models.CharField(verbose_name='Slug', unique=True, blank=False)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Имя', blank=False)
    measurement_unit = models.CharField(max_length=16, blank=False,
                                        verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'])
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор')
    name = models.CharField(blank=False, max_length=RECIPES_NAME_MAX_LENGTH,
                            verbose_name='Имя',)
    text = models.TextField(blank=False,
                            verbose_name='Описание')
    tags = models.ManyToManyField(Tag,
                                  related_name='tags_in_recipe',
                                  verbose_name='Тэги')
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        verbose_name='Картинка'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(600)],
        verbose_name='Время приготовления',
        blank=False
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='Ingredients_amount',
                                         through_fields=('recipe',
                                                         'ingredient'),
                                         related_name='recipe',
                                         verbose_name='Ингридиенты')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('pub_date',)

    def __str__(self):
        return self.name
    

class Added(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='users_%(class)s',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_in_users_%(class)s',
                               verbose_name='Рецепт')

    class Meta:
        abstract = True
        verbose_name = '%(class)s'
    
    def __str__(self):
        return f'Рецепт {self.recipe} у {self.user}'


class Favorites(Added):
    pass


class Shopping_cart(Added):
    pass


class Ingredients_amount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients_amount_in_recipe',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredients_amount',
                                   verbose_name='Ингридиент')
    amount = models.PositiveIntegerField(verbose_name='Количество',
                                         validators=[MinValueValidator(1),
                                                     MaxValueValidator(100000)])

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'
