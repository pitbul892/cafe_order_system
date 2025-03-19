from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import constants as c


class Dish(models.Model):
    """Модель блюда."""

    name = models.CharField('Название блюда', max_length=100)
    price = models.DecimalField('Стоимость блюда',
                                max_digits=6,
                                decimal_places=2)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return f'{self.name} - {self.price} руб'


class OrderItem(models.Model):
    """Модель для связи блюда и заказа."""

    order = models.ForeignKey('Order',
                              on_delete=models.CASCADE,
                              related_name='order_items',
                              verbose_name='Заказ')
    dish = models.ForeignKey(Dish,
                             on_delete=models.CASCADE,
                             verbose_name='Блюдо')
    quantity = models.PositiveIntegerField('Количество', default=1)

    def __str__(self):
        return f"{self.dish.name} - {self.dish.price} руб.- {self.quantity} шт"


class Order(models.Model):
    """Модель заказа."""

    table_number = models.IntegerField('Номер стола')
    items = models.ManyToManyField(Dish, through='OrderItem',
                                   verbose_name='Список блюд')
    total_price = models.DecimalField('Стоимость заказа',
                                      max_digits=8,
                                      decimal_places=2,
                                      default=0,
                                      editable=False)
    status = models.CharField('Статус', max_length=100,
                              choices=c.STATUS_CHOICES, default='waiting')

    @staticmethod
    @receiver(post_save, sender=OrderItem)
    def update_order_total(sender, instance, **kwargs):
        # Получаем заказ, к которому относится этот элемент
        order = instance.order
        order.calculate_total_price()
        order.save()

    def calculate_total_price(self):
        """Вычисление общей стоимости заказа."""
        total = sum(
            order_item.dish.price * order_item.quantity
            for order_item in self.order_items.all()
        )
        self.total_price = total
    def get_status_display(self):
        return dict(c.STATUS_CHOICES).get(self.status, self.status)
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    def __str__(self):
        return f"{self.id} заказ, стол №{self.table_number}"