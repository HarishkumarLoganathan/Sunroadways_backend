# Generated by Django 4.2.2 on 2023-10-22 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Billing', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billing',
            name='Client_Invoice',
        ),
    ]
