from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Size)
admin.site.register(FoodType)
admin.site.register(ExtraType)
admin.site.register(Subtype)
admin.site.register(Dish)
admin.site.register(Extra)
admin.site.register(Status)
admin.site.register(DeliveryType)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemExtra)
