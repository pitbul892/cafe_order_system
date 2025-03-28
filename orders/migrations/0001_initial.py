# Generated by Django 4.2.8 on 2025-03-21 08:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название блюда')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Стоимость блюда')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(verbose_name='Номер стола')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=8, verbose_name='Стоимость заказа')),
                ('status', models.CharField(choices=[('Waiting', 'В ожидании'), ('Ready', 'Готово'), ('Paid', 'Оплачено')], default='Waiting', max_length=100, verbose_name='Статус')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.dish', verbose_name='Блюдо')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.order', verbose_name='Заказ')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='orders.OrderItem', to='orders.dish', verbose_name='Список блюд'),
        ),
    ]
