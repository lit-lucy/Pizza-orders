# Generated by Django 3.0.7 on 2020-08-13 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='session',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
