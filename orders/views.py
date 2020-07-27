from django.http import HttpResponse
from django.shortcuts import render

from .models import *

# Create your views here.
def index(request):
    menu_items = {}
    food = Food.objects.all()


    for i in range(len(food)):
        food_type = food[i].food_type.type_name
        if food_type in menu_items:
            menu_items[food_type].append(food[i].food_name)
        else:
            menu_items[food_type] = [food[i].food_name]

    context = {
        "menu_items": menu_items,
        "food": food,
        "food_types": FoodType.objects.all()
    }
    return render(request, "orders/index.html", context)
