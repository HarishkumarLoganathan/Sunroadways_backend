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
from django.contrib.auth.hashers import make_password
from OrderNumber.lrnum import get_LrNumber
from django.db.models import Sum,Count

from django.db.models.functions import Concat
from django.db import connection
from .serializers import PMBranchBooking
from CustomerLogin.models import Clientinfo
from BlindManifestBooking.serializers import MonthlyBillingSerializer,PaidBillingSerializer
from ClientRateTable.models import Rate
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist





def perform_billing_operations(data):
    
    payment_client_id_list=[]
    for x in range (0,len(data)):
        if data[x]['payment_type']=='MONTHLY BILLING':
            if data[x]['payment_by']=="CONSIGNEE":
                try: 
                    payment_client_id= Clientinfo.objects.get(Client_GST=data[x]['consignee_GST']).id
                    try:
                        billing_client_id=Rate.objects.get(Client_id=payment_client_id)
                        payment_client_id_list.append(payment_client_id)
                    except ObjectDoesNotExist:
                        raise APIException('error' f"The consignee '{data[x]['lr_number']}': '{data[x]['consignee_name']}' is not in our monthly payment database. Cannot mark this booking payment as monthly. Please register the consignee in our database.")
                    
                except ObjectDoesNotExist:
                   raise APIException('error' f"The consignee '{data[x]['lr_number']}': '{data[x]['consignee_name']}' is not in either customer/monthly billing database. Cannot Proceed with Monthly Billing Option")
                
            else:
            
                payment_client_id=data[x]['client_id']
                try:
                    billing_client_id=Rate.objects.get(Client_id=payment_client_id)
                    payment_client_id_list.append(payment_client_id)
                except ObjectDoesNotExist:
                    raise APIException({'error': f"The consignee 'payment_client_id.Client_Name': '{data[x]['lr_number']}' exist in out Customer Database but is not registered as a Monthly Billing Customer"}, status=status.HTTP_400_BAD_REQUEST)
                    

        else:
            print ("THIS IS NOT A MONTHLY BILLING")
            if (data[x]['payment_by']=="CONSIGNOR"):
                payment_client_id=data[x]['client_id']
                payment_client_id_list.append(payment_client_id)
                
            else:
                
                try: 
                    payment_client_id= Clientinfo.objects.get(Client_GST=data[x]['consignee_GST']).id
                    payment_client_id_list.append(payment_client_id)
                except:
                    id=data[x]['consignee_name'][:2]+data[x]['consignee_name'][-2:]+data[x]['consignee_GST'][2:5]+data[x]['consignee_GST'][-7:-4]
                    client_name=data[x]['consignee_name']
                    client_gst=data[x]['consignee_GST']
                    client_email=data[x]['consignee_email']
                    client_phone=data[x]['consignee_delivery_contact']
                    company_address=data[x]['consignee_delivery_address']
                    company_area=data[x]['consignee_delivery_area']
                    company_city=data[x]['delivery_city']
                    company_pincode=data[x]['consignee_delivery_pincode']
                    hashed_password = make_password(data[x]['consignee_name']+ '@123')
            
            
            
                    
                
                    Clientinfo.objects.create(Client_Name=client_name,Client_GST=client_gst,Client_Email=client_email,Client_Password=hashed_password,id=id,Company_Address=company_address,Company_Area=company_area,Company_City=company_city,Company_Pincode=company_pincode)
                    payment_client_id= Clientinfo.objects.get(Client_GST=client_gst).id
                    payment_client_id_list.append(payment_client_id)
                    
                    
    print (payment_client_id_list)
    return(payment_client_id_list)
                
                
            
            
            
                    
        



    '''if (data['payment_by']=="CONSIGNOR"):
        payment_client_id=data['client_id']
        
    else:
        
       
        try: 
         payment_client_id= Clientinfo.objects.get(Client_GST=data['consignee_GST']).id
        except:
            id=data['consignee_name'][:2]+data['consignee_name'][-2:]+data['consignee_GST'][2:5]+data['consignee_GST'][-7:-4]
            client_name=data['consignee_name']
            client_gst=data['consignee_GST']
            client_email=data['consignee_email']
            client_phone=data['delivery_contact']
            company_address=data['delivery_address']
            company_area=data['delivery_area']
            company_city=data['drop_location']
            company_pincode=data['delivery_pincode']
            hashed_password = make_password(data['consignee_name']+ '@123')
            
            
            
            payment_client_id=id
            Clientinfo.objects.create(Client_Name=client_name,Client_GST=client_gst,Client_Email=client_email,Client_Password=hashed_password,id=id,Company_Address=company_address,Company_Area=company_area,Company_City=company_city,Company_Pincode=company_pincode)
    print (payment_client_id)
    
    if (data['payment_type']=="MONTHLY BILLING"):
        print ("MONTHLY BILLING")
        
        try:
            
            Billing_Detail=Rate.objects.get(Client_id=payment_client_id)
            # ADD ROUTE ID TO THIS
            
           
            print (serializer)
            return serializer
        except Rate.DoesNotExist:
            print ("ERROR")
        
            return Response({'error': 'Clientinfo MONTHLY BILLING INFO does not exist in our Database.'}, status=status.HTTP_400_BAD_REQUEST)

            
    
    else:
    
        serializer=PaidBillingSerializer(data=data,context={'payment_client_id':payment_client_id,'Lr_Number':lr_number})
    
        return serializer'''

# Create your views here.
@api_view(['POST'])
def PartialManifestBooking(request):
   # print(request.body)
    response_data = {'message': 'Success'}
    data = request.data.get('studentList', [])

    serialized_data = []
    
    order_id=get_LrNumber("OrderNumber/Lr_number.txt")
  
    serializer = StudentListSerializer(data=data,many=True,context={"Order_Id":order_id})

        
        
    if serializer.is_valid():
        serializer.save()
        
        
    else:
        print(serializer.errors)  

   
   
    


    return Response({'message': 'Success', 'data': serialized_data}, status=201)




@api_view(['GET'])
def PartialManifestList(request):
    branch_id = request.GET.get('branch_id') # Replace this with how you get the branch_id from request.data
    print(branch_id)
# Query to retrieve the data
    data = PartialManifest.objects.filter(
    Pickup_Branch=branch_id  
).values(
    'Order_Id',
    'Client_Id__Client_Name', 
    'Client_Id__Client_Phone',
    'Client_Id__Company_Area',
    'Client_Id__Company_Pincode',
    'Pickup_Status'
 
    
).annotate(Total_Weight=Sum('Total_Consignment_Weight'),Total_Articles=Sum('Total_Article'),Total_Consignments=Count('Lr_Number'))
    
    return Response( data, status=201)


@api_view(['GET'])
def PartialManifestOrderBooking(request):
    
    order_id= (request.GET.get('order_id'))
    
    
    data =PartialManifest.objects.filter(Order_Id=order_id).values()
    print (data)
    
    
    
    if not data:
        # If no data is found, return an error response
        error_message = f"Record not found for Order ID: {order_id}"
        return Response({'error': order_id +'Not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response( data, status=201) 
    

    
    
@api_view(['POST'])
def PartialManifestBranchBooking(request):
    
    data = request.data.get('bookingList', [])
    
    try:
        payment_Client_id_list=perform_billing_operations(data)
    
    except APIException as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = PMBranchBooking(data=data,many=True)
    
    
        
    if serializer.is_valid():
    
        instance=serializer.save()
       
           
    else:
         return Response({'error': str(serializer.errors)}, status=201)
            


    for x in range(0,len(instance)):
        Lr_Number=instance[x].Lr_Number
        print ("Started Billing")
        
        if data[x]['payment_type']=="MONTHLY BILLING":
            print (payment_Client_id_list[x])
            billing_serializer=MonthlyBillingSerializer(data=data[x],context={'payment_client_id':payment_Client_id_list[x],'Lr_Number':Lr_Number})
        else:
            print (payment_Client_id_list[x])
            billing_serializer=PaidBillingSerializer(data=data[x],context={'payment_client_id':payment_Client_id_list[x],'Lr_Number':Lr_Number})
       
        
    
        

        if billing_serializer.is_valid():
            print (billing_serializer)
            billing_serializer.save()
            print ("Sucess")
         
        else:
            print (billing_serializer.errors)
            return Response({'error': str(billing_serializer.errors)}, status=201)
            
                
    return Response('success', status=200)
  

    
    
        
        
        
    
    