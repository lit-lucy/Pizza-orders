from django.conf import settings
from django.db import models

# Create your models here.

class Size(models.Model):
    size = models.CharField(max_length=64)

    def __str__(self):
        return f"Size: {self.size}"


class FoodType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class ExtraType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Subtype(models.Model):
    food_type = models.ForeignKey(FoodType,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number_of_extras = models.IntegerField()

    def __str__(self):
        return f"{self.name}"

class Dish(models.Model):
    subtype = models.ForeignKey(Subtype,
        on_delete=models.CASCADE)
    size = models.ForeignKey(Size,
        on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.subtype}, {self.size}, ${self.price}"

class Extra(models.Model):
    subtype = models.ForeignKey(Subtype,
        on_delete=models.CASCADE)
    extra_type = models.ForeignKey(ExtraType,
        on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.subtype} ({self.extra_type})"

class Order(models.Model):
    # Statuses 
    IN_SHOPPING_CART = 1
    CONFIRMED = 2
    READY_TO_PICK_UP = 3
    PICKED_UP = 4
    STATUS_CHOICES = (
        (IN_SHOPPING_CART, 'In shopping cart'),
        (CONFIRMED, 'Confirmed'),
        (READY_TO_PICK_UP, 'Ready to pick up'),
        (PICKED_UP, 'Picked up'),

    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=IN_SHOPPING_CART, 
    )
    # Delivery types
    PICK_UP = 1
    DELIVERY_CHOICES = (
        (PICK_UP, 'Pick up in a restaurant'),
    )
    delivery_type = models.IntegerField(
        choices=DELIVERY_CHOICES,
        default=PICK_UP, 
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT)
    time_created = models.DateTimeField()

    is_paid = models.BooleanField()
    session = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} from {self.user}"

    def status_str(self):
        return self.STATUS_CHOICES[self.status-1][1]

    def delivery_type_str(self):
        return self.DELIVERY_CHOICES[self.delivery_type-1][1]

    def add_item_or_change_quantity(self, extras, dish, subtype_id):
        if self.orderitem_set.all().filter(dish=dish).exists():
            existing_item = self.orderitem_set.get(dish=dish)
            # Get a list of extra_ids for this item 
            list_of_extras = []
            for extra in existing_item.orderitemextra_set.all():
                list_of_extras.append(extra.extra.id)
            # Compare with a list of extras for an item to be added
            # if True, update quantity of existing_item by one, save
            # else create new order item  
            if sorted(list_of_extras) == sorted(extras):
                existing_item.quantity += 1
                existing_item.save()
                return 
        order_item = OrderItem(order=self, dish=dish, price=dish.price, quantity=1)
        order_item.save()
        # Add extras to order item
        if extras:
            for extra_id in extras:
                extra = ExtraType.objects.get(pk=int(extra_id)).extra_set.get(subtype=subtype_id)
                order_extra = OrderItemExtra(order_item=order_item, extra=extra, price=extra.price)
                order_extra.save()
        return

    def total_for_order(self):
        price = 0
        for item in self.orderitem_set.all():
            price += item.calculate_total_price()
        return price 

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
        on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish,
        on_delete=models.PROTECT)
    price = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.dish}, quantity: {self.quantity}"

    def calculate_total_price(self):
        price = self.price
        for extra in self.orderitemextra_set.all():
                price += extra.price
        return price

class OrderItemExtra(models.Model):
    order_item = models.ForeignKey(OrderItem,
        on_delete=models.CASCADE)
    extra = models.ForeignKey(Extra, 
        on_delete=models.PROTECT)
    price = models.FloatField()

    def __str__(self):
        return f"{self.extra}"





