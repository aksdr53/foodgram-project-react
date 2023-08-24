from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from foodgram.settings import NAME_MAX_LENGTH


class Tag(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Имя', unique=True, blank=False)
    color = models.CharField(max_length=16, unique=True, blank=False)
    slug = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Slug', unique=True, blank=False)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Имя', blank=False)
    measurement_unit = models.CharField(max_length=16, blank=False)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    name = models.CharField(blank=False, max_length=NAME_MAX_LENGTH,
                            verbose_name='Имя',)
    text = models.TextField(blank=False,
                            verbose_name='Описание')
    tags = models.ManyToManyField(Tag,
                                  related_name='tags_in_recipe',
                                  verbose_name='Тэги')
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)],
                                       verbose_name='Время приготовления',
                                       blank=False)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='Ingredients_amount',
                                         through_fields=('recipe',
                                                         'ingredient'),
                                         related_name='recipe',
                                         verbose_name='Ингридиенты')

    class Meta:
        verbose_name = 'Recipe'
        ordering = ('pub_date',)

    def __str__(self):
        return self.name


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='users_favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_in_users_favorites')


class Shopping_cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='users_shopping_cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_in_users_shopping_cart')


class Ingredients_amount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients_amount_in_recipe')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredients_amount')
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.recipe
