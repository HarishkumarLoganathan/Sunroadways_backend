from django.db import models
from ClientRateTable.models import Route
from BranchLogin.models import BranchLoginInfo
from DriverInfo.models import Driver_Info

# Create your models here.
class Line_TripSheet(models.Model):
    Tripsheet_Id=models.CharField(primary_key=True,max_length=15)
    Route_Id=models.ForeignKey(Route, on_delete=models.CASCADE)
    Boarding_Branch_Id=models.ForeignKey(BranchLoginInfo, on_delete=models.CASCADE,related_name='Boarding_Branch_Id')
    Destination_Branch_Id=models.ForeignKey(BranchLoginInfo,on_delete=models.CASCADE,related_name='Destination_Branch_Id')
    Driver_Id=models.ForeignKey(Driver_Info,on_delete=models.CASCADE)
    Vehicle_Number=models.CharField(max_length=10)
    Starting_kms=models.IntegerField()
    Ending_kms=models.IntegerField()
    DateTime=models.DateField()
    status=models.CharField(max_length=30)