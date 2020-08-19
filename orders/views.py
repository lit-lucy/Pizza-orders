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
    subtype = get_object_or_404(Subtype, pk=subtype_id)
    dish = subtype.dish_set.get(size=request.POST['size'])

    # Get(if order with such session exists) or create order
    # Check not only session, but also status - 'in shopping cart'
    order, created = Order.objects.get_or_create(session=request.session.session_key,
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
    extras = [x for x in extras if x != 0]
    # Check whether exact item already in the order returns boolean
    # If true, get this object 
    if order.orderitem_set.all().filter(dish=dish).exists():
        existing_object = order.orderitem_set.get(dish=dish)
        # Get a list of extra_ids for this item 
        list_of_extras = []
        for extra in existing_object.orderitemextra_set.all():
            list_of_extras.append(extra.extra.id)
        # Compare with a list of extras for an item to be added
        # if True, update quantity of existing_object by one, save
        # else create new order item  
        if sorted(list_of_extras) == sorted(extras):
            existing_object.quantity += 1
            existing_object.save()
        else:  
            order_item = OrderItem(order=order, dish=dish, price=dish.price, quantity=1)
            order_item.save()
            # Add extras to order item
            if extras:
                for extra_id in extras:
                    extra = ExtraType.objects.get(pk=int(extra_id)).extra_set.get(subtype=subtype_id)
                    order_extra = OrderItemExtra(order_item=order_item, extra=extra, price=extra.price)
                    order_extra.save()
            
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
    order = Order.objects.get(session=request.session.session_key)
    # Calculating total for dishes
    price = 0

    for item in order.orderitem_set.all():
        price += item.calculate_total_price()
    
    context = {
    "order": order,
    "total_price": price,
    }
    return render(request, "orders/shopping_cart.html", context)

def delete_from_order(request, item_id):
    order = get_object_or_404(Order, session=request.session.session_key)
    # Check if order has status 'in shopping cart'
    if order.status.name == 'in shopping cart':
        item = order.orderitem_set.get(pk=item_id)
        item.delete()

    return redirect("shopping_cart")
