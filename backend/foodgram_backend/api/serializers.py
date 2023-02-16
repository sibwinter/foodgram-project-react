from rest_framework import serializers
from recipes.models import Recipes, Ingredient, Favourite
from recipes.models import Follow, Tag, RecipeIngredientAmount


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('name', 'slug', 'pub_date', 'text', 'cooking_time', 'author', 'tags', 'ingradients', 'image') 