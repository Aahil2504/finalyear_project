import cv2
import os
import sys
from mtcnn import MTCNN

# -------- GET NAME FROM FLASK ----------
if len(sys.argv) < 2:
    print("Name not provided")
    sys.exit()

name = sys.argv[1].strip().replace(" ", "_")

# -------- PATH SETUP ----------
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset", name)

os.makedirs(DATASET_DIR, exist_ok=True)

# -------- CAMERA + FACE DETECTOR ----------
cap = cv2.VideoCapture(0)
detector = MTCNN()

count = 0
MAX_IMAGES = 20

print("Camera started for:", name)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb)

    for face in faces:
        x, y, w, h = face["box"]
        face_img = frame[y:y+h, x:x+w]

        if count < MAX_IMAGES:
            img_path = os.path.join(DATASET_DIR, f"{count}.jpg")
            cv2.imwrite(img_path, face_img)
            count += 1

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, f"Images: {count}/{MAX_IMAGES}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Register Face - Press Q to Exit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if count >= MAX_IMAGES:
        break

cap.release()
cv2.destroyAllWindows()
print("Registration completed for", name)
