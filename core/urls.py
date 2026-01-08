# File: core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Dấu '' nghĩa là trang chủ của app này
]