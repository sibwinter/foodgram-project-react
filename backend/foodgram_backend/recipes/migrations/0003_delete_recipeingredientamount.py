# Generated by Django 4.1.6 on 2023-05-04 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_tag_color'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RecipeIngredientAmount',
        ),
    ]