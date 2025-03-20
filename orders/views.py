from django.shortcuts import render
from .models import Order
from django.core.paginator import Paginator
from django.views.generic import (
    CreateView)
from .forms import OrderForm
from django.shortcuts import get_object_or_404, redirect, render
# Create your views here.

# def paginator(page_number, post_list):
#     paginator = Paginator(post_list, 5)
#     return paginator.get_page(page_number)

def index(request):
    template = ("order/index.html",)
    order_list = Order.objects.all()
    # page_obj = paginator(request.GET.get("page"), order_list)
    context = {"page_obj": order_list}
    return render(request, template, context)

# def order_detail(request, order_id):
#     template = ("order/detail.html",)
#     order = get_object_or_404(Order, pk=order_id)
#     # Для каждого заказа вычисляем стоимость каждого блюда
#     for item in order.order_items.all():
#         item.total_price = item.dish.price * item.quantity
#         print(item.dish.price, item.quantity, item.total_price)

#     context = {"order": order}
    
    
#     return render(request, template, context)



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