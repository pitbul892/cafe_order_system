from django import forms

from .models import Order, OrderItem


class OrderItemForm(forms.ModelForm):
    """Форма для добавления блюда в заказ."""

    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity']


class OrderForm(forms.ModelForm):
    """Форма для создания нового заказа."""

    class Meta:
        model = Order
        fields = ['table_number']

    def clean_table_number(self):
        """Валидация номера стола."""
        table_number = self.cleaned_data.get('table_number')
        if table_number <= 0:
            raise forms.ValidationError(
                'Номер стола должен быть положительным.')
        return table_number
