from django.db import models
from Bookings.models import Bookings
from CustomerLogin.models import Clientinfo

# Create your models here.

class Billing(models.Model):
    Billing_Id=models.CharField(max_length=15,primary_key=True)
    Billing_Lr_Number=models.ForeignKey(Bookings,on_delete=models.CASCADE, related_name='Billing_Lr_Number')
    Description=models.CharField(max_length=50)
    Freight=models.IntegerField()
    Hamali_Charge=models.IntegerField()
    Pickup_Charge=models.IntegerField()
    Delivery_Charge=models.IntegerField()
    Sub_Total=models.IntegerField()
    Gst_Amt=models.IntegerField()
    Total=models.IntegerField()
    Payment_Client=models.ForeignKey(Clientinfo,on_delete=models.CASCADE,related_name='Billing_client_id',default="")
    