import face_recognition
import pickle
import cv2
import os

# Folder tempat menyimpan foto karyawan (nama file = nama orang)
image_path = 'dataset/'
known_encodings = []
known_names = []

for file in os.listdir(image_path):
    image = face_recognition.load_image_file(f"{image_path}/{file}")
    encoding = face_recognition.face_encodings(image)[0]
    
    known_encodings.append(encoding)
    known_names.append(os.path.splitext(file)[0])

# Simpan encoding ke file agar tidak perlu proses ulang tiap saat
data = {"encodings": known_encodings, "names": known_names}
with open("encodings.pickle", "wb") as f:
    f.write(pickle.dumps(data))

print("Proses encoding selesai!")