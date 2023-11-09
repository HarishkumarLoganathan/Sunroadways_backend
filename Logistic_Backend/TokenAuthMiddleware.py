from django.http import JsonResponse,HttpRequest
from django.conf import settings
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timezone
from CustomerLogin.models import Clientinfo


class TokenValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        access_token_flag="V"
        
        secret_key='aae728574f535cc7e01f1'
        print (settings.MIDDLEWARE_EXCLUDE_PATHS)
        print (request.path)
        if request.path in settings.MIDDLEWARE_EXCLUDE_PATHS:
            return self.get_response(request)
        print(request.body)
        print("Session Data:", request.session.items())
        auth_header = request.headers.get('Authorization')
        access_token= auth_header
        
        request.session['name']='harish'
        
        print (request.session.get('name'))
        
        print ("ACCESS TOKEN")
        print (request.session.get("access_token"))
       # token_bytes = request.session.get("access_token").encode('utf-8')
       # print (token_bytes)
        result =self.validate_and_compare_tokens(access_token, request.session.get("access_token"), secret_key)

        if (not result) :
            
            if (access_token_flag=="I"):
            
                return JsonResponse({'error': 'INVALID ACCESS TOKEN'}, status=401)
        else:
            response = self.get_response(request)
            print ("VALID")
            return response
            
        
        if not self.requires_refresh_authentication(request,secret_key):
            print ("ACCESS TOKEN IS INVALID")
            
            if  self.is_refresh_valid_token(request,secret_key):
                print ("GENERATING NEW TOKEN")
                response = self.get_response(request)
                
                response['new_access']= request.session.get('access_token')
                response.status_code = 299
                return response
                
                return response(status=299, headers={'access_token': request.session.get('access_token')})
                
                 
            else: 
                return JsonResponse({'error': 'REFRESH TOKEN EXPIRED'}, status=401)

        response = self.get_response(request)
        print ("SMOOTH RESPONSE")
        
        return response
    


    def requires_refresh_authentication(self, request,secret_key):
        auth_header = request.headers.get('Authorization')
        access_token= auth_header
        
        try:
            decoded_token=jwt.decode(access_token,secret_key,algorithms=['HS256'])
        except:
            print ("I came to except")
            return False
        expiration_timestamp = decoded_token.get('exp', 0)
        expiration_datetime = datetime.fromtimestamp(expiration_timestamp, timezone.utc)
        current_datetime = datetime.now(timezone.utc)

        
        if(current_datetime > expiration_datetime):

            
            return True
        else:
            print ("ACCESS EXPIRED")
            return False

    def is_refresh_valid_token(self, request,secret_key):
        refresh_token=request.session.get('refresh_token')
        try:
            refresh_decoded_token=jwt.decode(refresh_token,secret_key,algorithms=['HS256'])
        except:
            print ("TIME WASTE")
            return False
        
        refresh_expiration_timestamp = refresh_decoded_token.get('exp', 0)
        refresh_expiration_datetime = datetime.fromtimestamp(refresh_expiration_timestamp, timezone.utc)
        refresh_current_datetime = datetime.now(timezone.utc)
        
        if(refresh_current_datetime < refresh_expiration_datetime):
            id=refresh_decoded_token.get('id')
            print (id)
            customer = Clientinfo.objects.get(id=id)
            print (customer)
          #if request.path.startswith('/user_login_path/'):       
                
            
            
        else:
            print ("TIME WASTE")
            return False
        refresh = RefreshToken.for_user(customer)
        request.session['access_token'] = str(refresh.access_token)
        request.session['refresh_token'] = str(refresh)
               # response.set_cookie('access_token', str(refresh.access_token), httponly=True)
               # response.set_cookie('refresh_token', str(refresh), httponly=True)
        print ("REFRESH TOKEN IS STILL VALID")
        return True
        # Handle the case when the customer does not exist
            

    # Generate a new refresh token for the customer
            

            
            
           
            
            
        
        
    def validate_and_compare_tokens(self,token1, token2, secret_key):
        print ("IM IN")
    # Validate tokens and get their payload
        try:
            print (token1)
            print (token2)
            payload1 = jwt.decode(token1, secret_key, algorithms=['HS256'])
            payload2 = jwt.decode(token2, secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            access_token_flag="E"
            return False  # Token has expired or is invalid
        

    # Compare relevant claims or data from the payload
        if payload1.get('id') == payload2.get('id'):
            print ("LOOKS GOOD")
            print (payload1.get('sub'))
            return True  # Tokens represent the same user or entity
        access_token_flag="I"
        return False 