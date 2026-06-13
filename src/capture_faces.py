import cv2
import os
from mtcnn import MTCNN

def capture_faces(student_name):
    detector = MTCNN()

    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dataset_dir = os.path.join(project_dir, "dataset")
    person_dir = os.path.join(dataset_dir, student_name)

    os.makedirs(person_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    print("📸 Capturing faces for:", student_name)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = detector.detect_faces(rgb)

        for face in faces:
            x, y, w, h = face['box']
            face_img = frame[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (200, 200))

            img_path = os.path.join(person_dir, f"{count}.jpg")
            cv2.imwrite(img_path, face_img)
            count += 1

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Register Face - Press Q to quit", frame)

        if count >= 20:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    print("✅ Face registration completed")
