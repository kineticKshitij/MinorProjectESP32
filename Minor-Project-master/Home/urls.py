from django.urls import path
from Home import views

urlpatterns = [
    path('', views.index, name='home'),          # Home page
    # path('Operation', views.Operation, name='Operation'),  # Dashboard page
    path('Login', views.login, name='Login'),    # Login page
    # path('Signup', views.Signup, name='Signup'), # Signup page
    path('organization-signup/', views.organization_signup, name='organization_signup'),
]
