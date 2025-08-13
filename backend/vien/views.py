//dhamo changed
//main branch changed
from django.shortcuts import render
from .serializers import *
from rest_framework import viewsets
from .models import *
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import random, json
from django.core.cache import cache
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from twilio.rest import Client
from django.conf import settings
import os, requests

OTP_STORE = {}

class EmpViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = EmpSerializer
    parser_classes = [MultiPartParser, FormParser]  # ✅ Required for FormData

    def create(self, request, *args, **kwargs):
        print("==== Incoming Data ====")
        for key in request.data:
            print(f"{key}: {request.data[key]}")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("==== Serializer Errors ====")
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        # You can add custom filtering logic here if needed
        return super().get_queryset()

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if not email:
            return JsonResponse({'error': 'Email required'}, status=400)
        otp = str(random.randint(100000, 999999))
        cache.set(f'otp_{email}', otp, timeout=300)  # 5 minutes
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            'pandiushak@gmail.com',
            [email],
            fail_silently=False,
        )
        return JsonResponse({'message': 'OTP sent'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        print("Incoming verify-otp request")
        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')
        print(f"Email: {email}, OTP: {otp}")
        cached_otp = cache.get(f'otp_{email}')
        print(f"Cached OTP: {cached_otp}")
        if cached_otp == otp:
            return JsonResponse({'verified': True})
        return JsonResponse({'verified': False, 'error': 'Invalid OTP'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

#Login Page
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('user_type')  # 'candidate' or 'client'

        if user_type == 'candidate':
            user = Candidate.objects.filter(gmail=email, password=password).first()
            request.session['user_type'] = 'candidate'  # Store user type in session
            request.session['user_id'] = user.id if user else None
            print(f"Candidate login: {user}")
        elif user_type == 'client':
            user = CompanyDetails.objects.filter(company_email=email, password=password).first()
            request.session['user_type'] = 'client'
            request.session['user_id'] = user.id if user else None
            print(f"Client login: {request.session['user_id']}")
        else:
            return JsonResponse({'success': False, 'message': 'Invalid user type'})

        if user:
            return JsonResponse({'success': True, 'message': f'{user_type.capitalize()} login successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials'})

    return JsonResponse({'success': False, 'message': 'Only POST allowed'})


@csrf_exempt
def send_numotp(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)
    phone = data.get('phone')

    if not phone:
        return JsonResponse({'error': 'Phone number is required'}, status=400)

    api_key = settings.TWOFACTOR_API_KEY
    url = f"https://2factor.in/API/V1/{api_key}/SMS/+91{phone}/AUTOGEN"

    try:
        response = requests.get(url)
        result = response.json()
        if result.get('Status') == 'Success':
            return JsonResponse({'message': 'OTP sent', 'session_id': result['Details']})
        else:
            return JsonResponse({'error': result.get('Details', 'Failed to send OTP')}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt    
def verify_numotp(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)
    session_id = data.get('session_id')
    otp = data.get('otp')

    print("Incoming verify-phone-otp:", session_id, otp)

    if not session_id or not otp:
        return JsonResponse({'error': 'OTP and Session ID are required'}, status=400)

    api_key = settings.TWOFACTOR_API_KEY
    url = f"https://2factor.in/API/V1/{api_key}/SMS/VERIFY/{session_id}/{otp}"

    try:
        response = requests.get(url)
        result = response.json()

        # 🔍 Log the exact API response from 2Factor
        print("2Factor API Response:", result)

        if result.get('Status') == 'Success':
            return JsonResponse({'verified': True, 'message': 'OTP verified'})
        else:
            # Show why OTP was invalid
            return JsonResponse({'verified': False, 'error': result.get('Details', 'Invalid OTP')}, status=400)
    except Exception as e:
        print("Exception during OTP verification:", e)
        return JsonResponse({'verified': False, 'error': str(e)}, status=500)

@csrf_exempt
def send_reset_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        usertype = data.get('userType') 

        if usertype == 'candidate':
            if not Candidate.objects.filter(gmail=email).exists():
                return JsonResponse({'error': 'Email not found'}, status=404)
            
        elif usertype == 'client':
            if not CompanyDetails.objects.filter(company_email=email).exists():
                return JsonResponse({'error': 'Email not found'}, status=404)

        otp = str(random.randint(100000, 999999))
        cache.set(f'reset_otp_{email}', otp, timeout=300)  # 5 mins

        send_mail(
            'Password Reset OTP',
            f'Your password reset OTP is {otp}',
            'pandiushak@gmail.com',
            [email],
            fail_silently=False,
        )
        return JsonResponse({'message': 'OTP sent to email'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def verify_reset_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')

        cached_otp = cache.get(f'reset_otp_{email}')
        if cached_otp == otp:
            return JsonResponse({'verified': True})
        return JsonResponse({'verified': False, 'error': 'Invalid OTP'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        new_password = data.get('new_password')
        user_type = data.get('userType')

        if user_type == 'candidate':
            user = Candidate.objects.filter(gmail=email).first()

        elif user_type == 'client':
            user = CompanyDetails.objects.filter(company_email=email).first()
            
        if user:
            user.password = new_password
            user.save()
            return JsonResponse({'message': 'Password reset successful'})
        return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

#Company ViewSet
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = CompanyDetails.objects.all()
    serializer_class = CompanySerializer

class OpeningViewSet(viewsets.ModelViewSet):
    queryset = Openings.objects.all()
    serializer_class = OpeningSerializer

    def create(self, request, *args, **kwargs):
        print("==== Incoming Opening Data ====")
        for key in request.data:
            print(f"{key}: {request.data[key]}")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("==== Serializer Errors ====")
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
