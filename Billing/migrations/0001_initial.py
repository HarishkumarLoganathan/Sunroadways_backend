# Generated by Django 4.2.2 on 2023-10-22 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('Billing_Id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('Client_Invoice', models.CharField(max_length=250)),
                ('Description', models.CharField(max_length=50)),
                ('Freight', models.IntegerField()),
                ('Hamali_Charge', models.IntegerField()),
                ('Pickup_Charge', models.IntegerField()),
                ('Delivery_Charge', models.IntegerField()),
                ('Sub_Total', models.IntegerField()),
                ('Gst_Amt', models.IntegerField()),
                ('Total', models.IntegerField()),
            ],
        ),
    ]
