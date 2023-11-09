from django.urls import path
from . import views

urlpatterns = [
     path('PartialManifestBooking/',views.PartialManifestBooking),
     path('PartialManifestList/',views.PartialManifestList)
     
    
]