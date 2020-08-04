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
        return f"{self.subtype} ({self.extra_type}), {self.price}$"
