from django.core.validators import (MinValueValidator,
                                    MaxValueValidator,
                                    RegexValidator)
from django.db import models
from django.urls import reverse
from users.models import User

MIN_AMOUNT = 1
MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 32000
MAX_AMOUNT = 32000


class Tag(models.Model):
    """Класс тэгов."""

    name = models.CharField(verbose_name='Название', max_length=32)
    slug = models.SlugField(
        verbose_name='Идентификатор', unique=True, max_length=32,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Введите корректный идентификатор'),
        ]
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'тэги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Класс ингредиентов."""

    name = models.CharField(verbose_name='Название', max_length=128)
    measurement_unit = models.CharField(
        verbose_name='Ед. измерения', max_length=64
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'ингредиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Класс рецептов."""

    name = models.CharField(verbose_name='Название', max_length=256)
    author = models.ForeignKey(
        User, verbose_name='Автор', on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='recipes/', null=True, default=None
    )
    text = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name='Ингредиенты', through='RecipeIngredient'
    )
    tags = models.ManyToManyField(Tag, blank=False, verbose_name='Тэги')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(MIN_COOKING_TIME),
            MaxValueValidator(MAX_COOKING_TIME)
        ]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'рецепты'
        default_related_name = 'recipes'
        ordering = ['-id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('api:recipe-detail', kwargs={'pk': self.pk})


class RecipeIngredient(models.Model):
    """Вспомогательная модель для рецептов и ингредиентов."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(MIN_AMOUNT),
            MaxValueValidator(MAX_AMOUNT)
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'ингредиенты'
        default_related_name = 'recipe_ingredients'
        ordering = ['recipe', 'ingredient']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe}'


class ShoppingCart(models.Model):
    """Модель корзины."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт', on_delete=models.CASCADE, null=True
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'корзины покупок'
        default_related_name = 'shopping_cart'
        ordering = ['user', 'recipe']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_in_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.recipe}'


class Favorite(models.Model):
    """Модель избранного."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'избранные рецепты'
        default_related_name = 'favorite'
        ordering = ['user', 'recipe']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_in_favorite'
            )
        ]

    def __str__(self):
        return f'{self.recipe}'


class ShortLink(models.Model):
    """Модель короткой ссылки."""

    lurl = models.URLField(max_length=255)
    surl = models.CharField(max_length=132, unique=True)

    class Meta:
        verbose_name = 'Короткая ссылка'
        verbose_name_plural = 'короткие ссылки'
        ordering = ['-id']
