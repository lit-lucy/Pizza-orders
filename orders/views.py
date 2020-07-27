from django.http import HttpResponse
from django.shortcuts import render

from .models import *

# Create your views here.
def index(request):

    context = {

        "food_types": FoodType.objects.all(),
        
    }
    return render(request, "orders/index.html", context)
