from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from .models import AttendanceLog, Employee
from django.views.decorators.csrf import csrf_exempt
import json

# 1. FUNGSI UNTUK DASHBOARD REACT (Ini yang tadi hilang)
def get_attendance_logs(request):
    # Mengambil 10 log terbaru
    logs = AttendanceLog.objects.all().order_by('-timestamp')[:10]
    data = [
        {
            "id": log.id,
            "employee_name": log.employee.name,
            "timestamp": log.timestamp,
            "status": log.status
        } for log in logs
    ]
    return JsonResponse(data, safe=False)

# 2. FUNGSI UNTUK SCANNER KAMERA (Milik kamu yang sudah bagus)
@csrf_exempt
def mark_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            emp_id = data.get('employee_id')
            
            employee = Employee.objects.get(employee_id=emp_id)
            now = timezone.now()
            
            # Cari absen terakhir karyawan hari ini
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            last_log = AttendanceLog.objects.filter(
                employee=employee, 
                timestamp__gte=today_start
            ).order_by('-timestamp').first()

            # Logika Cooldown
            if last_log and (now - last_log.timestamp) < timedelta(seconds=5):
                return JsonResponse({
                    'status': 'ignored', 
                    'message': 'Sabar, tunggu 5 menit untuk absen lagi'
                })

            # Tentukan Status (Toggle IN/OUT)
            if not last_log or last_log.status == 'OUT':
                new_status = 'IN'
            else:
                new_status = 'OUT'

            # Simpan Log Baru
            AttendanceLog.objects.create(employee=employee, status=new_status)
            
            return JsonResponse({
                'status': 'success', 
                'message': f'{employee.name} berhasil {new_status}'
            })

        except Employee.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User tidak dikenal'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)