import cv2
from mtcnn import MTCNN
import os

name = input("Enter student name: ")

path = os.path.join("dataset", name)
os.makedirs(path, exist_ok=True)

detector = MTCNN()
cap = cv2.VideoCapture(0)

count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb)

    for face in faces:
        x, y, w, h = face['box']
        face_img = frame[y:y+h, x:x+w]
        cv2.imwrite(f"{path}/{count}.jpg", face_img)
        count += 1
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Dataset Collection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 30:
        break

cap.release()
cv2.destroyAllWindows()
