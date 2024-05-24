from .models import BlindManifestbooking
from Bookings.models import Bookings
from CustomerLogin.models import Clientinfo
from BranchLogin.models import BranchLoginInfo
from rest_framework import serializers
from datetime import datetime
from BranchLogin.models import BranchLoginInfo
from OrderNumber.lrnum import get_LrNumber
from OrderNumber.lrnum import get_LrNumber
import sys
import logging
from ClientRateTable.models import Rate
from Billing.models import Billing



#clientinfo_clientid
logger = logging.getLogger(__name__)



class BlindManifestSerializer(serializers.Serializer):
    pickup_location=serializers.CharField(source='Pickup_City',max_length=15)
    pickup_branch=serializers.CharField(source='Pickup_Branch',max_length=15)
    drop_location=serializers.CharField(source='Delivery_City',max_length=15)
    delivery_branch=serializers.CharField(source='Delivery_Branch',max_length=15)
    total_consignment=serializers.IntegerField(source='Total_Consignment')
    total_weight=serializers.IntegerField(source='Total_Consignment_Weight')
    total_article=serializers.IntegerField(source='Total_Article')
    vehicle_type=serializers.CharField(source='Pickup_Truck')
    pickup_time=serializers.TimeField(source='Pickup_Time')
    client_id=serializers.CharField(source='Client_Id',max_length=15)
    

    def create(self, validated_data):
        
        
        Pickup_Date = datetime.now()
        Pickup_Status="Pending Confirmation"
        Order_Id="172138"
        clientinfo_clientid = Clientinfo.objects.get(id=validated_data['Client_Id'])
        pickup_branch=BranchLoginInfo.objects.get(Branch_Name=validated_data['Pickup_Branch'])
        delivery_branch=BranchLoginInfo.objects.get(Branch_Name=validated_data['Delivery_Branch'])
        validated_data.pop('Client_Id')
        validated_data.pop('Pickup_Branch')
        validated_data.pop('Delivery_Branch')
        validated_data['Client_Id']=clientinfo_clientid
        validated_data['Pickup_Branch']=pickup_branch
        validated_data['Delivery_Branch']=delivery_branch
        instance = BlindManifestbooking.objects.create(Pickup_Date=Pickup_Date,Pickup_Status=Pickup_Status,Order_Id=Order_Id,**validated_data)
        print(instance)
        return instance
    
class EwayInvoiceSerializer(serializers.Serializer):
    ewaybill_number = serializers.CharField( max_length=100)
    invoice_number = serializers.CharField( max_length=100)

class InvoicingSerializer(serializers.Serializer):
    invoicedetailArray = EwayInvoiceSerializer(many=True)
    
    
class BlindManifestBookingSerializer(serializers.Serializer):
    
    order_id=serializers.CharField(source='Order_Id',max_length=20) 
    consignee_name=serializers.CharField(source='Consignee_Name',max_length=20)
    consignee_GST=serializers.CharField(source='Consignee_GST',max_length=20)
    delivery_address=serializers.CharField(source='Consignee_Delivery_Address',max_length=100)
    delivery_area=serializers.CharField(source='Consignee_Area',max_length=15)
    drop_location=serializers.CharField(source='Consignee_City',max_length=15)
    delivery_contact=serializers.CharField(source='Consignee_Delivery_Contact',max_length=10)
    delivery_pincode=serializers.IntegerField(source='Consignee_Delivery_Pincode')
    delivery_type=serializers.CharField(source='Delivery_Type',max_length=10)
    consignment_weight=serializers.IntegerField(source='Total_Consignment_Weight')
    article_count=serializers.IntegerField(source='Total_Article')
    payment_type=serializers.CharField(source='Payment_Type',max_length=20)
    payment_by=serializers.CharField(source='Payment_By',max_length=15)
    client_id=serializers.CharField(source="Client_Id",max_length=10)
    pickup_branch=serializers.CharField(source="Pickup_Branch",max_length=10)
    delivery_branch=serializers.CharField(source="Delivery_Branch",max_length=20)
    invoicedetail=InvoicingSerializer()
   
   
    def create(self,validated_data):
        
        
        validated_data['Booking_Date'] = datetime.now()
        validated_data['Booking_Time']=datetime.now().strftime("%H:%M:%S")
        validated_data['Delivery_Status']="AT BOOKING BRANCH"
        client_id=Clientinfo.objects.get(id=validated_data['Client_Id'])
        validated_data.pop('Client_Id')
        validated_data['Client_Id']=client_id
        pickup_branch=BranchLoginInfo.objects.get(id=validated_data['Pickup_Branch'])
        validated_data.pop('Pickup_Branch')
        validated_data['Pickup_Branch']=pickup_branch
        delivery_branch=BranchLoginInfo.objects.get(Branch_Name=validated_data['Delivery_Branch'])
        validated_data.pop('Delivery_Branch')
        validated_data['Delivery_Branch']=delivery_branch
        validated_data['Pickup_Type']="DOOR"
        ewaybill_numbers = [item['ewaybill_number'] for item in validated_data['invoicedetail']['invoicedetailArray']]
        invoice_numbers = [item['invoice_number'] for item in validated_data['invoicedetail']['invoicedetailArray']]
        ewaybill_numbers_str = ', '.join(ewaybill_numbers)
        invoice_numbers_str = ', '.join(invoice_numbers)
        validated_data["Ewaybill_Number"]=ewaybill_numbers_str
        validated_data["Invoice_Number"]=invoice_numbers_str
        validated_data["Lr_Number"]=get_LrNumber("OrderNumber/Lr_number.txt")
        validated_data.pop('invoicedetail')
        
        #print ("LR NUMBER")
        
       
        instance=Bookings.objects.create(**validated_data)
       
       
        return instance
    
    
class PaidBillingSerializer(serializers.Serializer):
    consignment_description=serializers.CharField(source="Description",max_length=50)
    freight_amount=serializers.IntegerField(source="Freight")
    hamali_charge=serializers.IntegerField(source="Hamali_Charge")
    delivery_charge=serializers.IntegerField(source="Pickup_Charge")
    pickup_charge=serializers.IntegerField(source="Delivery_Charge")
    
    
    def create(self,validated_data):
        
        validated_data["Sub_Total"]=validated_data["Freight"]+validated_data["Hamali_Charge"]+validated_data["Pickup_Charge"]+validated_data["Delivery_Charge"]
        validated_data['Gst_Amt']=validated_data['Sub_Total']*.05
        validated_data['Total']=validated_data['Sub_Total']+validated_data['Gst_Amt']
        validated_data['Payment_Client']=self.context.get('payment_client_id')
        client_id=Clientinfo.objects.get(id=validated_data["Payment_Client"])
        validated_data.pop('Payment_Client')
        validated_data['Payment_Client']=client_id
        validated_data['Billing_Id']=get_LrNumber("OrderNumber/Billing_id.txt")
        
        validated_data['Billing_Lr_Number']=Bookings.objects.get(Lr_Number=self.context.get('Lr_Number'))
        instance=Billing.objects.create(**validated_data)
        return instance
        
        
        
class MonthlyBillingSerializer(serializers.Serializer):
    
    consignment_description=serializers.CharField(source="Description",max_length=50)
    
    def create(self,validated_data):

        payment_client_id = self.context.get('payment_client_id')
        validated_data['Payment_Client'] = Clientinfo.objects.get(id=payment_client_id)
        payment_rate_info=Rate.objects.get(Client_id=validated_data['Payment_Client'])
        
        
        charge_by=payment_rate_info.Charge_By
        bookings=Bookings.objects.get(Lr_Number= self.context.get('Lr_Number'))
        consignment_weight=bookings.Total_Consignment_Weight
        article_count=bookings.Total_Article
        print (consignment_weight,article_count)
        if charge_by=="Weight":
            freight=consignment_weight*payment_rate_info.Charge_per_unit_kg
            hamali=(consignment_weight/100)*payment_rate_info.Hamali_Charge
        else:
            freight=article_count*payment_rate_info.Charge_per_unit_kg
            hamali=(article_count)*payment_rate_info.Hamali_Charge
            
            
        validated_data["Freight"]=freight
        validated_data["Hamali_Charge"]=hamali

        
        
        if bookings.Pickup_Type=="DOOR":
            
            validated_data["Pickup_Charge"]=payment_rate_info.Pickup_Charge
            
            
        else:
            validated_data['Pickup_Charge']=0
            
          
        print (Bookings.Delivery_Type)
        if bookings.Delivery_Type=="DOOR":
            
            validated_data['Delivery_Charge']=payment_rate_info.Delivery_Charge
        else:
            validated_data['Delivery_Charge']=0
            
        validated_data["Sub_Total"]=validated_data["Freight"]+validated_data["Hamali_Charge"]+validated_data["Pickup_Charge"]+validated_data["Delivery_Charge"]
        validated_data['Gst_Amt']=validated_data['Sub_Total']*.05
        validated_data['Total']=validated_data['Sub_Total']+validated_data['Gst_Amt']

        validated_data['Billing_Id']=get_LrNumber("OrderNumber/Billing_id.txt")
        validated_data['Billing_Lr_Number']=Bookings.objects.get(Lr_Number=self.context.get('Lr_Number'))
        
        instance=Billing.objects.create(**validated_data)
        return instance
        
        
        
        



 
   
    