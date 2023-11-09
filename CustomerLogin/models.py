from django.db import models


class Clientinfo(models.Model):
    Client_Name=  models.CharField(max_length=500)
    Client_GST =  models.CharField(max_length=500)
    Client_Email = models.CharField (max_length=200)
    Client_Password = models.CharField(max_length=500)
    Client_Phone=models.CharField(max_length=20)
    Company_Pincode=models.IntegerField(max_length=6,default=0) 
    Company_City=models.CharField(max_length=15,default="")
    Company_Area=models.CharField(max_length=15,default="")
    Company_Address=models.CharField(max_length=50,default="")
    id=models.CharField(max_length=10,primary_key=True)
    
    
    