# Generated by Django 4.2.2 on 2023-10-28 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ClientRateTable', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rate',
            old_name='Door_Dly_Charge',
            new_name='Delivery_Charge',
        ),
    ]
