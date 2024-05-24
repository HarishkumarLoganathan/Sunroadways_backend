# Generated by Django 4.2.2 on 2024-01-25 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('BranchLogin', '0002_rename_branch_id_branchlogininfo_id'),
        ('DriverInfo', '0001_initial'),
        ('ClientRateTable', '0002_rename_door_dly_charge_rate_delivery_charge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Line_TripSheet',
            fields=[
                ('Tripsheet_Id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('Vehicle_Number', models.CharField(max_length=10)),
                ('Starting_kms', models.IntegerField()),
                ('Ending_kms', models.IntegerField()),
                ('DateTime', models.DateField()),
                ('status', models.CharField(max_length=30)),
                ('Boarding_Branch_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Boarding_Branch_Id', to='BranchLogin.branchlogininfo')),
                ('Destination_Branch_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Destination_Branch_Id', to='BranchLogin.branchlogininfo')),
                ('Driver_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DriverInfo.driver_info')),
                ('Route_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClientRateTable.route')),
            ],
        ),
    ]
