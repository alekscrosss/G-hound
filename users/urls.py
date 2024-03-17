
from django.contrib import admin
from django.urls import path, include 
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from .views import RegisterViews

app_name = "users"

urlpatterns = [
    path('signup/', RegisterViews.as_view(), name="register"), 
    path('login/', LoginView.as_view(template_name='users/login.html', authentication_form=LoginForm,
                                      redirect_authenticated_user=True), name='login'),    
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout')    
]
