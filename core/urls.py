# File: core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # Dấu '' nghĩa là trang chủ của app này
    path('upload/', views.upload_file, name='upload_file'),
    path('lists/', views.list_files, name='list_files'),
    path('signup/', views.signup, name='signup'),
    path('report/', views.report_dashboard, name='report_dashboard'),
]