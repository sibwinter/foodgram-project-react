from django.db import models

from users.models import User


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
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name[:15]


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название тэга')
    color = models.CharField(max_length=7, default="#ffffff")
    slug = models.SlugField(
        max_length=200,
        verbose_name='Уникальное имя цвета',
        unique=True,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:15]


class Recipes(models.Model):

    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    slug = models.SlugField(
        max_length=200,
        verbose_name='Уникальное имя рецепта',
        unique=True,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата',
        help_text='Укажите дату публикции',
        auto_now_add=True)
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
        verbose_name='список тэгов',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientAmount',
        related_name='recipes',
        verbose_name='Ингредиенты')
    image = models.ImageField(upload_to='uploads/')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name[:15]


class RecipeIngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(

        Recipes,
        on_delete=models.CASCADE
    )
    amount = models.SmallIntegerField(
        verbose_name="Количество"
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return 'Количество игредиента  в рецепте'


class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourite'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favourite'
    )
    
    class Meta:
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique favourite'
            ),
        ]

    def __str__(self):
        return self.user.get_username()


