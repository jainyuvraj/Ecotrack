from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserTable
import os
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import WasteReport, Feedback
import json
# Create your views here.
from .utils import generate_otp, verify_otp
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.decorators import user_passes_test

from django.http import HttpResponse, HttpResponseBadRequest





from .models import WasteReport
import base64
import re
from io import BytesIO
from PIL import Image
@csrf_exempt
def submit_report(request):
    if request.method == "POST":
        description = request.POST.get("description")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        image_data = request.POST.get("image")

        if not description or len(description) < 10:
            return JsonResponse({"error": "Description must be at least 10 characters"}, status=400)

        if not latitude or not longitude:
            return JsonResponse({"error": "Location is required"}, status=400)

        if image_data:
            image_data = re.sub('^data:image/.+;base64,', '', image_data)
            image_data = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_data))
            image_name = "waste_report_image.png"
            image_io = BytesIO()
            image.save(image_io, format='PNG')
            image_file = ContentFile(image_io.getvalue(), name=image_name)
        else:
            image_file = None

        waste_report = WasteReport(
            description=description,
            latitude=latitude,
            longitude=longitude,
            image=image_file,
            user = request.user,
        )
        waste_report.save()

        return JsonResponse({"message": "Report submitted successfully!"}, status=200)

    return render(request, "report_form.html")




def index(request):
    return render(request,'index1.html')


@login_required
def report_form(request):
    if request.method == 'POST' and request.FILES.get('image'):
        pass

    return render(request,'report_form.html')




@login_required
def logindex(request):
    return render(request,'logindex.html')


def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff)
def staff_dashboard(request):
    if request.user.is_authenticated:
        all_report = WasteReport.objects.all()
    return render(request,'Staff_Dashboard.html',{'reports':all_report})


def user_dashboard(request):
    if request.user.is_authenticated:
        user_reports = WasteReport.objects.filter(user=request.user)

        return render(request,'user-dashboard.html',{'reports':user_reports})
    else :
        return redirect('login/login_page.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff:
            
                return redirect('staff_dashboard')
            
            return redirect('/logindex')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login/login_page.html', {'error_message': error_message})
    return render(request,'login/login_page.html')


def sign_up(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        
        if password == repeatPassword:
            try:
                user = User.objects.create_user(name, email, password)
                new_user = UserTable(Name=name, Email=email)
                
                
                user.save()
                new_user.save()
                login(request,user)
                return redirect('/logindex')


                
            except:
                error_message = 'Error creating account'
                return render(request, 'login/sign_in.html', {'error_message': error_message})
        else:
            error_message = 'Password do not match'
            return render(request, 'login/sign_in.html', {'error_message': error_message})
    return render(request,'login/sign_in.html')

def feedback(request):
    
        
    return render(request,'feedback.html')


@csrf_exempt  # Only for development! Remove in production and handle CSRF properly
def submit_feedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            feedback = Feedback.objects.create(
                user = request.user,
                name=data['name'],
                email=data['email'],
                rating=data['rating'],
                feedback=data['feedback']
            )
            feedback.save()
            return JsonResponse({'status': 'success', 'message': 'Feedback submitted successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def user_logout(request):
    logout(request)
    return redirect('/')

def chatbot(request):
    return render(request,'chatbot.html')


