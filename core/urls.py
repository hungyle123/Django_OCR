# File: core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'), # Dấu '' nghĩa là trang chủ của app này
    path('lists/', views.list_files, name='list_files'),
]