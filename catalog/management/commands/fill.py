from django.core.management import BaseCommand
from catalog.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        category_list = [
            {'category_name': 'Laptop',
             'description': '15.6HP Laptop 15 15.6" '
                            'HD/Intel Celeron N4120 1.1ГГц/8Гб DDR4 '
                            'RAM/512Гб SSD/'
                            'Intel UHD Graphics 600/Windows 11 Pro'},
            {'category_name': 'Monitor'},
            {'category_name': 'Phone'},
            {'category_name': 'Notebook'}
        ]

        category_for_create = []
        for category_item in category_list:
            category_for_create.append(
                Category(**category_item)
            )

        Category.objects.all().delete()
        Category.objects.bulk_create(category_for_create)
