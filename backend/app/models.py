from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from foodgram.settings import NAME_MAX_LENGTH


class Tag(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Имя',)
    color = models.CharField(max_length=16)
    slug = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Slug',)


class Ingredient(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Имя',)
    measurement_unit = models.CharField(max_length=16)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Имя',)
    text = models.TextField(blank=True,
                            verbose_name='Описание')
    tags = models.ManyToManyField(Tag,
                                  related_name='tags',
                                  verbose_name='Тэги')
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)],
                                       verbose_name='Время приготовления')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients',
        verbose_name='Ингридиенты'
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Рецепты'
        ordering = ('pub_date',)

    def __str__(self):
        return self.name
