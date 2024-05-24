from rest_framework import serializers
from datetime import datetime
from .models import PartialManifest
from BranchLogin.models import BranchLoginInfo
from CustomerLogin.models import Clientinfo
from OrderNumber.lrnum import get_LrNumber
from Bookings.models import Bookings


class StudentSubjectSerializer(serializers.Serializer):
    ewaybill_number = serializers.CharField( max_length=100)
    invoice_number = serializers.CharField( max_length=100)

class StudentSubjectsSerializer(serializers.Serializer):
    studentSubjectArray = StudentSubjectSerializer(many=True)

class StudentListSerializer(serializers.Serializer):
    pickup_location = serializers.CharField(source='Pickup_City', max_length=20)
    pickup_branch = serializers.CharField(source='Pickup_Branch', max_length=20)
    drop_location = serializers.CharField(source='Delivery_City', max_length=20)
    delivery_branch = serializers.CharField(source='Delivery_Branch', max_length=20)
    article_count = serializers.IntegerField(source='Total_Article')
    consignment_weight = serializers.IntegerField(source='Total_Consignment_Weight')
    delivery_type = serializers.CharField(source='Delivery_Type', max_length=10)
    consignee_name = serializers.CharField(source='Consignee_Name', max_length=20)
    consignee_GST = serializers.CharField(source='Consignee_GST', max_length=20)
    delivery_address = serializers.CharField(source='Consignee_Delivery_Address', max_length=100)
    delivery_area = serializers.CharField(source='Consignee_Delivery_Area', max_length=30)
    delivery_pincode = serializers.CharField(source='Consignee_Delivery_Pincode', max_length=6)
    delivery_contact = serializers.CharField(source='Consignee_Delivery_Contact', max_length=10)
   # Consignor_id=serializers.CharField(source='Client_ID', max_length=10)
    studentSubjects = StudentSubjectsSerializer()
    
    #Lrnum
    #Orderid
    #booking date
    #booking time
    #pickupstatus


    def create(self, validated_data):
            # Extract the data you need from validated_data
            ewaybill_numbers = [item['ewaybill_number'] for item in validated_data['studentSubjects']['studentSubjectArray']]
            invoice_numbers = [item['invoice_number'] for item in validated_data['studentSubjects']['studentSubjectArray']]
            ewaybill_numbers_str = ', '.join(ewaybill_numbers)
            invoice_numbers_str = ', '.join(invoice_numbers)
            booking_time = datetime.now().strftime("%H:%M:%S")
            booking_date = datetime.now().date()
            print(validated_data['Pickup_Branch'])
            pickup_branch_instance = BranchLoginInfo.objects.get(Branch_Name=validated_data['Pickup_Branch'])
            delivery_branch_instance = BranchLoginInfo.objects.get(Branch_Name=validated_data['Delivery_Branch'])
            
            validated_data.pop('Pickup_Branch')
            validated_data.pop('Delivery_Branch')
            # Modify the data directly within validated_data
            print (validated_data['Consignee_Delivery_Contact'])
            validated_data['Pickup_Branch'] = pickup_branch_instance
            validated_data['Delivery_Branch'] = delivery_branch_instance           
           
            validated_data["Pickup_Status"] = "Pending Confirmation"
            validated_data["Booking_Time"] = booking_time
            validated_data["Booking_Date"] = booking_date
            validated_data["Client_Id"] = "BEERAEE225"
            validated_data["Ewaybill_Number"]=ewaybill_numbers_str
            validated_data["Invoice_Number"]=invoice_numbers_str
            cliend_id_instance=Clientinfo.objects.get(id=validated_data["Client_Id"])
            validated_data.pop('Client_Id')
            validated_data["Client_Id"]=cliend_id_instance
            validated_data.pop('studentSubjects')
            validated_data["Lr_Number"] = get_LrNumber("OrderNumber/Lr_number.txt")
            validated_data["Order_Id"] = self.context.get("Order_Id")

            print (validated_data)
            instance = PartialManifest.objects.create(**validated_data)
            return instance




#Issue
#1. Add Date
#2. Eway Number and Invoice number are not being updated

class PMBranchBooking(serializers.Serializer):
    lr_number=serializers.IntegerField(source='Lr_Number')
    order_id=serializers.CharField(source='Order_Id',max_length=20)
    consignee_name=serializers.CharField(source='Consignee_Name',max_length=20)
    consignee_GST=serializers.CharField(source='Consignee_GST',max_length=20)
    consignee_delivery_address=serializers.CharField(source='Consignee_Delivery_Address',max_length=100)
    consignee_delivery_area=serializers.CharField(source='Consignee_Area',max_length=15)
    delivery_city=serializers.CharField(source='Consignee_City',max_length=15)
    consignee_delivery_contact=serializers.CharField(source='Consignee_Delivery_Contact',max_length=10)
    consignee_delivery_pincode=serializers.IntegerField(source='Consignee_Delivery_Pincode')
    invoice_number=serializers.CharField(source='Invoice_Number',max_length=250)
    ewaybill_number=serializers.CharField(source='Ewaybill_Number',max_length=250)
    delivery_type=serializers.CharField(source='Delivery_Type',max_length=10)
    total_consignment_weight=serializers.IntegerField(source='Total_Consignment_Weight')
    total_article=serializers.IntegerField(source='Total_Article')
    booking_date = serializers.DateField(source='Booking_Date')
    booking_time = serializers.TimeField(source='Booking_Time')
    payment_by=serializers.CharField(source='Payment_By', max_length=10)
    client_id=serializers.CharField(source='Client_Id',max_length=10)
    pickup_branch_id=serializers.CharField(source='Pickup_Branch',max_length=10)
    delivery_branch_id=serializers.CharField(source='Delivery_Branch',max_length=10)
    
    
    
    
    def create(self,validated_data):
        validated_data['Delivery_Status']="AT BOOKING BRANCH"
        
        client_id=validated_data['Client_Id']
        client_id_instance=Clientinfo.objects.get(id=client_id)
        validated_data.pop('Client_Id')
        validated_data["Client_Id"]=client_id_instance
        pickup_branch=validated_data['Pickup_Branch']
        pickup_branch_instance=BranchLoginInfo.objects.get(id=pickup_branch)
        validated_data.pop('Pickup_Branch')
        validated_data['Pickup_Branch']=pickup_branch_instance
        
        delivery_branch=validated_data['Delivery_Branch']
        delivery_branch_instance=BranchLoginInfo.objects.get(id=delivery_branch)
        validated_data.pop('Delivery_Branch')
        validated_data['Delivery_Branch']=delivery_branch_instance
        
        
        
          
        instance=Bookings.objects.create(**validated_data)
       
       
        return instance
        
        
        
        
        
        
        
        
    
    
