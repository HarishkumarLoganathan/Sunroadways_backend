# Generated by Django 4.2.2 on 2023-10-11 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PartialManifest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partialmanifest',
            name='Consignee_Delivery_Contact',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='partialmanifest',
            name='Consignee_Delivery_Pincode',
            field=models.IntegerField(default=0),
        ),
    ]
