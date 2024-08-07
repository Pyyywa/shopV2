# Generated by Django 5.0.7 on 2024-08-01 08:37

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, verbose_name='наименование')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50, verbose_name='наименование')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='превью')),
                ('quantity_per_unit', models.PositiveIntegerField(default='0', verbose_name='цена за шт.')),
                ('creation_date', models.DateField(default=datetime.datetime.now, verbose_name='дата создания')),
                ('last_change_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='дата последнего изменения')),
                ('views_count', models.IntegerField(default=0, verbose_name='просмотры')),
                ('is_published', models.BooleanField(default=True, verbose_name='опубликовано')),
                ('slug', models.CharField(blank=True, max_length=150, null=True, verbose_name='slug')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='catalog.category', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.PositiveIntegerField(verbose_name='номер версии')),
                ('version_name', models.CharField(max_length=100, verbose_name='наименование версии')),
                ('current_version', models.BooleanField(default=False, verbose_name='Признак текущей версии')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='catalog.product', verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Версия продукта',
                'verbose_name_plural': 'Версии продуктов',
            },
        ),
    ]
