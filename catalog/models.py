from django.db import models
from datetime import datetime
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f'{self.category_name}'

    class Meta():
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    product_name = models.CharField(max_length=50, verbose_name='наименование')
    desc = models.TextField(verbose_name='описание',
                            **NULLABLE)
    image = models.ImageField(upload_to='products/',
                              verbose_name='превью', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories',
                                 verbose_name='категория')
    quantity_per_unit = models.PositiveIntegerField(verbose_name='цена за шт.', default='0')
    creation_date = models.DateField(verbose_name='дата создания', default=datetime.now)
    last_change_date = models.DateTimeField(verbose_name='дата последнего изменения', default=datetime.now,
                                            **NULLABLE)

    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)

    owner = models.ForeignKey(User, verbose_name='владелец', **NULLABLE, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.category} {self.product_name} '

    class Meta():
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = [
            ('can_change_is_published', 'Can change is_published'),
            ('can_change_desc', 'Can change description'),
            ('can_change_category', 'Can change category')
        ]


class Version(models.Model):
    name = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product",
        verbose_name="Наименование"
    )
    version_number = models.PositiveIntegerField(
        verbose_name="номер версии"
    )
    version_name = models.CharField(
        max_length=100,
        verbose_name="наименование версии"
    )
    current_version = models.BooleanField(
        default=False,
        verbose_name="Признак текущей версии"
    )

    def __str__(self):
        return f"{self.name} {self.version_number} {self.version_name}"

    class Meta:
        verbose_name = "Версия продукта"
        verbose_name_plural = "Версии продуктов"
