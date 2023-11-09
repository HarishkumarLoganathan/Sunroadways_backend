

# Create your models here.
from django.db import models
from BranchLogin.models import BranchLoginInfo
from CustomerLogin.models import Clientinfo

# Create your models here.
''' from django.db import models

class Product(models.Model):
    product_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

class Order(models.Model):
    order_number = models.CharField(max_length=10)
    product = models.ForeignKey(Product, to_field='product_code', on_delete=models.CASCADE)
    quantity = models.IntegerField() '''



''' from django.db import models

class Employee(models.Model):
    # Other fields for the Employee model
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.name '''
        
        
class BlindManifestbooking(models.Model):
    Order_Id =  models.CharField(max_length=20,primary_key=True)
    Pickup_City=models.CharField(max_length=20)
    Pickup_Branch = models.ForeignKey(BranchLoginInfo, on_delete=models.CASCADE,related_name='pickup_branch_blindmanifests', default='')
    Client_Id= models.ForeignKey(Clientinfo,on_delete=models.CASCADE,related_name='clientinfo_clientid')
    Delivery_City=models.CharField(max_length=20)
    Delivery_Branch=models.ForeignKey(BranchLoginInfo, on_delete=models.CASCADE,related_name='delivery_branch_blindmanifests',default='')
    Total_Consignment=models.IntegerField(default=0)
    Total_Consignment_Weight=models.IntegerField()
    Total_Article=models.IntegerField()
    Pickup_Truck=models.CharField(max_length=15,default='')
    Pickup_Date=models.DateField()
    Pickup_Time=models.TimeField()
    Pickup_Status=models.CharField(max_length=50)
    
    


    
    