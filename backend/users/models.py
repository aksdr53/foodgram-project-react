from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram.settings import (MAX_LENGTH,
                               EMAIL_MAX_LENGTH)


ADMIN = "admin"
USER = "user"
ROLE = [
    (ADMIN, "Администратор"),
    (USER, "Пользователь")
]


class User(AbstractUser):
    role = models.CharField(default=USER,
                            choices=ROLE,
                            max_length=len(max(map(lambda x: x[0], ROLE),
                                               key=len)))
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH,
                              blank=False, unique=True)
    username = models.CharField(blank=False,
                                max_length=MAX_LENGTH, unique=True)
    last_name = models.CharField(max_length=MAX_LENGTH, blank=False)
    first_name = models.CharField(max_length=MAX_LENGTH, blank=False)
    

    class Meta:
        verbose_name = 'Пользователь'

    @property
    def is_admin(self):
        return (self.role == ADMIN
                or self.is_superuser
                or self.is_staff)

    @property
    def is_user(self):
        return self.role == USER

    def __str__(self) -> str:
        return self.username


class Subscriptions(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='subscriber')
