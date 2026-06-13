import cv2
import os
import csv
import numpy as np
from datetime import datetime
from mtcnn import MTCNN
import mediapipe as mp
import math

# ================= PATH SETUP =================
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")
ATTENDANCE_DIR = os.path.join(PROJECT_DIR, "attendance")
ATTENDANCE_FILE = os.path.join(ATTENDANCE_DIR, "attendance.csv")

# ================= ATTENDANCE =================
def mark_attendance(name):
    os.makedirs(ATTENDANCE_DIR, exist_ok=True)

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            csv.writer(f).writerow(["Name", "Date", "Time"])

    with open(ATTENDANCE_FILE, "r") as f:
        for row in csv.reader(f):
            if len(row) > 1 and row[0] == name and row[1] == date:
                return True

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        csv.writer(f).writerow([name, date, time])

    print(f"Attendance marked for {name}")
    return True

# ================= BLINK SETUP =================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def dist(p1, p2):
    return math.dist(p1, p2)

def ear(eye):
    return (dist(eye[1],eye[5])+dist(eye[2],eye[4]))/(2*dist(eye[0],eye[3]))

EAR_THRESHOLD = 0.20
blink = False
done = False

# ================= FACE RECOGNITION =================
detector = MTCNN()
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces, labels, label_map = [], [], {}
lid = 0

for person in os.listdir(DATASET_DIR):
    p = os.path.join(DATASET_DIR, person)
    if not os.path.isdir(p): continue
    label_map[lid] = person
    for img in os.listdir(p):
        im = cv2.imread(os.path.join(p, img))
        if im is None: continue
        rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        d = detector.detect_faces(rgb)
        if not d: continue
        x,y,w,h = d[0]["box"]
        gray = cv2.resize(cv2.cvtColor(im[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY),(200,200))
        faces.append(gray)
        labels.append(lid)
    lid += 1

recognizer.train(faces, np.array(labels))

# ================= UI HELPERS =================
def glass_bar(frame, text, color):
    h, w, _ = frame.shape
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h-70), (w, h), (0,0,0), -1)
    cv2.addWeighted(overlay, 0.35, frame, 0.65, 0, frame)
    cv2.putText(frame, text, (30, h-25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

def draw_check(frame):
    h, w, _ = frame.shape
    cv2.circle(frame, (w//2, h//2), 60, (0,200,120), 3)
    cv2.line(frame, (w//2-25,h//2),
             (w//2-5,h//2+20),(0,200,120),4)
    cv2.line(frame, (w//2-5,h//2+20),
             (w//2+30,h//2-20),(0,200,120),4)

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    status = "Align face & blink to mark attendance"
    color = (255,255,255)

    # Blink detection
    res = face_mesh.process(rgb)
    if res.multi_face_landmarks:
        for lm in res.multi_face_landmarks:
            h,w,_ = frame.shape
            le = [(int(lm.landmark[i].x*w),int(lm.landmark[i].y*h)) for i in LEFT_EYE]
            re = [(int(lm.landmark[i].x*w),int(lm.landmark[i].y*h)) for i in RIGHT_EYE]
            if (ear(le)+ear(re))/2 < EAR_THRESHOLD:
                blink = True
                status = "Blink detected"

    # Face recognition
    for fd in detector.detect_faces(rgb):
        x,y,w,h = fd["box"]
        gray = cv2.resize(cv2.cvtColor(frame[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY),(200,200))
        label, conf = recognizer.predict(gray)

        if conf < 80:
            name = label_map[label]
            status = f"Recognized: {name}"

            if blink and not done:
                done = mark_attendance(name)
                status = "Attendance marked successfully"
                color = (0,200,120)

    glass_bar(frame, status, color)

    if done:
        draw_check(frame)
        cv2.imshow("Attendance System", frame)
        cv2.waitKey(1500)
        break

    cv2.imshow("Attendance System", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
