# face recognition
import cv2
import face_recognition
import os

match_found = False

#------------------------------- 얼굴 비교 함수 정의 ----------------------------------
def compare_with_dataset(captured_image_path, dataset_path="./dataset"):
    global match_found
    # 캡처 이미지 로드 및 얼굴 인코딩
    unknown_image = face_recognition.load_image_file(captured_image_path)
    face_locations = face_recognition.face_locations(unknown_image, model="cnn") 
    unknown_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    if len(unknown_encodings) == 0:
        print("❗ 캡처된 이미지에서 얼굴을 찾지 못했습니다.")
        return

    unknown_encoding = unknown_encodings[0]

    # 데이터셋 폴더 내 이미지와 비교
    for filename in os.listdir(dataset_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(dataset_path, filename)
            known_image = face_recognition.load_image_file(path)
            known_encodings = face_recognition.face_encodings(known_image)

            if not known_encodings:
                print(f"❗ 데이터셋 얼굴 인식 실패: {filename}")
                continue

            known_encoding = known_encodings[0]
            result = face_recognition.compare_faces([known_encoding], unknown_encoding, tolerance=0.4)
            distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]

            if (result[0]) & (match_found == False):
                print(f"✅ [일치] 캡처: {captured_image_path} ↔ 데이터셋: {filename} (거리: {distance:.4f})")
                match_found = True
                name = os.path.splitext(filename)[0]
                print(f"{name} 님 시험을 시작하겠습니다.")
                break
            else:
                print(f"❌ [불일치] {filename} (거리: {distance:.4f})")

    if not match_found:
        print("👤 일치하는 사람을 찾지 못했습니다.")
        print("👤 다시 시도해주세요.")

# ------------------------------- 실시간 웹캠 캡처 시작 ----------------------------
cap = cv2.VideoCapture(2)  # 필요시 1 또는 2로 변경

# 해상도 및 비디오 저장 설정
w, h = 640, 480
fps = 30
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (w, h))

i = 1  # 캡처 이미지 인덱스

print("🎥 웹캠 시작! 'c'를 눌러 캡처, 'q'를 눌러 종료")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("❌ 프레임을 가져올 수 없습니다.")
        break

    out.write(frame)
    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        print("🛑 종료합니다.")
        break
    elif (key & 0xFF == ord('c')) & (match_found == False):
        filename = f"whoareyou{i}.png"
        cv2.imwrite(filename, frame)
        print(f"\n📸 {filename} 저장 완료. 얼굴 비교 시작...")
        compare_with_dataset(filename)
        print("-" * 60)
        i += 1

cap.release()
out.release()
cv2.destroyAllWindows()
```

* dataset 구축
```python
# dataset 구축
import numpy as np
import cv2
import os

# 카메라 장치 번호 2번을 통해 영상 캡처 객체 생성
cap = cv2.VideoCapture(2)  # 숫자 2: 연결된 카메라 중 3번째 장치 (0부터 시작)

# 영상 프레임의 너비와 높이 설정
w = 640
h = 480

# FPS 설정 (초당 프레임 수)
fps = 30
i = 1

# dataset을 저장할 위치
save_dir = "~/dataset"

# 새로운 data가 기존의 data를 덮어쓰기하는것을 방지하기 위한 코드
while True:
    filename = f"person{i}.png"
    filepath = os.path.join(save_dir, filename)
    if not os.path.exists(filepath):
        break
    i += 1

# 비디오 코덱 설정 ('mp4v'는 mp4 확장자용 MPEG-4 코덱)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# VideoWriter 객체 생성 (파일명, 코덱, FPS, 프레임 크기)
out = cv2.VideoWriter('output.mp4', fourcc, fps, (w, h))

# 캡처할 프레임 크기를 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

# 영상 캡처 장치가 열려 있는 동안 계속 실행
while cap.isOpened():
    # 프레임을 하나씩 읽어옴
    ret, frame = cap.read()

    # 프레임을 못 읽었을 경우 종료
    if ret is False:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # 읽은 프레임을 비디오 파일로 저장
    out.write(frame)

    # 현재 프레임을 화면에 출력
    cv2.imshow("Camera", frame)

    # 1ms 대기 후 키 입력 체크, 'q' 키가 눌리면 루프 종료
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    if key & 0xFF == ord('c'):
        filename = f"person{i}.png"
        filepath = os.path.join(save_dir, filename)
        cv2.imwrite(filepath, frame)
        print(f"{i} captured → 저장 경로: {filepath}")
        print(f"{filename} 업로드 완료!")
        i += 1

# 자원 해제: 카메라와 파일 저장 객체 닫기
cap.release()

out.release()
cv2.destroyAllWindows()
