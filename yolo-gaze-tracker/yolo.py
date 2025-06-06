import cv2
from ultralytics import YOLO
import mediapipe as mp
import numpy as np

# 載入 YOLOv8 人臉模型 (需先下載 yolov8n-face.pt)
model = YOLO('C:/Users/user/PycharmProjects/PythonProject1/yolov8n-face.pt')

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 左右眼關鍵點
RIGHT_EYE_INDICES = [33, 133, 159]
LEFT_EYE_INDICES = [362, 263, 386]

def get_eye_points(landmarks, image_w, image_h, indices):
    return [(int(landmarks[i].x * image_w), int(landmarks[i].y * image_h)) for i in indices]

def estimate_avg_gaze_direction(left_eye, right_eye):
    def eye_ratio(eye):
        left_corner, right_corner, pupil = eye
        width = np.linalg.norm(np.array(left_corner) - np.array(right_corner))
        pos = np.linalg.norm(np.array(left_corner) - np.array(pupil))
        return pos / width if width != 0 else 0.5

    left_ratio = eye_ratio(left_eye)
    right_ratio = eye_ratio(right_eye)
    avg_ratio = (left_ratio + right_ratio) / 2

    if avg_ratio < 0.38:
        return 'Looking right'
    elif avg_ratio > 0.62:
        return 'Looking left'
    else:
        return 'Looking center'

def draw_gaze_arrow(frame, center, direction):
    if direction == 'Looking right':
        end = (center[0] + 60, center[1])
    elif direction == 'Looking left':
        end = (center[0] - 60, center[1])
    else:
        end = center
    cv2.arrowedLine(frame, center, end, (0, 255, 255), 3, tipLength=0.5)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    face_box = None
    for box in results.boxes:
        if box.conf[0] > 0.5:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            face_box = (x1, y1, x2, y2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            break

    if face_box:
        x1, y1, x2, y2 = face_box
        face_roi = frame[y1:y2, x1:x2]
        rgb_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
        mesh_result = face_mesh.process(rgb_roi)

        if mesh_result.multi_face_landmarks:
            lm = mesh_result.multi_face_landmarks[0].landmark
            h, w = face_roi.shape[:2]
            left_eye = get_eye_points(lm, w, h, LEFT_EYE_INDICES)
            right_eye = get_eye_points(lm, w, h, RIGHT_EYE_INDICES)

            # 畫出六個關鍵點
            for pt in left_eye + right_eye:
                cv2.circle(frame, (pt[0] + x1, pt[1] + y1), 3, (0, 0, 255), -1)

            if len(left_eye) == 3 and len(right_eye) == 3:
                gaze_dir = estimate_avg_gaze_direction(left_eye, right_eye)

                # 箭頭起點為左右眼中心平均
                avg_eye_center = (
                    int((left_eye[0][0] + left_eye[1][0] + right_eye[0][0] + right_eye[1][0]) / 4 + x1),
                    int((left_eye[0][1] + left_eye[1][1] + right_eye[0][1] + right_eye[1][1]) / 4 + y1)
                )
                draw_gaze_arrow(frame, avg_eye_center, gaze_dir)
                cv2.putText(frame, gaze_dir, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("YOLOv8 + MediaPipe Gaze (Average)", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
