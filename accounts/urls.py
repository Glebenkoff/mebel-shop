from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('profile/', views.profile, name='profile'),
    path('test-email/', views.test_email, name='test_email'),
]