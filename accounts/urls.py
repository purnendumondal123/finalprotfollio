from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('otp/', views.otp_verify, name='otp'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]