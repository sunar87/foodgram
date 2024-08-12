from django_filters.rest_framework import filters, FilterSet

from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(FilterSet):
    """Фильтр рецептов."""

    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(), field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset


class IngredientFilter(FilterSet):
    """Фильтрация ингредиентов."""

    name = filters.CharFilter(lookup_expr='istartswith',)

    class Meta:
        model = Ingredient
        fields = ('name',)
