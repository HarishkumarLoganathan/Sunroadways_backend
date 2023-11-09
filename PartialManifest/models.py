from django.db import models
from BranchLogin.models import BranchLoginInfo
from CustomerLogin.models import Clientinfo



        
        
class PartialManifest(models.Model):
    
    Lr_Number =  models.IntegerField(primary_key=True)
    Order_Id =  models.CharField(max_length=20)
    Pickup_City=models.CharField(max_length=20)
    Pickup_Branch = models.ForeignKey(BranchLoginInfo, on_delete=models.CASCADE,related_name='pickup_branch_partialManifest')
    Delivery_City=models.CharField(max_length=20)
    Delivery_Branch=models.ForeignKey(BranchLoginInfo, on_delete=models.CASCADE,related_name='delivery_branch_partialManifest')
    Delivery_Type=models.CharField(max_length=10)
    Client_Id=models.ForeignKey(Clientinfo,on_delete=models.CASCADE,related_name='Consginor_Id')
    Consignee_Name=models.CharField(max_length=20)
    Consignee_GST=models.CharField(max_length=20)
    Consignee_Delivery_Address=models.CharField(max_length=100)
    Consignee_Delivery_Area=models.CharField(max_length=30)
    Consignee_Delivery_Pincode=models.IntegerField(default=0)
    Consignee_Delivery_Contact=models.CharField(default='',max_length=10)
    Total_Consignment_Weight=models.IntegerField(max_length=6)
    Total_Article=models.IntegerField(max_length=5)
    Booking_Date=models.DateField()
    Booking_Time=models.TimeField()
    Invoice_Number=models.CharField(max_length=250)
    Ewaybill_Number=models.CharField(max_length=250)
    Pickup_Status=models.CharField(max_length=30)
    
    

    
    