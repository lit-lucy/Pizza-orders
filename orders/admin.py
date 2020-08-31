from django.contrib import admin

from .models import *

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_id','get_items')

    def get_id(self, obj):
        return obj.id
    def get_items(self, obj):
        items_with_extras = {}
        items = obj.orderitem_set.all()
        for item in items:
            if item.orderitemextra_set.all().exists():
                items_with_extras[str(item)] = list(item.orderitemextra_set.all())
            else:
                items_with_extras[str(item)] = 'no extras'
        return items_with_extras
    def get_extras(self, obj):
        pass

    get_id.admin_order_field = 'id'
    get_id.short_description = 'Order id'

    get_items.admin_order_field = 'item'
    get_items.short_description = 'Order item'

admin.site.register(Size)
admin.site.register(FoodType)
admin.site.register(ExtraType)
admin.site.register(Subtype)
admin.site.register(Dish)
admin.site.register(Extra)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(OrderItemExtra)
