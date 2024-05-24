from django.db import models

# Create your models here.
class Driver_Info(models.Model):
    Driver_Id=models.CharField(max_length=10,primary_key=True)
    Driver_Name=models.CharField(max_length=25)
    Lisence_Number=models.CharField(max_length=15)
    Phone_Number=models.CharField(max_length=10)
    Native_State=models.CharField(max_length=10)
    Native_City=models.CharField(max_length=15)
    Native_Address=models.CharField(max_length=50)
    Native_Pincode=models.CharField(max_length=6)
    Emergency_Contact=models.CharField(max_length=10)
    Blood_group=models.CharField(max_length=5)