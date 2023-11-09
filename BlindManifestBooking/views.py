from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from .models import BlindManifestbooking
from CustomerLogin.models import Clientinfo
from BranchLogin.models import BranchLoginInfo
from rest_framework.decorators import api_view
from django.http import HttpResponse,JsonResponse
import json
from .serializers import BlindManifestSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

# Create your views here.

@api_view(['POST'])
def BlindManifestBooking(request):
    data = json.loads(request.body)
    print(data)
    serializer = BlindManifestSerializer(data=data)

        
        
    if serializer.is_valid():
        print("VALID SERIALIZER")
        serializer.save()
        
        
    else:
        print ("DEBUG")
        print(serializer.errors)  
    
    return Response({'message': 'Success'}, status=201)

    
    

#Order Id----- Need to create
#Branch Id: ---- yes
#Client Id:   --- Yes
#pick up City --- Yes
#Pickup Branch --- Yes
#Pickup Branch id (optional)
#Delivery City --- Yes
# Delivery Branch --- Yes
#Delivery Branch Id(optional)
#Total Weight: Yes
#Total Article Count: Yes
#Pick up date: Yes
# Pick up time: Yes 
# Pick up Status: Need to Set


#All set start to code
@api_view(['GET'])
def BlindManifestList(request):
    branch_id = request.GET.get('branch_id') # Replace this with how you get the branch_id from request.data

# Query to retrieve the data
    data = BlindManifestbooking.objects.filter(
    Delivery_Branch=branch_id  # Filter by Branch id
).values(
    'Order_Id',
    'Client_Id__Client_Name',  # Consignor_name
    'Delivery_City',
    'Total_Consignment_Weight',
    'Total_Article',
    'Client_Id__Client_Phone', 
    'Pickup_Truck',
    'Total_Consignment',
    'Client_Id',# Delivery_Contact
    'Pickup_Status',
    
)
    
    return Response( data, status=201)





@api_view(['GET'])
def BlindManifestOrderBooking(request):
    order_id = request.GET.get('order_id')
    print (order_id)# Replace this with how you get the branch_id from request.data

# Query to retrieve the data
    data = BlindManifestbooking.objects.filter(
    Order_Id=order_id  # Filter by Branch id
).values(
    
'Client_Id',
'Total_Consignment',
'Order_Id'
)
    if not data:
        # If no data is found, return an error response
        error_message = f"Record not found for Order ID: {order_id}"
        return Response({'error': order_id +'Not found'}, status=status.HTTP_404_NOT_FOUND)
    print (data)
    return Response( data, status=201)
    