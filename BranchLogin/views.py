from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist


from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json
from .models import BranchLoginInfo
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
def Branch_Signup(request):
        if request.method == 'POST':
        

 
        
            data = json.loads(request.body)
            Branch_Name=data.get('branch_name')
            Branch_Address = data.get('branch_address')
            Branch_City=data.get('branch_city')
            Branch_State=data.get('branch_state')
            Branch_Email=data.get('branch_email')
            Branch_Password=data.get('branch_password')
            id = data.get('branch_id')
            
            existing_branch = BranchLoginInfo.objects.filter(id=id).first()
            if existing_branch:
            # User with the provided email already exists
                return JsonResponse({'error': f"User with GST '{id}' Already registered with '{existing_branch.id}'...! Please try login with valid email"}, status=400)
            existing_email = BranchLoginInfo.objects.filter(Branch_Email=Branch_Email).first()
            if existing_email:
            # User with the provided email already exists
                return JsonResponse({'error': f"Email'{existing_email.Branch_Email}'Already registered...! Please try login with some other email"}, status=400)
            new_user = BranchLoginInfo(Branch_Name=Branch_Name,Branch_Address=Branch_Address,Branch_City=Branch_City,Branch_State=Branch_State,Branch_Email=Branch_Email,Branch_Password=Branch_Password,id=id)
            new_user.save()
            return HttpResponse(json.dumps({"Message":"Login Successful"}))
            
@csrf_exempt
@api_view(['POST'])
def Branch_Login(request):
    print ("DEBUG")
    auth_header = request.headers.get('Authorization')
    data = json.loads(request.body)
    print (data)
    Branch_Email=data.get('branch_email')
    print (Branch_Email)
    Branch_Password=data.get('branch_password')
    response = HttpResponse()

    print (Branch_Email)
    print (Branch_Password)

    try:
        
        branch = BranchLoginInfo.objects.get(Branch_Email=Branch_Email)
        print (branch)
        print (branch.Branch_Password)
        print (Branch_Password)

    except BranchLoginInfo.DoesNotExist as e:
        print(f"Error: {e}")
        return Response({'message': 'FUCKER'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if branch.Branch_Password == Branch_Password:
        print ("hi")
        try:
            
            
            print ("TOEKN")
            print (branch)
            refresh = RefreshToken.for_user(branch)

        
            print (refresh)
            
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
            'Branch_Id':branch.id,
            'Branch_Name':branch.Branch_Name,
        }, status=status.HTTP_200_OK)
        except:
            
            return Response({'message': 'Invalid password'})



    else:
   
        return Response({'message': 'Invalid email or dubakoor'}, status=status.HTTP_401_UNAUTHORIZED)


# Create your views here.
