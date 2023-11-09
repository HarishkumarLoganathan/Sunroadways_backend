from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json
from .serializers import LoginSerializer

from .models import Clientinfo




@csrf_exempt
def Client_Signin(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        serializer = LoginSerializer(data=json.loads(request.body))
        print (json.loads(request.body))
        

        

        Client_GST=data.get('company_gst')
        Client_Email=data.get('email')

        
        
        existing_gst = Clientinfo.objects.filter(Client_GST=Client_GST).first()
        if existing_gst:
        # User with the provided email already exists
            return JsonResponse({'error': f"User with GST '{Client_GST}' Already registered with '{existing_gst.Client_Email}'...! Please try login with valid email"}, status=400)
        existing_email = Clientinfo.objects.filter(Client_GST=Client_GST).first()
        if existing_email:
        # User with the provided email already exists
            return JsonResponse({'error': f"Email'{existing_email.Client_Email}'Already registered...! Please try login with some other email"}, status=400)

        


        
        if serializer.is_valid():
            
            serializer.save()

        
        else:
            print (serializer.errors)
        
        return HttpResponse(json.dumps({"Message":"Login Successful"}))
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Clientinfo
from django.contrib.auth.hashers import check_password


User = get_user_model()

@api_view(['POST'])
def client_Login(request):
    print ("DEBUG")
    auth_header = request.headers.get('Authorization')
    data = json.loads(request.body)

    Client_Email=data.get('login_email')
    Client_Password=data.get('login_password')
    response = HttpResponse()

 
    print (Client_Email)
    print (Client_Password)

    try:
        client = Clientinfo.objects.get(Client_Email=Client_Email)
       # print (type(client))
       # print (dir(client))
    except ObjectDoesNotExist:
        return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

   
    if check_password(Client_Password, client.Client_Password):
        try:
            
            
            
            refresh = RefreshToken.for_user(client)
            #print (refresh)

        # Authentication successful
        # Return access token and refresh token
        
            
            
            #response.set_cookie('access_token', str(refresh.access_token), httponly=False,samesite='Lax', max_age=max_age)
           # response.set_cookie('refresh_token', str(refresh), httponly=True)
            request.session['access_token'] = str(refresh.access_token)
            request.session['refresh_token'] = str(refresh)
            print ("UPDATION SESSION STORAGE")
            print (request.session.get('access_token'))
            print (request.session.get('refresh_token'))
            


            return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'Client_id':client.id,
            'Client_name':client.Client_Name,
        }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Create a new user in the default user model if not already exists
            return Response({'message': 'Invalid password'})



    else:
        # Authentication failed
        return Response({'message': 'Invalid email or dubakoor'}, status=status.HTTP_401_UNAUTHORIZED)
