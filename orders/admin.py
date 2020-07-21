from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Sizes)
admin.site.register(Types)
admin.site.register(Extras)
admin.site.register(FullTypes)
admin.site.register(BasePrices)
admin.site.register(ExtraPrices)
