# Generated by Django 4.2.2 on 2024-01-25 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Tripsheet', '0001_initial'),
        ('Bookings', '0005_bookings_pickup_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracking_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Lr_Number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bookings.bookings')),
                ('Trip_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tripsheet.line_tripsheet')),
            ],
        ),
    ]
