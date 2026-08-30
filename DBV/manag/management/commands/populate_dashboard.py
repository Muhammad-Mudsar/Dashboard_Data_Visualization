import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from manag.models import Category, Product, Order

class Command(BaseCommand):
    help = 'Populates database with sample dashboard data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Order.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Create categories
        categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
        category_objs = [Category.objects.create(name=name) for name in categories]

        # Create products
        products_data = [
            ('Laptop', 'Electronics', Decimal('999.99')),
            ('Smartphone', 'Electronics', Decimal('699.99')),
            ('Headphones', 'Electronics', Decimal('199.99')),
            ('T-shirt', 'Clothing', Decimal('19.99')),
            ('Jeans', 'Clothing', Decimal('49.99')),
            ('Jacket', 'Clothing', Decimal('89.99')),
            ('Sofa', 'Home & Garden', Decimal('499.99')),
            ('Lamp', 'Home & Garden', Decimal('29.99')),
            ('Plant Pot', 'Home & Garden', Decimal('14.99')),
            ('Yoga Mat', 'Sports', Decimal('39.99')),
            ('Dumbbells', 'Sports', Decimal('79.99')),
            ('Basketball', 'Sports', Decimal('24.99')),
            ('Fiction Novel', 'Books', Decimal('12.99')),
            ('Cookbook', 'Books', Decimal('18.99')),
            ('Children Book', 'Books', Decimal('9.99')),
        ]

        category_map = {cat.name: cat for cat in category_objs}
        products = []
        for name, cat_name, price in products_data:
            product = Product.objects.create(
                name=name,
                category=category_map[cat_name],
                price=price
            )
            products.append(product)

        # Create orders over last 30 days
        today = timezone.now().date()
        for i in range(300):  # 300 orders
            product = random.choice(products)
            days_ago = random.randint(0, 29)
            order_date = timezone.make_aware(
                timezone.datetime.combine(
                    today - timedelta(days=days_ago),
                    timezone.datetime.min.time()
                ) + timedelta(
                    hours=random.randint(9, 18),
                    minutes=random.randint(0, 59)
                )
            )
            quantity = random.randint(1, 5)
            # Apply occasional discount? For simplicity total = price * quantity
            total = product.price * quantity

            Order.objects.create(
                product=product,
                quantity=quantity,
                order_date=order_date,
                total_price=total
            )

        self.stdout.write(self.style.SUCCESS('Dashboard sample data created successfully'))


        # Scripting backend data for tables |this will add dummy data| python manage.py populate_dashboard