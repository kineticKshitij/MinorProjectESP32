from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    # Organization views
    organization_signup, 
    organization_login,  # Optional if switching to JWT completely
    organization_dashboard,
    
    # Employee views
    employee_signup, 
    employee_login,   # Optional if switching to JWT completely
    employee_dashboard,
    add_employee, 
    manage_employees, 
    remove_employee,
    
    # Query views
    submit_query, 
    get_public_queries,
    index,
    # submit_contact  # Removed because the view doesn't exist
    receive_rfid,
)

# Define API URL patterns for better organization
organization_patterns = [
    path('signup/', organization_signup, name='organization_signup'),
    path('login/', organization_login, name='organization_login'),
    path('dashboard/', organization_dashboard, name='organization_dashboard'),
]

employee_patterns = [
    path('signup/', employee_signup, name='employee_signup'),
    path('login/', employee_login, name='employee_login'),
    path('dashboard/', employee_dashboard, name='employee_dashboard'),
    path('add-employee/<str:org_name>/', add_employee, name='add_employee'),
    path('manage/', manage_employees, name='manage_employees'),
    path('remove/<int:employee_id>/', remove_employee, name='remove_employee'),
]

query_patterns = [
    path('submit/', submit_query, name='submit_query'),
    path('public/', get_public_queries, name='get_public_queries'),
]

urlpatterns = [
    # JWT endpoints for token obtain and refresh
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path("api/rfid/", receive_rfid, name="receive_rfid"),

    # Organization APIs
    path('api/org/', include(organization_patterns)),
    # Employee APIs
    path('api/emp/', include(employee_patterns)),
    # Query APIs
    path('api/query/', include(query_patterns)),
    
    # Root index view
    path('', index, name="index"),
    # Uncomment the next line if the submit_contact view is added later
    # path('api/contact/', submit_contact, name='submit_contact'),
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
