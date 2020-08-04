from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import *

# Create your views here.
def index(request):
    context = {
        "food_types": FoodType.objects.all(),
    }
    return render(request, "orders/index.html", context)

def food_modifications(request, subtype_id):
    try:
        subtype = Subtype.objects.get(id=subtype_id)
    except Subtype.DoesNotExist:
        raise Http404("Dish does not exist")

    context = {
        "subtype": subtype,
        "range": range(subtype.number_of_extras),
    }

    return render(request, "orders/food.html", context)

def add_to_order(request, subtype_id):
    subtype = get_object_or_404(Subtype, pk=subtype_id)
    # Add try and except 
    dish_price = subtype.dish_set.get(size=request.POST['size']).price
    extra_price = 0

    extras = request.POST.getlist('extras')
    for extra in extras:
        if extra != '0':
            extra_price += ExtraType.objects.get(pk=int(extra)).extra_set.get(subtype=subtype_id).price


    context = {
        "price": dish_price + extra_price,
        "dish": subtype,
        "extras": extras,
        "dish_price": subtype.dish_set.get(size=request.POST['size']),

    } 

    return render(request, "orders/check.html", context)
