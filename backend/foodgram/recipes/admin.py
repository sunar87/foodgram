"""Настройки админки."""

from django.contrib import admin

from .models import (
    RecipeIngredient,
    Recipe,
    Favorite,
    Ingredient,
    ShoppingCart,
    Tag
)

admin.site.disable_action("delete_selected")


@admin.action(description='Удалить %(verbose_name)s')
def delete(modeladmin, request, obj):
    """Удаляет выбранный объект."""
    obj.delete()


class IngredientAdmin(admin.ModelAdmin):
    """Настройки отображения модели Ingredient в админке."""

    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    actions = [delete]


class TagAdmin(admin.ModelAdmin):
    """Настройки отображения модели Tag в админке."""

    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    actions = [delete]


class RecipeIngredientInline(admin.StackedInline):
    """Инлайн для ингредиентов рецепта."""

    model = RecipeIngredient
    extra = 0
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    """Настройки отображения модели Recipe в админке."""

    inlines = [RecipeIngredientInline]
    list_display = ('name', 'author', 'favorites_count')
    search_fields = ('name', 'author__username')
    list_filter = ('tags',)
    exclude = ('ingredients',)
    actions = [delete]

    def favorites_count(self, obj):
        """Возвращает количество избранных."""
        return obj.favorite.count()


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
