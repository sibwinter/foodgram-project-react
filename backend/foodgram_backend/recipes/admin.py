from django.contrib import admin

from recipes.models import Recipes, Tag, Ingredient, IngredientAmount, Favourite, ShoppingCart


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    list_filter = ('name', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    list_filter = ('name', 'slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', )
    list_filter = ('name', )

@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingredient', 'amount',)
    list_filter = ('ingredient', )



@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', )

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', )


