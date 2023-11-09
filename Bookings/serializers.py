from CustomerLogin.models import Clientinfo
from BranchLogin.models import BranchLoginInfo
from rest_framework import serializers
from datetime import datetime
from .models import Bookings



class BookingsSerialers(serializers.Serializer):
    nearest_branch= serializers.CharField(source='Delivery_Branch', max_length=15)
    article_count=serializers.CharField(source='Total_Article',max_length=5)
    consignment_weight=serializers.CharField(source='Total_Consignment_Weight',max_length=6)
    delivery_type=serializers.CharField(source='Delivery_Type',max_length=10)
    pickup_type=serializers.CharField(source="Pickup_Type",max_length=10)
    consignee_name=serializers.CharField(source='Consignee_Name',max_length=20)
    consignee_gst=serializers.CharField(source='Consignee_GST',max_length=15)
    
    consignee_address=serializers.CharField(source='Consignee_Delivery_Address',max_length=100)
    consignee_area=serializers.CharField(source='Consignee_Area',max_length=15)
    consignee_city=serializers.CharField(source='Consignee_City',max_length=15)
    consignee_pincode=serializers.IntegerField(source='Consignee_Delivery_Pincode')
    consignee_contact=serializers.CharField(source='Consignee_Delivery_Contact',max_length=10)
    payment_by=serializers.CharField(source='Payment_By')
    invoice_number=serializers.CharField(source='Invoice_Number',max_length=250)
    ewaybill_number=serializers.CharField(source='Ewaybill_Number',max_length=250)
    pickup_branch_id=serializers.CharField(source='Pickup_Branch', max_length=15)
    payment_type=serializers.CharField(source="Payment_Type",max_length=20)
    
    
    
    def create(self,validated_data):
        print (validated_data['Delivery_Branch'])
        delivery_branch_id=BranchLoginInfo.objects.get(Branch_Name=validated_data['Delivery_Branch'])
        validated_data.pop('Delivery_Branch')
        validated_data['Delivery_Branch']=delivery_branch_id
        print ("Thalaiva")
        print (validated_data['Pickup_Branch'])
        
        pickup_branchid=BranchLoginInfo.objects.get(id=validated_data['Pickup_Branch'])
        validated_data.pop('Pickup_Branch')
        validated_data['Pickup_Branch']=pickup_branchid
        
        consignor_gst=self.context.get('consignor_gst')
        consignor_id=Clientinfo.objects.get(Client_GST=consignor_gst)
        consignee_id=Clientinfo.objects.get(Client_GST=validated_data['Consignee_GST'])
    
        validated_data['Client_Id']=consignor_id
        
        '''if validated_data['Payment_Client_id'] == "CONSIGNEE":
            payment_client_id=consignee_id
            print ("CONSIGNOR")
        else:
            print (validated_data['Client_Id'])
            
            try:
                payment_client_id = consignor_id
            
            except Clientinfo.DoesNotExist:
                print("Clientinfo object with the provided Client_Id does not exist.")
            
         '''   
        #validated_data.pop('Payment_Client_id')
        #validated_data['Payment_Client_id']=payment_client_id
        validated_data['Delivery_Status']="Booking Completed"
        booking_time = datetime.now().strftime("%H:%M:%S")
        booking_date = datetime.now().date()
        validated_data['Booking_Date']=booking_date
        validated_data['Booking_Time']=booking_time
        validated_data['Lr_Number']=789173
        validated_data['Order_Id']="7138491"
        
        instance = Bookings.objects.create(**validated_data)
        return instance
        
        
        
        
            
        
        
        
        

    
    """ Lr_Number =  models.IntegerField(primary_key=True)
    Order_Id =  models.CharField(max_length=20)
    Consignee_Name=models.CharField(max_length=20)
    Consignee_GST=models.CharField(max_length=20)
    Consignee_Delivery_Address=models.CharField(max_length=100)
    Consignee_Area=models.CharField(max_length=15)
    Consignee_City=models.CharField(max_length=15)
    Consignee_Delivery_Contact=models.IntegerField
    Invoice_Number=models.CharField(max_length=250)
    Ewaybill_Number=models.CharField(max_length=250)
    Pickup_Branch = models.ForeignKey(BranchLoginInfo, on_delete=models.CASCADE,related_name="pickup_branch_id")
    Delivery_Branch=models.ForeignKey(BranchLoginInfo, on_delete=models.CASCADE,related_name='delivery_branch_id')
    Delivery_Type=models.CharField(max_length=10)
    Client_Id= models.ForeignKey(Clientinfo,on_delete=models.CASCADE)
    Total_Consignment_Weight=models.IntegerField(max_length=6)
    Total_Article=models.IntegerField(max_length=5)
    Description=modles.CharField(max_length=50)
    Booking_Date=models.DateField()
    Booking_Time=models.TimeField()
    Delivery_Status=models.CharField(max_length=15)
    
    Billing_By=models.CharField(max_length=15)
    Payment_Client_id=models.ForeignKey(Clientinfo, on_delete=models.CASCADE,related_name='payment_client_id')
    """
#LR NUMBER - NEW
#Order id -NEW
#Delivery_Branch
#Pickup_Branch
#Booking_Date
#Booking_Time
#Delivery_Status
#Payment_Client_id
#Client_ID



