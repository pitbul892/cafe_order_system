# from django.core.paginator import Paginator
from typing import Any

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import View

import constants as c

from .forms import OrderForm, OrderItemForm
from .models import Dish, Order, OrderItem

# def paginator(page_number, post_list):
#     paginator = Paginator(post_list, 5)
#     return paginator.get_page(page_number)

today = timezone.now().date()


def order_list(request: Any) -> Any:
    """Получение списка."""
    template = 'order/index.html'
    # Получаем параметр из поисковой строки
    query = request.GET.get('q', '').strip().capitalize()
    orders = Order.objects.filter(pub_date__date=today)

    if status_filter := c.STATUS_DICT.get(query):
        # Преобразуем запрос, если это русский статус
        status_filter = c.STATUS_DICT.get(query)

        if status_filter:
            orders = orders.filter(status=status_filter)
        else:
            orders = orders.filter(table_number__icontains=query)
    # page_obj = paginator(request.GET.get("page"), order_list)
    context = {"page_obj": orders}
    return render(request, template, context)


def order_detail(request: Any, order_id: int) -> Any:
    """Получение по id."""
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        # Обработаем форму изменения статуса
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status
            order.save()
            return redirect('orders:order_detail', order_id=order.id)
    context = {
        'order': order,
    }

    return render(request, 'order/detail.html', context)


def order_delete(request: Any, order_id: int) -> Any:
    """Удаление заказа."""
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        order.delete()
        return redirect("orders:index")
    return render(request, "order/confirm_delete.html", {"order": order})


class OrderCreateView(View):
    """Страница для создания нового заказа."""

    def get(self, request: Any) -> Any:
        """Вывод формы."""
        order_form = OrderForm()
        item_form = OrderItemForm()
        dishes = Dish.objects.all()

        return render(request, 'order/create.html', {
            'order_form': order_form,
            'item_form': item_form,
            'dishes': dishes,
        })

    def post(self, request: Any) -> Any:
        """Создание заказа."""
        order_items_data = request.POST.getlist('order_items')
        order = Order.objects.create(table_number=request.POST['table_number'])

        # Обрабатываем блюда
        for item in order_items_data:
            try:
                dish_id, quantity = item.split(":")
                dish = Dish.objects.get(id=dish_id)
                OrderItem.objects.create(
                    order=order,
                    dish=dish,
                    quantity=int(quantity))
            except Exception as e:
                return render(
                    request,
                    'order/create.html',
                    {'error': f'Ошибка при обработке блюда: {e}'})
        return redirect("orders:index")


def revenue_for_shift(request: Any) -> Any:
    """Получение выручки за смену."""
    template = "order/revenue.html"
    orders = Order.objects.filter(pub_date__date=today, status='Paid')
    total_revenue = sum(order.total_price for order in orders)
    total_orders = orders.count()
    context = {"total_revenue": total_revenue,
               'total_orders': total_orders}
    return render(request, template, context)
