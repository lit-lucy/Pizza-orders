from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Size)
admin.site.register(FoodType)
admin.site.register(Extra)
admin.site.register(Food)
admin.site.register(BasePrice)
admin.site.register(ExtraPrice)
