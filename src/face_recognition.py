import cv2
import os
import csv
import numpy as np
from datetime import datetime
from mtcnn import MTCNN

# ================= PROJECT ROOT =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")
ATTENDANCE_DIR = os.path.join(PROJECT_DIR, "attendance")
ATTENDANCE_FILE = os.path.join(ATTENDANCE_DIR, "attendance.csv")

print("Project:", PROJECT_DIR)
print("Dataset:", DATASET_DIR)

# ================= ATTENDANCE =================
def mark_attendance(name):
    if not os.path.exists(ATTENDANCE_DIR):
        os.makedirs(ATTENDANCE_DIR)

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            csv.writer(f).writerow(["Name", "Date", "Time"])

    with open(ATTENDANCE_FILE, "r") as f:
        for line in f:
            if name in line and date in line:
                return

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        csv.writer(f).writerow([name, date, time])

    print(f"Attendance marked for {name}")

# ================= FACE RECOGNITION =================
detector = MTCNN()
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces, labels = [], []
label_map = {}
label_id = 0

print("Loading dataset...")

for person in os.listdir(DATASET_DIR):
    person_path = os.path.join(DATASET_DIR, person)
    if not os.path.isdir(person_path):
        continue

    label_map[label_id] = person

    for img_name in os.listdir(person_path):
        img = cv2.imread(os.path.join(person_path, img_name))
        if img is None:
            continue

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detected = detector.detect_faces(rgb)
        if not detected:
            continue

        x, y, w, h = detected[0]["box"]
        face = cv2.cvtColor(img[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
        face = cv2.resize(face, (200, 200))

        faces.append(face)
        labels.append(label_id)

    label_id += 1

recognizer.train(faces, np.array(labels))
print("Training completed")

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    detected = detector.detect_faces(rgb)

    for face_data in detected:
        x, y, w, h = face_data["box"]
        gray = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (200, 200))

        label, confidence = recognizer.predict(gray)

        name = "Unknown"
        if confidence < 80:
            name = label_map[label]
            mark_attendance(name)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        cv2.putText(frame, name, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    cv2.imshow("Face Recognition Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
