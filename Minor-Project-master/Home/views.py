import logging
import traceback
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.images import get_image_dimensions
from django.utils import timezone
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes,
    throttle_classes
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from django.views.decorators.cache import never_cache
from rest_framework_simplejwt.tokens import RefreshToken
from Home.models import Organization, EmployeeSignup, Query, RFIDCard
from Home.serializers import OrganizationSerializer, EmployeeSerializer, ContactQuerySerializer

logger = logging.getLogger(__name__)
# RFID 
@api_view(['POST'])
@permission_classes([AllowAny])
def receive_rfid(request):
    """
    API to receive RFID card UID and store it in the database.
    """
    card_uid = request.data.get("card_uid")
    print("Card ID=>",card_uid)
    if not card_uid:
        return Response({"error": "Card UID is required"}, status=400)

    # Save or update card details
    card, created = RFIDCard.objects.get_or_create(card_uid=card_uid)

    return Response({
        "message": "Card details saved successfully",
        "card_uid": card_uid
    })

# Render index page
def index(request):
    return render(request, "index.html")

# ---------------------------
# Utility Functions
# ---------------------------
def validate_image(image_file):
    if not image_file:
        return None
    if image_file.size > 5 * 1024 * 1024:
        return "Image size must be under 5MB"
    width, height = get_image_dimensions(image_file)
    if width > 2000 or height > 2000:
        return "Image dimensions must be 2000x2000 pixels or smaller"
    allowed_types = ['image/jpeg', 'image/png', 'image/gif']
    if image_file.content_type not in allowed_types:
        return "Image must be JPEG, PNG, or GIF format"
    return None

def validate_credentials(data):
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return "Email and password are required"
    return None

# ---------------------------
# Organization Endpoints
# ---------------------------

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@throttle_classes([UserRateThrottle])
def organization_signup(request):
    try:
        data = request.data
        print("From Frontend=>", data)
        if not all([data.get('name'), data.get('email'), data.get('password')]):
            return Response({'error': 'Name, email, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        cred_error = validate_credentials(data)
        if cred_error:
            return Response({'error': cred_error}, status=status.HTTP_400_BAD_REQUEST)

        if Organization.objects.filter(email=data.get('email')).exists():
            return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

        logo = request.FILES.get('logo')
        if logo:
            logo_error = validate_image(logo)
            if logo_error:
                return Response({'error': logo_error}, status=status.HTTP_400_BAD_REQUEST)

        organization = Organization.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            password=make_password(data.get('password')),
            logo=logo
        )

        return Response({
            'message': 'Organization registered successfully',
            'organization': OrganizationSerializer(organization).data
        }, status=status.HTTP_201_CREATED)
    except Exception:
        logger.error(f"Organization signup error: {traceback.format_exc()}")
        return Response({'error': 'Registration failed. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------------------
# JWT Organization Login
# ---------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def organization_login(request):
    """
    Authenticate an organization using email and password,
    and return JWT tokens on success.
    """
    try:
        data = request.data
        if not data.get('email') or not data.get('password'):
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        org = authenticate(request, email=data.get('email'), password=data.get('password'))
        if org is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(org)
        return Response({
            'message': 'Login successful',
            'organization': {
                'id': org.id,
                'name': org.name,
                'email': org.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)

    except Exception:
        logger.error(f"Organization login error: {traceback.format_exc()}")
        return Response({'error': 'Login failed. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------------------
# Organization Dashboard (JWT Protected)
# ---------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@never_cache
def organization_dashboard(request):
    print("Function initialize")
    try:
        logger.debug("User: %s", request.user)
        org = request.user
        employee_count = EmployeeSignup.objects.filter(organization=org).count()
        query_count = Query.objects.filter(owner=org).count()

        logo_url = request.build_absolute_uri(org.logo.url) if org.logo else None

        return Response({
            'message': f'Welcome to {org.name} Organization Dashboard',
            'stats': {
                'total_employees': employee_count,
                'total_queries': query_count,
            },
            'organization': {
                'id': org.id,
                'name': org.name,
                'email': org.email,
                'logo': logo_url,
            }
        }, status=status.HTTP_200_OK)

    except Exception:
        logger.error(f"Organization dashboard error: {traceback.format_exc()}")
        return Response({'error': 'Failed to load dashboard'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------------------------
# (Optional) JWT Logout - Typically handled client-side by deleting tokens
# ---------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def organization_logout(request):
    """
    In a JWT-based system, logout is usually handled on the client side
    by simply deleting the stored tokens. You can also implement token
    blacklisting if needed.
    """
    return Response({'message': 'Logout successful (client-side token deletion required)'}, status=status.HTTP_200_OK)


# ---------------------------
# Employee Endpoints (Modified similarly for JWT login)
# ---------------------------

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def employee_signup(request):
    try:
        data = request.data
        if not all([data.get('name'), data.get('email'), data.get('org_name'), data.get('password')]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if EmployeeSignup.objects.filter(email=data.get('email')).exists():
            return Response({'error': 'Employee already exists'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            organization = Organization.objects.get(name=data.get('org_name'))
        except Organization.DoesNotExist:
            return Response({'error': 'Organization not found'}, status=status.HTTP_400_BAD_REQUEST)

        photo = request.FILES.get('photo')
        if photo:
            photo_error = validate_image(photo)
            if photo_error:
                return Response({'error': photo_error}, status=status.HTTP_400_BAD_REQUEST)

        employee = EmployeeSignup.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            password=make_password(data.get('password')),
            organization=organization,
            photo=photo
        )
        
        return Response({
            'message': 'Employee registered successfully',
            'employee': EmployeeSerializer(employee).data
        }, status=status.HTTP_201_CREATED)
    except Exception:
        logger.error(f"Employee signup error: {traceback.format_exc()}")
        return Response({'error': 'Registration failed. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def employee_login(request):
    """
    Authenticate an employee and return JWT tokens.
    """
    try:
        data = request.data
        # print("From Frontend =>", data)
        
        if not data.get('email') or not data.get('password'):
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate employee using the email and password.
        employee = authenticate(request, email=data.get('email'), password=data.get('password'))
        if employee is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(employee)
        
        return Response({
            'message': 'Login successful',
            'employee': EmployeeSerializer(employee).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)
    
    except Exception:
        logger.error(f"Employee login error: {traceback.format_exc()}")
        return Response({'error': 'Login failed. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_dashboard(request):
    try:
        user = request.user

        # Determine if the authenticated user is an EmployeeSignup or an Organization.
        if hasattr(user, 'organization'):
            # If user is an EmployeeSignup, then 'organization' is available and user has date_joined.
            org = user.organization
            employee_data = {
                'name': user.name,
                'email': user.email,
                'photo': request.build_absolute_uri(user.photo.url) if user.photo else None,
                'date_joined': user.date_joined,
            }
        else:
            # Otherwise, user is an Organization. We assume that the Organization object is acting as the user.
            org = user
            employee_data = {
                'name': user.name,
                'email': user.email,
                'photo': None,  # Organization doesn't have a date_joined or photo by design
                'date_joined': None,
            }

        total_queries = Query.objects.filter(owner=org).count()
        org_logo_url = request.build_absolute_uri(org.logo.url) if org.logo else None

        return Response({
            'message': f'Welcome {user.email} to Employee Dashboard',
            'employee': employee_data,
            'organization': {
                'name': org.name,
                'logo': org_logo_url,
            },
            'stats': {
                'total_queries': total_queries,
            }
        }, status=status.HTTP_200_OK)
        
    except Exception:
        logger.error(f"Employee dashboard error: {traceback.format_exc()}")
        return Response({'error': 'Failed to load dashboard. Please try again.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def add_employee(request, org_name):
    try:
        data = request.data
        if not all([data.get('name'), data.get('email'), data.get('password')]):
            return Response({'error': 'Name, Email, and Password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            organization = Organization.objects.get(name=org_name)
        except ObjectDoesNotExist:
            return Response({'error': 'Organization not found!'}, status=status.HTTP_404_NOT_FOUND)
        
        photo = request.FILES.get('photo')
        if not photo:
            return Response({'error': 'Photo is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if EmployeeSignup.objects.filter(email=data.get('email')).exists():
            return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)
        
        employee = EmployeeSignup.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            password=make_password(data.get('password')),
            organization=organization,
            photo=photo
        )
        
        return Response({
            'message': 'Employee added successfully!',
            'employee': EmployeeSerializer(employee).data
        }, status=status.HTTP_201_CREATED)
    except Exception:
        logger.error(f"Error adding employee: {traceback.format_exc()}")
        return Response({'error': 'Failed to add employee. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_employee(request, employee_id):
    try:
        try:
            employee = EmployeeSignup.objects.get(id=employee_id, organization=request.user)
        except EmployeeSignup.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        
        employee.delete()
        return Response({'message': 'Employee removed successfully'}, status=status.HTTP_200_OK)
    except Exception:
        logger.error(f"Remove employee error: {traceback.format_exc()}")
        return Response({'error': 'Failed to remove employee. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_public_queries(request):
    try:
        page = int(request.GET.get('page', 1))
        page_size = min(int(request.GET.get('page_size', 10)), 50)
        start = (page - 1) * page_size
        end = start + page_size
        
        queries = Query.objects.filter(visibility='public').order_by('-created_at')[start:end]
        total_queries = Query.objects.filter(visibility='public').count()
        
        return Response({
            'queries': ContactQuerySerializer(queries, many=True).data,
            'total': total_queries,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_queries + page_size - 1) // page_size
        }, status=status.HTTP_200_OK)
    except Exception:
        logger.error(f"Get public queries error: {traceback.format_exc()}")
        return Response({'error': 'Failed to fetch queries. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manage_employees(request):
    """
    Fetch a paginated list of employees belonging to the authenticated organization.
    This endpoint works with JWT since request.user is set when a valid JWT is provided.
    """
    try:
        # Get pagination parameters
        page = int(request.GET.get('page', 1))
        page_size = min(int(request.GET.get('page_size', 10)), 50)
        start = (page - 1) * page_size
        end = start + page_size

        # Filter employees that belong to the organization (request.user)
        employees_qs = EmployeeSignup.objects.filter(organization=request.user).order_by('name')
        total_employees = employees_qs.count()
        employees = employees_qs[start:end]

        # Serialize the data
        serialized_employees = EmployeeSerializer(employees, many=True).data

        return Response({
            'employees': serialized_employees,
            'total': total_employees,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_employees + page_size - 1) // page_size
        }, status=status.HTTP_200_OK)
    except Exception:
        logger.error(f"Manage employees error: {traceback.format_exc()}")
        return Response({'error': 'Failed to fetch employees. Please try again.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_query(request):
    """
    Allow an authenticated organization to submit a query.
    """
    try:
        data = request.data
        query_content = data.get('query')
        if not query_content:
            return Response({'error': 'Query content is required'}, status=status.HTTP_400_BAD_REQUEST)
        if len(query_content) > 5000:
            return Response({'error': 'Query content must be under 5000 characters'}, status=status.HTTP_400_BAD_REQUEST)
        
        query = Query.objects.create(
            query=query_content,
            visibility=data.get('visibility', 'private'),
            owner=request.user
        )
        
        return Response({
            'message': 'Query submitted successfully',
            'query': ContactQuerySerializer(query).data
        }, status=status.HTTP_201_CREATED)
    except Exception:
        logger.error(f"Query submission error: {traceback.format_exc()}")
        return Response({'error': 'Query submission failed. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
