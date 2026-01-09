from django.urls import path
from . import views

urlpatterns = [
    # Jalur ini yang dicari oleh main_scanner.py (attendance/mark/)
    path('mark/', views.mark_attendance, name='mark_attendance'),
    
    # Jalur ini yang dicari oleh React (attendance/api/logs/)
    path('api/logs/', views.get_attendance_logs, name='get_logs'),
]