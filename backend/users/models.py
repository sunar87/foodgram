from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    email = models.EmailField(
        max_length=256,
        unique=True,
        verbose_name='Электронная почта')
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин пользователя')
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя')
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пользователя')
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль пользователя')

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='subscriptions_unique')]

    def __str__(self):
        return f'Подписка {self.user} на {self.author}'
