from django.urls import path
from . import views

urlpatterns = [
     path('BranchSignup/',views.Branch_Signup),
     path('BranchLogin/',views.Branch_Login),
    
]