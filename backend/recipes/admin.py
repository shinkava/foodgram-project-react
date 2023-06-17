from django.contrib import admin

from .models import (
    FavoriteRecipe, Ingredient, Recipe, RecipeIngredient, ShoppingList, Tag
)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)
    ordering = ('color',)
    empty_value_display = "-пусто-"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
        'get_recipes_count',
    )
    search_fields = ('name',)
    ordering = ('measurement_unit',)
    empty_value_display = "-пусто-"

    def get_recipes_count(self, obj):
        return RecipeIngredient.objects.filter(ingredient=obj.id).count()

    get_recipes_count.short_description = ('Использований в рецептах')


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 1


@admin.register(RecipeIngredient)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = ('id', 'recipe', 'ingredient')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'in_favorite',
    )
    list_filter = ('name', 'author', 'tags',)
    readonly_fields = ('in_favorite',)
    inlines = (RecipeIngredientsInline,)
    empty_value_display = "-пусто-"

    def in_favorite(self, obj):
        return obj.in_favorite.all().count()

    in_favorite.short_description = ('Количество добавлений в избранное')


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
