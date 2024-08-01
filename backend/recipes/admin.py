from django.contrib import admin

from .models import (
    Tag, Recipe, Ingredient,
    RecipeIngredient, RecipeTag,
    Favorites, ShoppingCart
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'display_tags', 'favorite_count')
    list_filter = ('author', 'name', 'tags__name',)
    search_fields = ('name', 'author__username', 'tags__name')
    inlines = [RecipeIngredientInline]

    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    display_tags.short_description = 'Tags'

    def favorite_count(self, obj):
        return obj.in_favorites.count()

    favorite_count.short_description = 'Favorite Count'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeTag)
admin.site.register(RecipeIngredient)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
