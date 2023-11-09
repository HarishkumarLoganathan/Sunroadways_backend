from rest_framework import serializers
from .models import Clientinfo
from django.contrib.auth.hashers import make_password


class LoginSerializer(serializers.Serializer):
    company_name = serializers.CharField(source='Client_Name', max_length=500)
    company_gst = serializers.CharField(source='Client_GST', max_length=500)
    email = serializers.EmailField(source='Client_Email', max_length=200)
    signin_password = serializers.CharField(source='Client_Password', max_length=500)
    signin_mobile = serializers.CharField(source='Client_Phone', max_length=20)
    company_pincode=serializers.CharField(source='Company_Pincode',max_length=20)
    company_city=serializers.CharField(source='Company_City',max_length=15)
    company_area=serializers.CharField(source='Company_Area',max_length=15)
    company_address=serializers.CharField(source='Company_Address',max_length=50)

    def create(self, validated_data):
        Client_Name=validated_data["Client_Name"]
        Client_GST=validated_data["Client_GST"]
        validated_data["id"]=Client_Name[:2]+Client_Name[-2:]+Client_GST[2:5]+Client_GST[-7:-4]
        hashed_password = make_password(validated_data['Client_Password'])
        print(hashed_password)
        validated_data.pop("Client_Password")
        validated_data['Client_Password']=hashed_password
        Clientinfo_instance=Clientinfo.objects.create(**validated_data)
        
        return Clientinfo_instance


class LoginCheckSerializer(serializers.Serializer):
    company_name = serializers.CharField(source='Client_Name', max_length=500)
    company_gst = serializers.CharField(source='Client_GST', max_length=500)
    email = serializers.EmailField(source='Client_Email', max_length=200)
    signin_password = serializers.CharField(source='Client_Password', max_length=500)
    signin_mobile = serializers.CharField(source='Client_Phone', max_length=20)