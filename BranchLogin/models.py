from django.db import models


# Create your models here.
class BranchLoginInfo(models.Model):
    Branch_Name=  models.CharField(max_length=500)
    Branch_Address =  models.CharField(max_length=500)
    Branch_City =  models.CharField(max_length=500)
    Branch_State = models.CharField (max_length=200)
    Branch_Email = models.CharField(max_length=500)
    Branch_Password=models.CharField(max_length=20)
    id=models.CharField(max_length=10,primary_key=True)
    
    
    
    
    