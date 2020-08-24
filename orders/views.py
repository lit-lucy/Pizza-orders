from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from .models import *
from django.contrib.auth.models import User

def index(request):
    context = {
        "food_types": FoodType.objects.all(),
    }
    return render(request, "orders/index.html", context)

def food_modifications(request, subtype_id):
    subtype = get_object_or_404(Subtype, pk=subtype_id)

    context = {
        "subtype": subtype,
        "range": range(subtype.number_of_extras),
    }

    return render(request, "orders/food.html", context)

def add_to_order(request, subtype_id):
    dish = get_object_or_404(Subtype, pk=subtype_id).dish_set.get(size=request.POST['size'])

    order, created = Order.objects.get_or_create(session=request.session.session_key,
        status=1,  # Status 'in shopping cart'
        defaults={
            'session': request.session.session_key,
            'status': Status.objects.get(pk=1), # Status 'in shopping cart'
            'user': User.objects.get(pk=2), # Test user
            'time_created': timezone.now(),
            'delivery_type': DeliveryType.objects.get(pk=1), # Type 'pick up'
            'is_paid': False
            })
    
    extras = request.POST.getlist('extras')
    # Remover 0 from the list (0 = no extras)
    extras = [x for x in extras if x != '0']

    order.add_item_or_change_quantity(extras, dish, subtype_id)
            
    return redirect("last_added_item", order_id=order.id)

def last_added_item(request, order_id):
    last_item_in_order = Order.objects.get(pk=order_id).orderitem_set.all().last()
    price = last_item_in_order.calculate_total_price()

    context = {
    "order_item": last_item_in_order,
    "price": price,

    }
    return render(request, "orders/check.html", context)

def shopping_cart(request):
    order = get_object_or_404(Order, session=request.session.session_key, status=1)
    # Calculating total for dishes
    price = order.total_for_order()
    
    context = {
    "order": order,
    "total_price": price,
    }
    return render(request, "orders/shopping_cart.html", context)

def delete_from_order(request, item_id):
    item = get_object_or_404(Order, session=request.session.session_key,status=1).orderitem_set.get(pk=item_id)
    item.delete()

    return redirect("shopping_cart")

def change_quantity(request, item_id):
    item = get_object_or_404(Order, session=request.session.session_key,status=1).orderitem_set.get(pk=item_id)
    number = request.POST['quantity']
    item.quantity = int(number)
    item.save()
    return redirect("shopping_cart")

def confirm_order(request):
    order = get_object_or_404(Order, session=request.session.session_key, status=1)
    order.status=Status.objects.get(pk=2) # Status 'confirmed'
    order.save()

    return redirect("order_status")

def order_status(request):
    context = {
    "orders": Order.objects.all().filter(session=request.session.session_key).exclude(status=1)
    }
    return render(request, "orders/order_status.html", context)

