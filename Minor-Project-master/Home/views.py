from django.shortcuts import render
<<<<<<< HEAD
from Home.models import Organization
=======
from Home.models import Signup
>>>>>>> origin/master
from django.core.mail import send_mail
from django.http import JsonResponse
import random
from django.contrib.auth.hashers import make_password
<<<<<<< HEAD
import smtplib
=======
>>>>>>> origin/master

# Render the index page
def index(request):
    return render(request, 'index.html')

# Render the dashboard
def operation(request):
    return render(request, 'dashboard.html')

# Render the login page
def login(request):
    return render(request, 'login.html')

<<<<<<< HEAD
def resend_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Add your logic to resend the OTP here
        return JsonResponse({'status': 'success', 'message': 'OTP resent successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        # Add logic to verify the OTP (e.g., compare it with the generated OTP)
        session_otp = request.session.get('otp')
        if otp and str(otp) == str(session_otp):
            return JsonResponse({'status': 'success', 'message': 'OTP verified successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Incorrect OTP. Please try again.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def organization_signup(request):
    if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            captcha_answer = request.POST.get('captcha_answer')
            expected_answer = request.session.get('captcha')

            if int(captcha_answer) == expected_answer:
                # Generate OTP and send it via email
                otp = random.randint(100000, 999999)
                print(f"OTP generated: {otp}")  # For debugging purposes; remove in production
                request.session['otp'] = otp

                try:
                    # Use Django's send_mail function
                    print("")
                    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                        connection.starttls()
                        connection.login(user='minorproject347d@gmail.com', password='yanzzyizaomyuswn')
                        connection.sendmail(from_addr='minorproject347d@gmail.com', to_addrs=email,
                        msg=f"Subject:OTP Verification!\n\n your otp is {otp}")
                    # subject='OTP Verification',
                        # message=f'Your OTP code is {otp}.',
                        # from_email='minorproject347d@gmail.com',  # Change to your verified sender email
                        # recipient_list=[email],
                        # fail_silently=False,
                    

                    # Save the organization data (without OTP, because OTP should not be stored in the database)
                    organization = Organization(
                        name=name,
                        email=email,
                        password=make_password(password)
                    )
                    organization.save()

                    return JsonResponse({'status': 'success', 'message': 'OTP has been sent to your email.'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': f'Error sending OTP: {str(e)}'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid CAPTCHA. Please try again.'})

    # Generate CAPTCHA numbers for the form
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    request.session['captcha'] = num1 + num2
=======
# Handle organization signup with CAPTCHA and OTP
def organization_signup(request):
    if request.method == 'POST':
        # Handle CAPTCHA and OTP generation
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        captcha_answer = request.POST.get('captcha_answer', None)  # Get the CAPTCHA answer
        expected_answer = request.session.get('captcha')  # Get expected CAPTCHA answer from session

        if captcha_answer is None or captcha_answer.strip() == "":
            return JsonResponse({'status': 'error', 'message': 'CAPTCHA is missing'})
        
        if expected_answer is None:
            return JsonResponse({'status': 'error', 'message': 'CAPTCHA validation error'})
        
        try:
            if int(captcha_answer) == expected_answer:
                # CAPTCHA is valid; generate OTP
                otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
                request.session['otp'] = otp  # Store the OTP in the session
                
                # Print the OTP to the terminal
                print(f"Generated OTP: {otp}")  # This will print the OTP in the terminal
                
                try:
                    # Send OTP to the provided email
                    send_mail(
                        'Your OTP Code',
                        f'Your OTP code is {otp}. Please enter it in the application.',
                        'MinorProject347d@yahoo.com',  # Replace with your email
                        [email],
                        fail_silently=False,
                    )
                    return JsonResponse({'status': 'success', 'message': 'OTP has been sent to your email.'})
                except Exception as e:  
                     print(f"Error sending email: {str(e)}")  # Log the error to the console
                     return JsonResponse({'status': 'error', 'message': f'Error sending email: {str(e)}'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid CAPTCHA input'})

    # Display the signup form with CAPTCHA
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    request.session['captcha'] = num1 + num2  # Store expected answer in session
>>>>>>> origin/master

    context = {
        'num1': num1,
        'num2': num2,
    }
<<<<<<< HEAD
    return render(request, 'organization_signup.html', context)
=======
    return render(request, 'organization_signup.html', context)
>>>>>>> origin/master
