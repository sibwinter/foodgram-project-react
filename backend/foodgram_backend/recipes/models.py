from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        default="кг"
    )


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название тэга')
    color = models.CharField(max_length=7, default="#ffffff")
    slug = models.SlugField(
        max_length=200,
        verbose_name='Уникальное имя цвета',
        unique=True,
    )

class Recipes(models.Model):

    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    text = models.TextField(
        verbose_name='Описание рецепта',
        null=True,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, мин',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='список тэгов'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Ingredients_with_amount',
        verbose_name='список ингредиентов'
    )


class Ingredients_with_amount(models.Model):
    ingredient = models.ForeignKey(Ingredient)
    amount = models.SmallIntegerField(
        verbose_name="Количество"
    )
