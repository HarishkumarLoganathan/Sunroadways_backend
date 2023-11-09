# Generated by Django 4.2.2 on 2023-10-18 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BranchLogin', '0002_rename_branch_id_branchlogininfo_id'),
        ('BlindManifestBooking', '0003_alter_blindmanifestbooking_client_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='blindmanifestbooking',
            name='Delivery_Branch',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='delivery_branch_blindmanifests', to='BranchLogin.branchlogininfo'),
        ),
        migrations.AddField(
            model_name='blindmanifestbooking',
            name='Pickup_Branch',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='pickup_branch_blindmanifests', to='BranchLogin.branchlogininfo'),
        ),
        migrations.AlterField(
            model_name='blindmanifestbooking',
            name='Delivery_City',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='blindmanifestbooking',
            name='Pickup_City',
            field=models.CharField(max_length=20),
        ),
    ]