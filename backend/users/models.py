from django.contrib.auth.models import AbstractUser
from django.db import models
from app.constants import (USERS_EMAIL_MAX_LENGTH,
                           USERS_NAMES_PASSWORDS_MAX_LENGTH)


class User(AbstractUser):
    email = models.EmailField(max_length=USERS_EMAIL_MAX_LENGTH,
                              blank=False, unique=True, verbose_name='email')
    username = models.CharField(blank=False,
                                max_length=USERS_NAMES_PASSWORDS_MAX_LENGTH,
                                unique=True,
                                verbose_name='username')
    last_name = models.CharField(max_length=USERS_NAMES_PASSWORDS_MAX_LENGTH,
                                 blank=False, verbose_name='last name')
    first_name = models.CharField(max_length=USERS_NAMES_PASSWORDS_MAX_LENGTH,
                                  blank=False, verbose_name='first name')
    password = models.CharField(verbose_name='password',
                                max_length=USERS_NAMES_PASSWORDS_MAX_LENGTH)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('date_joined', )

    @property
    def is_admin(self):
        return (self.is_superuser
                or self.is_staff)

    @property
    def is_user(self):
        return not (self.is_superuser
                    or self.is_staff)

    def __str__(self) -> str:
        return self.username


class Subscriptions(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author', verbose_name='Автор')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='subscriber',
                                   verbose_name='Подписчик')
    
    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'{self.subscriber} subscribed for {self.author}'
