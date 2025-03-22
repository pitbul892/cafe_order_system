import csv
import os

import django
from django.db.utils import IntegrityError

# Указываем Django, где находятся настройки проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Инициализируем Django
django.setup()
import csv

from orders.models import Dish

# Открываем CSV файл
with open('dishes.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    try:
        for row in reader:
            name = row['name']
            price = row['price']
            
            # Создаем запись в модели Dish
            Dish.objects.create(name=name, price=price)
        print('Блюда успешно загружены')
    except IntegrityError:
        print('Данные уже были загружены')

