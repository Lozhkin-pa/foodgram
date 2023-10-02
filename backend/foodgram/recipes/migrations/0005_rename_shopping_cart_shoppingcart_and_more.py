# Generated by Django 4.2.5 on 2023-10-02 11:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0004_ingredient_unique_name_measurement_unit'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Shopping_cart',
            new_name='ShoppingCart',
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('id',), 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(blank=True, max_length=7, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')], verbose_name='Цвет в HEX'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator(regex='^([A-Fa-f)/(А-Яа-я])$')], verbose_name='Название тега'),
        ),
    ]