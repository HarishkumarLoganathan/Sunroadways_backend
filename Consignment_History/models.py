from django.db import models
from Tripsheet.models import Line_TripSheet
from Bookings.models import Bookings

# Create your models here.
class Tracking_History(models.Model):
    Trip_Id=models.ForeignKey(Line_TripSheet,on_delete=models.CASCADE)
    Lr_Number=models.ForeignKey(Bookings,on_delete=models.CASCADE)
    