import uuid
from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)

# ✅ Generate a unique 12-character ID
def generate_uuid():
    return uuid.uuid4().hex[:12]

# ✅ Organization Manager
class OrganizationManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        org = self.model(name=name, email=email)
        if password:
            org.set_password(password)  # Secure password hashing using set_password
        org.save(using=self._db)
        return org

    def create_superuser(self, name, email, password):
        org = self.create_user(name, email, password)
        org.is_superuser = True
        org.is_staff = True
        org.save(using=self._db)
        return org

# ✅ Organization Model
class Organization(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=255)  # Stored as a hashed password
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="organization_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="organization_permissions", blank=True)

    objects = OrganizationManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def set_password(self, raw_password):
        self.password = make_password(raw_password)  # Use Django's make_password
       
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name

# Custom Manager for EmployeeSignup
class EmployeeSignupManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        """
        Creates and saves an EmployeeSignup with the given email, name, and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        if password:
            user.set_password(password)  # Use set_password to ensure one-time hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, **extra_fields):
        """
        Creates and saves a superuser for EmployeeSignup.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, password, **extra_fields)

# ✅ EmployeeSignup Model
class EmployeeSignup(AbstractBaseUser, PermissionsMixin):
    unique_id = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
        default=generate_uuid  # Ensures unique ID
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    date_joined = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    photo = models.ImageField(upload_to='employees_photos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="employee_signup_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="employee_signup_permissions", blank=True)

    # Use the custom manager
    objects = EmployeeSignupManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

# ✅ Query Model
class Query(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    query = models.TextField()
    visibility = models.CharField(max_length=8, choices=VISIBILITY_CHOICES, default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='queries')
    
    def __str__(self):
        return self.query

class RFIDCard(models.Model):
    card_uid = models.CharField(max_length=50, unique=True)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card UID: {self.card_uid} - Scanned at {self.scanned_at}"