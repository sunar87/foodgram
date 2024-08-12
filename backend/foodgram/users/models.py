from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс пользователей."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254, unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150, null=True, unique=True
    )
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    avatar = models.ImageField(
        upload_to='users/', null=True, default=None
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    def __str__(self):
        return self.get_full_name()


class Subscriber(models.Model):
    """Класс подписок на авторов."""

    user = models.ForeignKey(
        User, verbose_name='Пользователь', related_name='follower',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, verbose_name='Автор', related_name='following',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'
