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
from .serializers import BlindManifestBookingSerializer
from django.contrib.auth.hashers import make_password
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .serializers import MonthlyBillingSerializer
from .serializers import PaidBillingSerializer
from Billing.models import Billing
from ClientRateTable.models import Rate
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def send_email(subject, body, to_email,from_email):
    print("Sending Email")
    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = from_email  # Replace with your email address
    msg['To'] = to_email
    msg['Subject'] = subject
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server (in this case, using Gmail's SMTP server)
    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Start TLS for security
            server.starttls()
            # Login to the SMTP server with your Gmail credentials
            server.login(from_email, 'Harish@12345')
            # Send the email
            server.sendmail(from_email, to_email, message.as_string())

        print('Email sent successfully!')

    except Exception as e:
        print(f"An error occurred: {e}")
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
                        raise APIException('error' f"The consignee '{data[x]['order_id']}': '{data[x]['consignee_name']}' is not in our monthly payment database. Cannot mark this booking payment as monthly. Please register the consignee in our database.")
                    
                except ObjectDoesNotExist:
                   raise APIException('error' f"The consignee '{data[x]['order_id']}': '{data[x]['consignee_name']}' is not in either customer/monthly billing database. Cannot Proceed with Monthly Billing Option")
                
            else:
            
                payment_client_id=data[x]['client_id']
                try:
                    billing_client_id=Rate.objects.get(Client_id=payment_client_id)
                    payment_client_id_list.append(payment_client_id)
                except ObjectDoesNotExist:
                    raise APIException({'error': f"The consignee 'payment_client_id.Client_Name': '{data[x]['order_id']}' exist in out Customer Database but is not registered as a Monthly Billing Customer"}, status=status.HTTP_400_BAD_REQUEST)
                    

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
                    client_phone=data[x]['delivery_contact']
                    company_address=data[x]['delivery_address']
                    company_area=data[x]['delivery_area']
                    company_city=data[x]['drop_location']
                    company_pincode=data[x]['delivery_pincode']
                    hashed_password = make_password(data[x]['consignee_name']+ '@123')
            
            
            
                    
                
                    Clientinfo.objects.create(Client_Name=client_name,Client_GST=client_gst,Client_Email=client_email,Client_Password=hashed_password,id=id,Company_Address=company_address,Company_Area=company_area,Company_City=company_city,Company_Pincode=company_pincode)
                    payment_client_id= Clientinfo.objects.get(Client_GST=client_gst).id
                    payment_client_id_list.append(payment_client_id)
                    
                    
    print (payment_client_id_list)
    return(payment_client_id_list)
    

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
    
    
    
    
@api_view(['POST'])
def BlindManifestBranchBooking(request):
    



    data = request.data.get('bookingList', [])
    
    try:
        payment_Client_id_list=perform_billing_operations(data)
    
    except APIException as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = BlindManifestBookingSerializer(data=data,many=True)
    
    
        
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
  