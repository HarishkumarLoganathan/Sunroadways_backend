from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .serializers import StudentListSerializer
from .models import PartialManifest

# Create your views here.
@api_view(['POST'])
def PartialManifestBooking(request):
   # print(request.body)
    response_data = {'message': 'Success'}
    data = request.data.get('studentList', [])

    serialized_data = []
  
    serializer = StudentListSerializer(data=data,many=True)

        
        
    if serializer.is_valid():
        serializer.save()
        
        
    else:
        print(serializer.errors)  

   
   
    


    return Response({'message': 'Success', 'data': serialized_data}, status=201)




@api_view(['GET'])
def PartialManifestList(request):
    branch_id = request.GET.get('branch_id') # Replace this with how you get the branch_id from request.data

# Query to retrieve the data
    data = PartialManifest.objects.filter(
    Delivery_Branch=branch_id  # Filter by Branch id
).values(
    'Client_Id__Client_Name',  # Consignor_name
    'Lr_Number',
    'Consignee_Name',
    'Delivery_City',
    'Consignee_Delivery_Area',  # Delivery_Area
    'Consignee_Delivery_Pincode',
    'Total_Consignment_Weight',  # Consignment_weight
    'Consignee_Delivery_Contact',  # Delivery_Contact
    'Pickup_Status',
    'Order_Id',
    'Total_Article'
)
    
    return Response( data, status=201)