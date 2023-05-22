from django_filters import rest_framework
from distutils.util import strtobool

from recipes.models import Favourite, Recipe, ShoppingCart, Tag, Ingredient


class IngredientFilter(rest_framework.FilterSet):
    name = rest_framework.filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(rest_framework.FilterSet):
    is_favorited = rest_framework.BooleanFilter(
        method='is_favorited_method'
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='is_in_shopping_cart_method'
    )
    author = rest_framework.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    def is_favorited_method(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()

        recipe = Favourite.objects.values_list("id", flat=True)
        new_queryset = queryset.filter(id__in=recipe)

        if not strtobool(value):
            return queryset.difference(new_queryset)

        return queryset.filter(id__in=recipe)

    def is_in_shopping_cart_method(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()

        shopping_cart = ShoppingCart.objects.filter(user=self.request.user)
        recipe = [item.recipe.id for item in shopping_cart]
        new_queryset = queryset.filter(id__in=recipe)

        if not strtobool(value):
            return queryset.difference(new_queryset)

        return queryset.filter(id__in=recipe)

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
