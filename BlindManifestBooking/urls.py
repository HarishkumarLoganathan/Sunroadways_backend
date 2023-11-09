from django.urls import path
from . import views

urlpatterns = [
     path('BlindManifestBooking/',views.BlindManifestBooking),
     path('BlindManifestList/',views.BlindManifestList),
     path('OrderBooking/',views.BlindManifestOrderBooking),
     
     
     
     
    
]