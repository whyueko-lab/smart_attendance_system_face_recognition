import cv2
import face_recognition
import requests
import time  # Ditambahkan untuk logika cooldown

# 1. Load Data Wajah (Contoh: Wajah Kamu)
# Pastikan kamu punya foto 'admin.jpg' di folder yang sama
image_of_user = face_recognition.load_image_file("admin.jpg")
user_encoding = face_recognition.face_encodings(image_of_user)[0]

known_face_encodings = [user_encoding]
known_face_names = ["ADM-001"] # ID Karyawan sesuai Database Django

# Variabel untuk kontrol cooldown agar tidak spam API
last_request_time = 0 
cooldown_seconds = 10 # Kirim data maksimal setiap 10 detik sekali

# 2. Akses Kamera Laptop
video_capture = cv2.VideoCapture(0)

print("Sistem Scan Wajah Berjalan... Tekan 'q' untuk berhenti.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Kecilkan ukuran frame untuk mempercepat deteksi (0.25x)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Cari wajah di frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            # --- LOGIKA KIRIM DATA KE DJANGO ---
            current_time = time.time() # Ambil waktu sekarang
            
            # Cek apakah sudah melewati masa cooldown (10 detik)
            if current_time - last_request_time > cooldown_seconds:
                try:
                    url = "http://127.0.0.1:8000/attendance/mark/"
                    payload = {"employee_id": name}
                    response = requests.post(url, json=payload, timeout=2)
                    
                    if response.status_code == 200:
                        print(f"Berhasil Absen: {name} - Status: {response.json().get('message')}")
                        last_request_time = current_time # Update waktu kirim terakhir
                    else:
                        print(f"Server merespon: {response.status_code}")
                        
                except Exception as e:
                    print("Gagal lapor ke server (Cek apakah Django sudah running?):", e)

        # Tambahan Visual: Gambar kotak di wajah (opsional tapi bagus untuk demo UAS)
        top *= 4
        right *= 4 
        bottom *= 4 
        left *= 4 # Kembalikan ke ukuran asli
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    # Tampilkan Preview Kamera
    cv2.imshow('Smart Attendance Scanner', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()