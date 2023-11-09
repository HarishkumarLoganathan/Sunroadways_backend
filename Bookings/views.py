from django.shortcuts import render
from Billing.serializers import BillingSerializer
from .serializers import BookingsSerialers
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from Billing.serializers import MonthlyBillingSerializer





# Create your views here.

@api_view(['POST'])
def BranchBookings(request):
    data=request.data
    
    

    
    #first serializer should return model,Lr_number,Payment_Client_id
    
    #LR_Number and Payment_Client_id
    
    serializer = BookingsSerialers(data=data,context={'consignor_gst': request.data.get('consignor_gst')})

    #data['billing_lr_number']=Lr_Number
    #data['payment_client_id']=payment_client_id
    #print (serializer,Lr_Number,payment_client_id)
    
    
    if serializer.is_valid():
        
        instance=serializer.save()
        serialized_data = serializer.data
        Lr_Number=instance.Lr_Number
        print (Lr_Number)
        
    
        

        
        
        
    else:
        print(serializer.errors)
        return Response({'message': 'Success', 'data': serializer.errors}, status=201)
    
    
    
    if request.data.get('payment_type')=="MONTHLY BILLING":
        print ("MONTHLY BILLING CUSTOMER")
        try:
            print (Lr_Number)
            billingserializer=MonthlyBillingSerializer(data=data,context={'Lr_Number': Lr_Number,'consginor_gst':request.data.get('consignor_gst'),'consginee_gst':request.data.get('consignee_gst')})
        except Exception as e:
            print ("ERROR")
            print (billingserializer.errors)
    else:
        print (data)
        billingserializer=BillingSerializer(data=data,context={'Lr_Number': Lr_Number,'consginor_gst':request.data.get('consignor_gst'),'consginee_gst':request.data.get('consignee_gst')})
        
        
    if billingserializer.is_valid():
        billingserializer.save()
        return Response({'message': 'Success', 'data': billingserializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Validation Error', 'data': billingserializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    




    
    
    
    
    
    
    
    
    return Response({'message': 'Success', 'data': sliced_data}, status=201)
    
