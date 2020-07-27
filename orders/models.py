from django.db import models

# Create your models here.

class Size(models.Model):
    size = models.CharField(max_length=64)

    def __str__(self):
        return f"Size: {self.size}"


class FoodType(models.Model):
    type_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.type_name}"

class Extra(models.Model):
    extras_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.extras_name}"

class Food(models.Model):
    food_type = models.ForeignKey(FoodType,
        on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    number_of_extras = models.IntegerField()

    def __str__(self):
        return f"{self.food_name}"

class BasePrice(models.Model):
    food = models.ForeignKey(Food,
        on_delete=models.CASCADE)
    size = models.ForeignKey(Size,
        on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.size}, {self.price}$"

class ExtraPrice(models.Model):
    food = models.ForeignKey(Food,
        on_delete=models.CASCADE)
    extra = models.ForeignKey(Extra,
        on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.food} ({self.extra}), {self.price}$"
