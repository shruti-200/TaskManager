from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('user_details', views.user_details, name='user_details'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
]