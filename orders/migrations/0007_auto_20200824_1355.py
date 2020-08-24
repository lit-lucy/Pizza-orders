# Generated by Django 3.0.7 on 2020-08-24 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20200824_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'In shopping cart'), (2, 'Confirmed'), (3, 'Ready to pick up'), (4, 'Picked up')], default=1),
        ),
    ]