#new file

from django.contrib import admin
from django.urls import path, include
from . import views
from .apps import AppGhoundConfig

app_name = "app_ghound"

urlpatterns = [
    path('', views.main, name='root'),
    path('app_ghound/', views.main, name='app_ghound'),   
    path("users/", include("users.urls"))
]