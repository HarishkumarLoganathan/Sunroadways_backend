from rest_framework import serializers
from Billing.models import Billing
''' class Billing(models.Model):
    Billing_Id=models.CharField(max_length=15)
    Client_Invoice=models.CharField(max_length=250)
    Lr_Number=models.ForeignKey(Bookings,on_delete=models.CASCADE, related_name='Lr_Number')
    Description=models.CharField(max_length=50)
    Freight=models.IntegerField()
    Hamali_Charge=models.IntegerField()
    Pickup_Charge=models.IntegerField()
    Delivery_Charge=models.IntegerField()
    Sub_Total=models.IntegerField()
    Gst_Amt=models.IntegerField()
    Total=models.IntegerField() '''
    
from Bookings.models import Bookings
from ClientRateTable.models import Rate
from CustomerLogin.models import Clientinfo


class BillingSerializer(serializers.Serializer):
   # billing_lr_number=serializers.CharField(source='Billing_Lr_Number',max_length=15)
    consignment_description=serializers.CharField(source='Description',max_length=50)
    freight_amount=serializers.IntegerField(source='Freight')
    hamali_charge=serializers.IntegerField(source='Hamali_Charge')
    pickup_charge=serializers.IntegerField(source='Pickup_Charge')
    delivery_charge=serializers.IntegerField(source='Delivery_Charge')

    payment_by=serializers.CharField(source='Payment_Client',max_length=15)

    
    
    def create(self,validated_data):
        validated_data['Billing_Id']="SR102"
        #validated_data['Payment_Client']=Clientinfo.objects.get(id=payment_client_id)
        billing_lr_number=self.context.get('Lr_Number')
        object_lr=Bookings.objects.get(Lr_Number=billing_lr_number)
        validated_data['Billing_Lr_Number']=object_lr
        if validated_data['Payment_Client'] == "CONSIGNEE":
            payment_client_id=Clientinfo.objects.get(Client_GST=self.context.get('consginee_gst'))
            print ("CONSIGNOR")
        else:
            payment_client_id=Clientinfo.objects.get(Client_GST=self.context.get('consginor_gst'))
            print ("CONSIGNOR")
            
            
        validated_data.pop('Payment_Client')
        #payment_client_id="BEERAEE225"
        validated_data['Payment_Client']=payment_client_id
        validated_data['Sub_Total']=validated_data['Freight']+validated_data['Hamali_Charge']+validated_data['Pickup_Charge']+validated_data['Delivery_Charge']
        validated_data['Gst_Amt']=validated_data['Sub_Total']*.05
        validated_data['Total']=validated_data['Sub_Total']+validated_data['Gst_Amt']
        print (validated_data)
        instance=Billing.objects.create(**validated_data)
        return instance
        
        #consignment_description
        #delivery_charge
        #freight_amount
        #hamali_charge
        #payment_by
        #payment_type
        #pickup_type
        
        #Hint - Monthly billing serializer
        
class MonthlyBillingSerializer(serializers.Serializer):
    #Payeee
    #billing_lr_number=serializers.CharField(source='Billing_Lr_Number',max_length=15)
    consignment_description=serializers.CharField(source='Description',max_length=50)
    payment_by=serializers.CharField(source='Payment_Client',max_length=15)
    
    
    
    def create(self,validated_data):
        validated_data['Billing_Id']="SR101"
        Lr_number=self.context.get('Lr_Number')
        consignor_gst=self.context.get('consignor_gst')
        print (Lr_number)
        object_lr=Bookings.objects.get(Lr_Number=Lr_number)
        #validated_data.pop('Billing_Lr_Number')
        validated_data['Billing_Lr_Number']=object_lr
        
        if validated_data['Payment_Client'] == "CONSIGNEE":
            payment_client_id=Clientinfo.objects.get(Client_GST=self.context.get('consginee_gst'))
            print ("CONSIGNOR")
        else:
            payment_client_id=Clientinfo.objects.get(Client_GST=self.context.get('consginor_gst'))
            print ("CONSIGNOR")
            
            
        validated_data.pop('Payment_Client')
        #payment_client_id="BEERAEE225"
        validated_data['Payment_Client']=payment_client_id
        payment_rate_info=Rate.objects.get(Client_id=payment_client_id)
        
        
        charge_by=payment_rate_info.Charge_By
        bookings=Bookings.objects.get(Lr_Number=Lr_number)
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
            
        
            
        validated_data['Sub_Total']=validated_data['Freight']+validated_data['Hamali_Charge']+validated_data['Pickup_Charge']+validated_data['Delivery_Charge']
            
        validated_data['Gst_Amt']=validated_data['Sub_Total']*.05
        validated_data['Total']=validated_data['Sub_Total']+validated_data['Gst_Amt']
        validated_data['Billing_Id']="SR101"
        print ("DONE")
        
        
        instance = Billing.objects.create(**validated_data)
        print(instance)
        return instance
        
    
    #Article_count
    
    #consignment_weight
    #pickup_type
    #Delivery_type
    
    
    
    
    
    
        
        
        
       # Create 2 serializer one is for paid to pay and other is for monthly
       