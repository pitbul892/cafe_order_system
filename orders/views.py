from django.shortcuts import render
from .models import Order
from django.core.paginator import Paginator
from django.views.generic import (
    CreateView)
from .forms import OrderForm
from django.shortcuts import get_object_or_404, redirect, render
import constants as c
from django.utils import timezone
# Create your views here.

# def paginator(page_number, post_list):
#     paginator = Paginator(post_list, 5)
#     return paginator.get_page(page_number)
today = timezone.now().date()
def order_list(request):
    
    template = ("order/index.html",)
    query = request.GET.get("q", "").strip().capitalize()  # Получаем параметр из поисковой строки
    orders = Order.objects.filter(pub_date__date=today)

    if query:
        # Преобразуем запрос, если это русский статус
        status_filter = c.STATUS_DICT.get(query) 

        if status_filter:
            orders = orders.filter(status=status_filter)
        else:
            orders = orders.filter(table_number__icontains=query)
    # page_obj = paginator(request.GET.get("page"), order_list)
    context = {"page_obj": orders}
    return render(request, template, context)




def order_detail(request, order_id):
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

def order_delete(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        order.delete()
        return redirect("orders:index")
    return render(request, "order/confirm_delete.html", {"order": order})

from .forms import OrderItemForm
from .models import Dish, OrderItem
from django.views.generic import View
from django.http import JsonResponse

class OrderCreateView(View):
    """Страница для создания нового заказа."""

    def get(self, request):

        order_form = OrderForm()
        item_form = OrderItemForm()
        dishes = Dish.objects.all()
        
        return render(request, 'order/create.html', {
            'order_form': order_form,
            'item_form': item_form,
            'dishes': dishes,
        })

    def post(self, request):
        order_items_data = request.POST.getlist('order_items')  # передаем данные как список
        order = Order.objects.create(table_number=request.POST['table_number'])

        # Обрабатываем блюда
        for item in order_items_data:
            try:
                dish_id, quantity = item.split(":")
                dish = Dish.objects.get(id=dish_id)
                OrderItem.objects.create(order=order, dish=dish, quantity=int(quantity))
            except Exception as e:
                return render(request, 'order/create.html', {'error': f"Ошибка при обработке блюда: {e}"})
        return redirect("orders:index")
    
def revenue_for_shift(request):
    template = ("order/revenue.html",)
    orders = Order.objects.filter(pub_date__date=today, status='Paid')
    total_revenue = sum(order.total_price for order in orders)
    total_orders = orders.count()
    context = {"total_revenue": total_revenue,
               'total_orders': total_orders}
    return render(request, template, context)
