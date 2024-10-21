from django.shortcuts import render
from Home.models import Organization
from django.core.mail import send_mail
from django.http import JsonResponse
import random
from django.contrib.auth.hashers import make_password
import smtplib

# Render the index page
def index(request):
    return render(request, 'index.html')

# Render the dashboard
def operation(request):
    return render(request, 'dashboard.html')

# Render the login page
def login(request):
    return render(request, 'login.html')

# Handle organization signup with CAPTCHA and OTP
from .models import Organization
from django.contrib.auth.hashers import make_password  # For encrypting passwords

def organization_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        captcha_answer = request.POST.get('captcha_answer', None)
        expected_answer = request.session.get('captcha')

        if captcha_answer is None or captcha_answer.strip() == "":
            return JsonResponse({'status': 'error', 'message': 'CAPTCHA is missing'})
        
        if expected_answer is None:
            return JsonResponse({'status': 'error', 'message': 'CAPTCHA validation error'})

        try:
            if int(captcha_answer) == expected_answer:
                # CAPTCHA is valid; generate OTP
                otp = random.randint(100000, 999999)
                request.session['otp'] = otp

                print(f"Generated OTP: {otp}")

                try:
                    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                        connection.starttls()
                        connection.login(user="minorproject347d@gmail.com", password="yanzzyizaomyuswn")
                        connection.sendmail(from_addr="minorproject347d@gmail.com", to_addrs=email,
                                msg=f'''Subject: OTP Verification \n\nYour OTP code is {otp}. Please enter it in the application.''')

                    # Create the organization instance and save it
                    organization = Organization(
                        name=name,
                        email=email,
                        password=make_password(password),  # Encrypt the password
                        otp=otp,
                    )
                    organization.save()

                    return JsonResponse({'status': 'success', 'message': 'OTP has been sent to your email.'})
                except Exception as e:
                    print(f"Error sending email: {str(e)}")
                    return JsonResponse({'status': 'error', 'message': f'Error sending email: {str(e)}'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid CAPTCHA input'})

    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    request.session['captcha'] = num1 + num2

    context = {
        'num1': num1,
        'num2': num2,
    }
    return render(request, 'organization_signup.html', context)
