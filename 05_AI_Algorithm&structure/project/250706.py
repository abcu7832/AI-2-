import cv2
import mediapipe as mp
import numpy as np
import face_recognition
import time
import os

# 눈 EAR 계산 함수
def calculate_ear(landmarks, eye_indices):
    left = np.array([landmarks[eye_indices[0]].x, landmarks[eye_indices[0]].y])
    right = np.array([landmarks[eye_indices[3]].x, landmarks[eye_indices[3]].y])
    top = (np.array([landmarks[eye_indices[1]].x, landmarks[eye_indices[1]].y]) +
           np.array([landmarks[eye_indices[2]].x, landmarks[eye_indices[2]].y])) / 2
    bottom = (np.array([landmarks[eye_indices[4]].x, landmarks[eye_indices[4]].y]) +
              np.array([landmarks[eye_indices[5]].x, landmarks[eye_indices[5]].y])) / 2
    horizontal = np.linalg.norm(left - right)
    vertical = np.linalg.norm(top - bottom)
    return vertical / horizontal

# 눈 랜드마크 인덱스 (Mediapipe 기준)
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

mp_face_mesh = mp.solutions.face_mesh

# 얼굴 인식 및 비교 함수
def authenticate_face(img_path, dataset_path="./dataset"):
    known_encodings = []
    known_names = []

    for filename in os.listdir(dataset_path):
        if filename.endswith(('.jpg', '.png')):
            image = face_recognition.load_image_file(os.path.join(dataset_path, filename))
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])

    unknown_image = face_recognition.load_image_file(img_path)
    unknown_encodings = face_recognition.face_encodings(unknown_image)

    if unknown_encodings:
        results = face_recognition.compare_faces(known_encodings, unknown_encodings[0], tolerance=0.4)
        distances = face_recognition.face_distance(known_encodings, unknown_encodings[0])

        if True in results:
            idx = results.index(True)
            print(f"✅ 신원 확인 성공: {known_names[idx]} (거리: {distances[idx]:.4f})")
        else:
            print("❌ 신원 확인 실패: 등록된 인물이 아닙니다.")
    else:
        print("❗ 얼굴 인식 실패: 이미지에 얼굴이 감지되지 않았습니다.")

# 눈 깜빡임 감지 및 신원 확인
def detect_blink_and_authenticate(dataset_path="./dataset"):
    cap = cv2.VideoCapture(2)  # 카메라 인덱스 조정 필요 시 변경
    blink_count = 0
    blink_flag = False
    start_time = time.time()
    DURATION = 6  # 초
    BLINK_THRESHOLD = 0.21
    BLINK_REQUIRED = 2

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

        prev_ear = 0
        frame_to_save = None

        print("📸 눈 깜빡임 감지 시작 (q 키로 종료)")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    landmarks = face_landmarks.landmark
                    left_ear = calculate_ear(landmarks, LEFT_EYE)
                    right_ear = calculate_ear(landmarks, RIGHT_EYE)
                    ear = (left_ear + right_ear) / 2.0

                    # 디버깅 EAR 출력
                    cv2.putText(frame, f"EAR: {ear:.3f}", (30, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                    if ear < BLINK_THRESHOLD and not blink_flag:
                        blink_count += 1
                        blink_flag = True
                        print(f"👁 눈 깜빡임 감지! 총 {blink_count}회")

                    if ear >= BLINK_THRESHOLD:
                        blink_flag = False

                    frame_to_save = frame.copy()

            cv2.imshow('Blink Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if time.time() - start_time > DURATION:
                break

        cap.release()
        cv2.destroyAllWindows()

        if blink_count >= BLINK_REQUIRED and frame_to_save is not None:
            print("✅ 실제 사람으로 판별됨. 신원 확인 시작...")
            img_path = "capture.jpg"
            cv2.imwrite(img_path, frame_to_save)
            authenticate_face(img_path, dataset_path)
        else:
            print("❌ 사진으로 판별됨 (눈 깜빡임 감지되지 않음).")

# 실행
if __name__ == "__main__":
    detect_blink_and_authenticate(dataset_path="./dataset")
