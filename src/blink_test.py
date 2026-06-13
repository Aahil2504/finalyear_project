import cv2
import mediapipe as mp
import math

# Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Eye landmark indexes
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def distance(p1, p2):
    return math.dist(p1, p2)

def eye_aspect_ratio(eye):
    v1 = distance(eye[1], eye[5])
    v2 = distance(eye[2], eye[4])
    h = distance(eye[0], eye[3])
    return (v1 + v2) / (2.0 * h)

EAR_THRESHOLD = 0.20
blink_detected = False

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        for landmarks in result.multi_face_landmarks:
            h, w, _ = frame.shape

            left_eye = [(int(landmarks.landmark[i].x * w),
                         int(landmarks.landmark[i].y * h)) for i in LEFT_EYE]
            right_eye = [(int(landmarks.landmark[i].x * w),
                          int(landmarks.landmark[i].y * h)) for i in RIGHT_EYE]

            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)
            avg_ear = (left_ear + right_ear) / 2

            if avg_ear < EAR_THRESHOLD:
                blink_detected = True

    if blink_detected:
        cv2.putText(frame, "BLINK DETECTED", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Blink Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
