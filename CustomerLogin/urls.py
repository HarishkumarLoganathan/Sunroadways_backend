from django.urls import path
from . import views

urlpatterns = [
     path('ClientSignin/',views.Client_Signin),
     path('ClientLogin/',views.client_Login),
    
]