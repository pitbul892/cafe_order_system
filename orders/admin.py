from django.contrib import admin

from .models import Dish, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline для отображения блюд и их количества в заказе."""

    model = OrderItem
    verbose_name = 'Блюдо'
    verbose_name_plural = 'Блюда'
    extra = 1  # Количество пустых форм блюд
    min_num = 1  # Минколичество блюд


class OrderAdmin(admin.ModelAdmin):
    """Отображение заказов в админке."""

    readonly_fields = ('total_price',)
    list_display = ('table_number', 'total_price', 'status')
    inlines = [OrderItemInline]


admin.site.register(Dish)
admin.site.register(Order, OrderAdmin)
