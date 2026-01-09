from rest_framework import serializers
from .models import AttendanceLog

class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.name')
    class _Meta:
        model = AttendanceLog
        fields = ['id', 'employee_name', 'timestamp', 'status']