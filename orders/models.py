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
        return f"{self.subtype} ({self.extra_type}), ${self.price}"

class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class DeliveryType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class Order(models.Model):
    status = models.ForeignKey(Status, 
        on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT)
    time_created = models.DateTimeField()
    delivery_type = models.ForeignKey(DeliveryType,
        on_delete=models.PROTECT)
    is_paid = models.BooleanField()
    session = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.id} from {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
        on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish,
        on_delete=models.PROTECT)
    price = models.FloatField()

    def __str__(self):
        return f"{self.dish} from {self.order} order"

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
        return f"{self.extra} for {self.order_item}"





