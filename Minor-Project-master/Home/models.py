from django.db import models

<<<<<<< HEAD
class Organization(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Ensure to store encrypted passwords
    address = models.CharField(max_length=255, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)  # To track if the organization has verified their OTP

    def __str__(self):
        return self.name

    # Additional methods, such as to verify OTP, can be added here
=======
# Create your models here.
class Signup(models.Model):
    Organization_Name = models.CharField(max_length=100)
    email=models.EmailField()
    # widgets = {
    #         'password': models.PasswordInput()
    #     }
    phone=models.BigIntegerField()
    
>>>>>>> origin/master
