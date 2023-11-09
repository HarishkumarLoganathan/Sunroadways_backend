from django.db import models

# Create your models here.
from django.db import models
from BranchLogin.models import BranchLoginInfo
from CustomerLogin.models import Clientinfo



        
        
class Bookings(models.Model):
    
    Lr_Number =  models.IntegerField(primary_key=True)
    Order_Id =  models.CharField(max_length=20)
    Consignee_Name=models.CharField(max_length=20)
    Consignee_GST=models.CharField(max_length=20)
    Consignee_Delivery_Address=models.CharField(max_length=100)
    Consignee_Area=models.CharField(max_length=15)
    Consignee_City=models.CharField(max_length=15)
    Consignee_Delivery_Contact=models.CharField(max_length=10)
    Consignee_Delivery_Pincode=models.IntegerField()
    Invoice_Number=models.CharField(max_length=250)
    Ewaybill_Number=models.CharField(max_length=250)
    Pickup_Branch = models.ForeignKey(BranchLoginInfo, on_delete=models.CASCADE,related_name="pickup_branch_id")
    Delivery_Branch=models.ForeignKey(BranchLoginInfo, on_delete=models.CASCADE,related_name='delivery_branch_id')
    Delivery_Type=models.CharField(max_length=10)
    Pickup_Type=models.CharField(max_length=10,default="")
    Client_Id= models.ForeignKey(Clientinfo,on_delete=models.CASCADE)
    Total_Consignment_Weight=models.IntegerField(max_length=6)
    Total_Article=models.IntegerField(max_length=5)
    Booking_Date=models.DateField()
    Booking_Time=models.TimeField()
    Delivery_Status=models.CharField(max_length=50)
    Payment_Type=models.CharField(max_length=15)
    Payment_By=models.CharField(max_length=15, default="")
    
    