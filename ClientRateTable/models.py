from django.db import models
from CustomerLogin.models import Clientinfo

# Create your models here.


class City (models.Model):
    City=models.CharField(max_length=20)
    City_id=models.CharField(max_length=10,primary_key=True)
    
    
class Route(models.Model):
    Route_id=models.CharField(max_length=20,primary_key=True)
    Origin_City=models.ForeignKey(City,on_delete=models.CASCADE,related_name="Origin_City_id")
    Destination_City=models.ForeignKey(City,on_delete=models.CASCADE,related_name="destination_City_id")
    route_name=models.CharField(max_length=20)
    
class Rate(models.Model):
    Route_id = models.ForeignKey(Route,on_delete=models.CASCADE,related_name="Billingconsignment_route_id")
    Client_id=models.ForeignKey(Clientinfo,on_delete=models.CASCADE,related_name="Billing_Client_id")
    Charge_By=models.CharField(max_length=10)
    Charge_per_unit_kg=models.IntegerField()
    Hamali_Charge_Flag=models.CharField(max_length=1)
    Hamali_Charge=models.IntegerField()
    Delivery_Charge=models.IntegerField()
    Pickup_Charge=models.IntegerField()
    