from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Имя'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Имя'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Слаг'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения ингредиента')

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
        through='RecipeTag',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes',
        through='RecipeIngredient'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MaxValueValidator(120),
            MinValueValidator(5)])
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE)

    def __str__(self):
        return f'Рецепт {self.recipe} имеет тег {self.tag}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MaxValueValidator(1000),
            MinValueValidator(1)])


class Favorites(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorites',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='userfavorites_unique')
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном {self.user}'


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь')

    class Meta:
        verbose_name = 'ShoppingCart'
        verbose_name_plural = 'ShoppingCarts'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='usershoppingcart_unique')]

    def __str__(self):
        return f'Рецепт {self.recipe} в корзине {self.user}'
