from django.db import models
from django.utils import timezone

class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    # Tambahkan blank=True dan null=True
    face_encoding = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AttendanceLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[('IN', 'Masuk'), ('OUT', 'Keluar')])

    def __str__(self):
        return f"{self.employee.name} - {self.status} at {self.timestamp}"