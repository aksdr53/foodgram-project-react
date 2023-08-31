from django.contrib import admin

from .models import Ingredient, IngredientsAmount, Recipe, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color',
                    'slug')


class IngredientAmountInline(admin.TabularInline):
    model = IngredientsAmount


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', )


class IngredientsAmountAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',
                    'in_favorites')
    list_filter = ('author', 'name', 'tags')
    inlines = [
        IngredientAmountInline,
    ]

    def in_favorites(self, obj):
        return obj.recipe_in_users_favorites.count()


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientsAdmin)
admin.site.register(IngredientsAmount, IngredientsAmountAdmin)
