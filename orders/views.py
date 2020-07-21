from django.http import HttpResponse
from django.shortcuts import render

from .models import Sizes

# Create your views here.
def index(request):
    context = {
        "sizes": Sizes.objects.all()
    }
    return render(request, "orders/index.html", context)
