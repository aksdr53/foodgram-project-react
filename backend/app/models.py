from django.db import models
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Имя',)
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=(validate_year, ),
    )
    description = models.TextField(blank=True,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(Genre,
                                   related_name='genre',
                                   verbose_name='Жанр')
    category = models.ForeignKey(
        Category, null=True,
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение'
        ordering = ('name',)

    def __str__(self):
        return self.name