from django.db import models

# Create your models here.

class Sizes(models.Model):
    size = models.CharField(max_length=64)

    def __str__(self):
        return f"Size: {self.size}"


class Types(models.Model):
    type_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.type_name}"

class Extras(models.Model):
    extras_name = models.CharField(max_length=100)

class FullTypes(models.Model):
    type_id = models.ForeignKey(Types,
        on_delete=models.CASCADE)
    full_type_name = models.CharField(max_length=100)
    number_of_extras = models.IntegerField()

class BasePrices(models.Model):
    fulltype_id = models.ForeignKey(FullTypes,
        on_delete=models.CASCADE)
    size_id = models.ForeignKey(Sizes,
        on_delete=models.CASCADE)
    price = models.FloatField()

class ExtraPrices(models.Model):
    fulltype_id = models.ForeignKey(FullTypes,
        on_delete=models.CASCADE)
    extras_id = models.ForeignKey(Extras,
        on_delete=models.CASCADE)
    extra_price = models.FloatField()
