from .models import BlindManifestbooking
from CustomerLogin.models import Clientinfo
from BranchLogin.models import BranchLoginInfo
from rest_framework import serializers
from datetime import datetime
from BranchLogin.models import BranchLoginInfo
#clientinfo_clientid



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