import cv2
import mediapipe as mp
import numpy as np
import time
from datetime import datetime
import json
import sys
from gtts import gTTS
import os
import face_recognition
import threading
import argparse
from pathlib import Path

class AIExamSupervisorIntegrated:
    def __init__(self, config_path="config.json"):
        """통합 AI 시험 감독관 초기화"""
       
        # 설정 로드
        self.load_config(config_path)
       
        # MediaPipe 초기화 (라즈베리파이 최적화)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            refine_landmarks=False,  # 라즈베리파이 최적화
            static_image_mode=False,
            max_num_faces=2,  # 메모리 절약
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
       
        # 얼굴 랜드마크 포인트 정의
        self.NOSE_TIP = 1
        self.LEFT_EYE_LEFT = 33
        self.RIGHT_EYE_RIGHT = 263
        self.LEFT_MOUTH = 61
        self.RIGHT_MOUTH = 291
        self.CHIN = 18
       
        # 눈 영역 포인트 (아이트래킹용)
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 387, 385, 263, 373, 380]
       
        # 시스템 상태
        self.system_phase = "IDENTITY_CHECK"  # IDENTITY_CHECK -> EXAM_MONITORING
        self.authenticated_user = None
        self.exam_start_time = None
        self.exam_terminated = False
        self.termination_reason = ""
       
        # 위반 상태 초기화
        self.reset_violation_states()
       
        # 경고 시스템 초기화
        self.MAX_WARNINGS = 5  # 최대 경고 횟수 (통합)
        self.total_warnings = 0  # 총 경고 횟수 (고개 방향 + 시선 이탈)
        self.head_warnings = 0  # 고개 방향 경고 횟수 (표시용)
        self.gaze_warnings = 0  # 시선 이탈 경고 횟수 (표시용)
       
        # 얼굴 추적 변수들
        self.last_face_landmarks = None
        self.face_lost_time = 0
       
        # 아이트래킹 변수들
        self.gaze_baseline = None
        self.frame_count = 0
        self.baseline_sum = 0
        self.last_gaze_violation_time = 0
       
        # 로깅 시스템
        self.violation_log = []
        self.total_violations = 0
        self.identity_attempts = 0
       
        # 터미널 출력 설정
        self.last_status_print = 0
       
        # ANSI 색상 코드
        self.setup_colors()
       
        # 데이터셋 경로 확인
        self.ensure_dataset_exists()
       
        print(f"{self.BOLD}{self.CYAN}🔒 AI 시험 감독관 시스템 v2.1 (라즈베리파이5 최적화){self.END}")
        print(f"{self.GREEN}✅ 시스템 초기화 완료{self.END}")
        print(f"{self.YELLOW}📋 부정행위 탐지 규칙:{self.END}")
        print(f"{self.RED}   • 다중 인원 탐지: 즉시 부정행위 판정 및 시험 중단{self.END}")
        print(f"{self.RED}   • 화면 이탈: 즉시 부정행위 판정 및 시험 중단{self.END}")
        print(f"{self.YELLOW}   • 고개 방향/시선 이탈: 통합 5회 경고 후 부정행위 판정 및 시험 중단{self.END}")
        print("=" * 70)
   
    def load_config(self, config_path):
        """설정 파일 로드"""
        default_config = {
            "camera": {
                "index": 0,
                "width": 640,
                "height": 480,
                "fps": 20,
                "mirror": True
            },
            "detection": {
                "x_threshold": 0.15,
                "y_threshold": 0.5,
                "sustained_time": 2.0,
                "gaze_margin": 0.5,
                "face_lost_threshold": 1.0
            },
            "identity": {
                "dataset_path": "./dataset",
                "tolerance": 0.5,
                "max_attempts": 5
            },
            "system": {
                "print_interval": 1.0,
                "baseline_frames": 30,
                "gaze_debug_mode": False,
                "save_video": True,
                "log_path": "./logs",
                "max_warnings": 5
            }
        }
       
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 기본값과 병합
                for key in default_config:
                    if key not in config:
                        config[key] = default_config[key]
                    else:
                        for subkey in default_config[key]:
                            if subkey not in config[key]:
                                config[key][subkey] = default_config[key][subkey]
            except Exception as e:
                print(f"설정 파일 로드 실패: {e}")
                config = default_config
        else:
            config = default_config
            # 기본 설정 파일 생성
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
       
        # 설정값 적용
        self.config = config
        self.CAMERA_INDEX = config["camera"]["index"]
        self.CAMERA_WIDTH = config["camera"]["width"]
        self.CAMERA_HEIGHT = config["camera"]["height"]
        self.CAMERA_FPS = config["camera"]["fps"]
        self.MIRROR_CAMERA = config["camera"]["mirror"]
       
        self.X_THRESHOLD = config["detection"]["x_threshold"]
        self.Y_THRESHOLD = config["detection"]["y_threshold"]
        self.SUSTAINED_TIME = config["detection"]["sustained_time"]
        self.GAZE_MARGIN = config["detection"]["gaze_margin"]
        self.FACE_LOST_THRESHOLD = config["detection"]["face_lost_threshold"]
       
        self.DATASET_PATH = config["identity"]["dataset_path"]
        self.FACE_TOLERANCE = config["identity"]["tolerance"]
        self.MAX_IDENTITY_ATTEMPTS = config["identity"]["max_attempts"]
       
        self.PRINT_INTERVAL = config["system"]["print_interval"]
        self.BASELINE_FRAMES = config["system"]["baseline_frames"]
        self.GAZE_DEBUG_MODE = config["system"]["gaze_debug_mode"]
        self.SAVE_VIDEO = config["system"]["save_video"]
        self.LOG_PATH = config["system"]["log_path"]
        self.MAX_WARNINGS = config["system"]["max_warnings"]
   
    def setup_colors(self):
        """ANSI 색상 코드 설정"""
        self.RED = '\033[91m'
        self.GREEN = '\033[92m'
        self.YELLOW = '\033[93m'
        self.BLUE = '\033[94m'
        self.MAGENTA = '\033[95m'
        self.CYAN = '\033[96m'
        self.WHITE = '\033[97m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'
        self.END = '\033[0m'
   
    def ensure_dataset_exists(self):
        """데이터셋 폴더 존재 확인 및 생성"""
        Path(self.DATASET_PATH).mkdir(exist_ok=True)
        Path(self.LOG_PATH).mkdir(exist_ok=True)
       
        # 데이터셋 파일 확인
        dataset_files = list(Path(self.DATASET_PATH).glob("*.jpg")) + \
                       list(Path(self.DATASET_PATH).glob("*.jpeg")) + \
                       list(Path(self.DATASET_PATH).glob("*.png"))
       
        if not dataset_files:
            print(f"{self.YELLOW}⚠️  데이터셋 폴더가 비어있습니다: {self.DATASET_PATH}{self.END}")
            print(f"{self.YELLOW}   인증용 얼굴 이미지를 '{self.DATASET_PATH}' 폴더에 추가하세요{self.END}")
   
    def reset_violation_states(self):
        """위반 상태 초기화"""
        self.is_head_abnormal = False
        self.head_abnormal_start_time = time.time()
        self.is_head_violation = False
       
        self.is_multiple_faces = False
        self.multiple_faces_start_time = time.time()
        self.is_multiple_faces_violation = False
       
        self.is_no_face = False
        self.no_face_start_time = time.time()
        self.is_no_face_violation = False
       
        self.is_gaze_abnormal = False
        self.gaze_abnormal_start_time = time.time()
        self.is_gaze_violation = False
   
    def terminate_exam(self, reason):
        """시험 중단"""
        self.exam_terminated = True
        self.termination_reason = reason
       
        print(f"\n{self.BOLD}{self.RED}🚨 부정행위 탐지! 시험 즉시 중단! 🚨{self.END}")
        print(f"{self.RED}╔══════════════════════════════════════════════════════════════╗{self.END}")
        print(f"{self.RED}║                      부정행위 탐지                          ║{self.END}")
        print(f"{self.RED}║                      시험 즉시 중단                         ║{self.END}")
        print(f"{self.RED}║                                                              ║{self.END}")
        print(f"{self.RED}║  사유: {reason:<50} ║{self.END}")
        print(f"{self.RED}║  시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<50} ║{self.END}")
        print(f"{self.RED}║                                                              ║{self.END}")
        print(f"{self.RED}║  심각한 부정행위가 탐지되어 시험이 즉시 중단되었습니다.      ║{self.END}")
        print(f"{self.RED}║  이 결과는 시험 관리자에게 보고됩니다.                      ║{self.END}")
        print(f"{self.RED}╚══════════════════════════════════════════════════════════════╝{self.END}")
        speak_tts("심각한 부정행위가 탐지되어 시험을 중단합니다.")
        # 로그 기록
        self.log_violation("부정행위-시험중단", reason)
   
    def issue_warning(self, warning_type, details):
        """경고 발급 (통합 5회 시스템)"""
        # 개별 경고 횟수 증가 (표시용)
        if warning_type == "고개 방향":
            self.head_warnings += 1
        elif warning_type == "시선 이탈":
            self.gaze_warnings += 1
       
        # 통합 경고 횟수 증가
        self.total_warnings += 1
        remaining = self.MAX_WARNINGS - self.total_warnings
        speak_tts(f"{warning_type}부정행위가 탐지되었습니다.")
        print(f"\n{self.BOLD}{self.YELLOW}⚠️  경고 {self.total_warnings}/{self.MAX_WARNINGS} - {warning_type}{self.END}")
        print(f"{self.YELLOW}상세: {details}{self.END}")
       
        if self.total_warnings >= self.MAX_WARNINGS:
            print(f"{self.RED}🚨 총 {self.MAX_WARNINGS}회 경고 누적! 부정행위로 판정됩니다.{self.END}")
            self.terminate_exam(f"경고 {self.MAX_WARNINGS}회 누적 (고개: {self.head_warnings}회, 시선: {self.gaze_warnings}회)")
            return True
        else:
            print(f"{self.YELLOW}남은 경고: {remaining}회 (고개: {self.head_warnings}회, 시선: {self.gaze_warnings}회){self.END}")
       
        # 로그 기록
        self.log_violation(f"경고-{warning_type}", details)
        return False
   
    def find_camera(self):
        """카메라 찾기 (라즈베리파이 최적화)"""
        # 설정된 카메라 인덱스부터 시도
        camera_indices = [self.CAMERA_INDEX] + [i for i in range(5) if i != self.CAMERA_INDEX]
       
        for camera_idx in camera_indices:
            try:
                cap = cv2.VideoCapture(camera_idx)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAMERA_WIDTH)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAMERA_HEIGHT)
                cap.set(cv2.CAP_PROP_FPS, self.CAMERA_FPS)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 버퍼 크기 최소화
               
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        print(f"{self.GREEN}✅ 카메라 {camera_idx}번 연결 성공 ({self.CAMERA_WIDTH}x{self.CAMERA_HEIGHT}@{self.CAMERA_FPS}fps){self.END}")
                        return cap
                    cap.release()
            except Exception as e:
                continue
        return None
   
    def compare_with_dataset(self, captured_image_path):
        """데이터셋과 얼굴 비교"""
        try:
            # 캡처 이미지 로드 및 얼굴 인코딩
            unknown_image = face_recognition.load_image_file(captured_image_path)
            face_locations = face_recognition.face_locations(unknown_image, model="hog")  # 라즈베리파이 최적화
            unknown_encodings = face_recognition.face_encodings(unknown_image, face_locations)

            if len(unknown_encodings) == 0:
                print(f"{self.RED}❗ 캡처된 이미지에서 얼굴을 찾지 못했습니다.{self.END}")
                return None

            unknown_encoding = unknown_encodings[0]

            # 데이터셋 폴더 내 이미지와 비교
            dataset_files = []
            for ext in ["*.jpg", "*.jpeg", "*.png"]:
                dataset_files.extend(Path(self.DATASET_PATH).glob(ext))
           
            if not dataset_files:
                print(f"{self.RED}❌ 데이터셋에 이미지가 없습니다.{self.END}")
                return None

            best_match = None
            best_distance = float('inf')
           
            for file_path in dataset_files:
                try:
                    known_image = face_recognition.load_image_file(str(file_path))
                    known_encodings = face_recognition.face_encodings(known_image)

                    if not known_encodings:
                        print(f"❗ 얼굴 인식 실패: {file_path.name}")
                        continue

                    known_encoding = known_encodings[0]
                    distance = face_recognition.face_distance([known_encoding], unknown_encoding)[0]
                   
                    print(f"   📊 {file_path.name}: 거리 {distance:.4f}")
                   
                    if distance < best_distance:
                        best_distance = distance
                        best_match = file_path.stem  # 확장자 제외한 파일명
                       
                except Exception as e:
                    print(f"❗ 파일 처리 오류 {file_path.name}: {e}")
                    continue

            # 매칭 결과 판단
            if best_match and best_distance <= self.FACE_TOLERANCE:
                print(f"{self.GREEN}✅ [매칭 성공] {best_match} (거리: {best_distance:.4f}){self.END}")
                return best_match
            else:
                print(f"{self.RED}❌ [매칭 실패] 최소 거리: {best_distance:.4f} (임계값: {self.FACE_TOLERANCE}){self.END}")
                return None
               
        except Exception as e:
            print(f"{self.RED}❌ 얼굴 인식 처리 오류: {e}{self.END}")
            return None
   
    def identity_verification_phase(self, cap):
        """신원 확인 단계"""
        print(f"\n{self.BOLD}{self.BLUE}🔍 1단계: 신원 확인{self.END}")
        print(f"{self.CYAN}카메라 화면에서 'c' 키를 눌러 얼굴을 캡처하세요{self.END}")
        speak_tts("신원 조회를 시작합니다. C키를 눌러 얼굴을 캡처하세요.")
        print(f"{self.CYAN}최대 {self.MAX_IDENTITY_ATTEMPTS}회 시도 가능, 'q' 키로 종료{self.END}")
        print("-" * 70)
       
        while self.identity_attempts < self.MAX_IDENTITY_ATTEMPTS:
            ret, frame = cap.read()
            if not ret:
                print(f"{self.RED}❌ 프레임을 가져올 수 없습니다.{self.END}")
                return False
           
            if self.MIRROR_CAMERA:
                frame = cv2.flip(frame, 1)
           
            # 상태 정보 표시
            cv2.putText(frame, f"Identity Verification ({self.identity_attempts + 1}/{self.MAX_IDENTITY_ATTEMPTS})",
                       (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame, "Press 'c' to capture, 'q' to quit",
                       (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
           
            # 얼굴 감지 표시
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(frame_rgb, model="hog")
           
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, "Face Detected", (left, top - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
           
            cv2.imshow("AI Exam Supervisor - Identity Check", frame)
           
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print(f"{self.YELLOW}신원 확인을 취소했습니다.{self.END}")
                return False
            elif key == ord('c'):
                self.identity_attempts += 1
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"identity_check_{timestamp}_{self.identity_attempts}.png"
                cv2.imwrite(filename, frame)
               
                print(f"\n📸 {self.identity_attempts}번째 시도: {filename} 저장 완료")
                print("🔍 얼굴 인식 처리 중...")
               
                # 얼굴 비교 수행
                matched_name = self.compare_with_dataset(filename)
               
                if matched_name:
                    self.authenticated_user = matched_name
                    print(f"{self.BOLD}{self.GREEN}🎉 인증 성공! {matched_name}님, 환영합니다.{self.END}")
                    speak_tts("신원 확인이 완료되었습니다. 시선 처리를 위해 카메라를 바라봐주세요.")
                    # 캡처 파일 정리
                    try:
                        os.remove(filename)
                    except:
                        pass
                   
                    return True
                else:
                    print(f"{self.RED}❌ 인증 실패 ({self.identity_attempts}/{self.MAX_IDENTITY_ATTEMPTS}){self.END}")
                    if self.identity_attempts < self.MAX_IDENTITY_ATTEMPTS:
                        print(f"{self.YELLOW}다시 시도하세요. 남은 횟수: {self.MAX_IDENTITY_ATTEMPTS - self.identity_attempts}회{self.END}")
                   
                    # 실패한 캡처 파일 정리
                    try:
                        os.remove(filename)
                    except:
                        pass
               
                print("-" * 70)
       
        print(f"{self.RED}❌ 신원 확인 실패: 최대 시도 횟수 초과{self.END}")
        return False
   
    def get_landmarks_coords(self, face_landmarks, image_w, image_h):
        """MediaPipe 랜드마크를 픽셀 좌표로 변환"""
        coords = []
        for landmark in face_landmarks.landmark:
            x = int(landmark.x * image_w)
            y = int(landmark.y * image_h)
            coords.append([x, y])
        return np.array(coords)
   
    def get_head_direction(self, landmarks, image_w, image_h):
        """머리 방향 판단"""
        nose_tip = landmarks[self.NOSE_TIP]
        left_eye_left = landmarks[self.LEFT_EYE_LEFT]
        right_eye_right = landmarks[self.RIGHT_EYE_RIGHT]
       
        # 얼굴 중심선 계산
        face_width = abs(right_eye_right[0] - left_eye_left[0])
        face_center_x = (left_eye_left[0] + right_eye_right[0]) / 2
       
        # 좌우 방향 판단
        offset_x = nose_tip[0] - face_center_x
       
        # 상하 방향 판단
        eye_center_y = (left_eye_left[1] + right_eye_right[1]) / 2
        offset_y = nose_tip[1] - eye_center_y
       
        if face_width == 0:
            return "Forward", 0, 0
       
        # 정규화
        x_ratio = offset_x / face_width
        y_ratio = offset_y / face_width
       
        # 방향 판단
        if y_ratio > self.Y_THRESHOLD:
            return "Down", x_ratio, y_ratio
        elif x_ratio > self.X_THRESHOLD:
            return "Left", x_ratio, y_ratio
        elif x_ratio < -self.X_THRESHOLD:
            return "Right", x_ratio, y_ratio
        else:
            return "Forward", x_ratio, y_ratio
   
    def get_gaze_ratio(self, eye_indices, landmarks, frame, gray):
        """시선 방향 계산"""
        h, w = frame.shape[:2]
       
        try:
            # 눈 영역 좌표 계산
            eye_region = np.array([(int(landmarks[i][0] * w), int(landmarks[i][1] * h))
                                  for i in eye_indices], np.int32)
           
            # 마스크 생성
            mask = np.zeros((h, w), dtype=np.uint8)
            cv2.fillPoly(mask, [eye_region], 255)
           
            # 눈 영역 추출
            eye = cv2.bitwise_and(gray, gray, mask=mask)
           
            # 경계 좌표 계산
            min_x = np.min(eye_region[:, 0])
            max_x = np.max(eye_region[:, 0])
            min_y = np.min(eye_region[:, 1])
            max_y = np.max(eye_region[:, 1])
           
            # 경계 검사
            if min_x >= max_x or min_y >= max_y or min_x < 0 or min_y < 0 or max_x >= w or max_y >= h:
                return 1.0
           
            # 눈 영역 크롭
            gray_eye = eye[min_y:max_y, min_x:max_x]
           
            if gray_eye.size == 0:
                return 1.0
           
            # 임계값 적용
            _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
           
            th_h, th_w = threshold_eye.shape
           
            if th_w < 2:
                return 1.0
           
            # 좌우 영역의 흰색 픽셀 수 계산
            left_white = cv2.countNonZero(threshold_eye[:, 0:int(th_w / 2)])
            right_white = cv2.countNonZero(threshold_eye[:, int(th_w / 2):])
           
            if left_white == 0 or right_white == 0:
                return 1.0
            else:
                return left_white / right_white
               
        except Exception as e:
            return 1.0
   
    def update_violation_states(self, face_count, head_direction, gaze_ratio):
        """위반 상태 업데이트 (개선된 로직)"""
        current_time = time.time()
       
        # 시험이 이미 중단된 경우 처리 중지
        if self.exam_terminated:
            return
       
        # 1. 다중 인물 감지 - 즉시 중단
        current_multiple_faces = face_count > 1
        if current_multiple_faces != self.is_multiple_faces:
            self.is_multiple_faces = current_multiple_faces
            self.multiple_faces_start_time = current_time
            self.is_multiple_faces_violation = False
       
        if self.is_multiple_faces:
            duration = current_time - self.multiple_faces_start_time
            if duration >= self.SUSTAINED_TIME and not self.is_multiple_faces_violation:
                self.is_multiple_faces_violation = True
                # 부정행위 알림 출력
                self.print_violation_alert("다중 인물 감지", f"감지된 얼굴 수: {face_count}명",
                                         is_start=True, duration=duration)
                # 시험 즉시 중단
                self.terminate_exam(f"다중 인물 감지 ({face_count}명)")
                return
            elif duration < self.SUSTAINED_TIME and duration > 0.5:
                self.print_warning("다중 인물 감지", f"{face_count}명 감지됨", duration)
       
        # 2. 화면 이탈 감지 - 즉시 중단
        current_no_face = face_count == 0
        if current_no_face != self.is_no_face:
            self.is_no_face = current_no_face
            self.no_face_start_time = current_time
            self.is_no_face_violation = False
       
        if self.is_no_face:
            duration = current_time - self.no_face_start_time
            if duration >= self.SUSTAINED_TIME and not self.is_no_face_violation:
                self.is_no_face_violation = True
                # 부정행위 알림 출력
                self.print_violation_alert("화면 이탈", "얼굴 감지 불가 - 화면에서 완전히 이탈",
                                         is_start=True, duration=duration)
                # 시험 즉시 중단
                self.terminate_exam("화면 이탈 (얼굴 감지 불가)")
                return
            elif duration < self.SUSTAINED_TIME and duration > 0.5:
                self.print_warning("화면 이탈", "얼굴이 감지되지 않음", duration)
       
        # 3. 고개 방향 감지 - 3회 경고 후 중단
        current_head_abnormal = head_direction in ["Left", "Right", "Down"]
        if current_head_abnormal != self.is_head_abnormal:
            if not current_head_abnormal and self.is_head_violation:
                # 위반 상태 종료
                total_duration = current_time - self.head_abnormal_start_time
                print(f"{self.GREEN}[{datetime.now().strftime('%H:%M:%S')}] 고개 방향 정상화 (지속시간: {total_duration:.1f}초){self.END}")
           
            self.is_head_abnormal = current_head_abnormal
            self.head_abnormal_start_time = current_time
            self.is_head_violation = False
       
        if self.is_head_abnormal:
            duration = current_time - self.head_abnormal_start_time
            if duration >= self.SUSTAINED_TIME and not self.is_head_violation:
                self.is_head_violation = True
                # 경고 발급
                is_terminated = self.issue_warning("고개 방향", f"방향: {head_direction}")
                if is_terminated:
                    return
            elif duration < self.SUSTAINED_TIME and duration > 0.5:
                self.print_warning("고개 방향", f"{head_direction} 방향으로 움직임", duration)
       
        # 4. 시선 이탈 감지 - 3회 경고 후 중단
        if self.gaze_baseline is not None and gaze_ratio != 1:
            current_gaze_abnormal = (gaze_ratio < self.gaze_baseline - self.GAZE_MARGIN or
                                   gaze_ratio > self.gaze_baseline + self.GAZE_MARGIN)
           
            if current_gaze_abnormal != self.is_gaze_abnormal:
                if not current_gaze_abnormal and self.is_gaze_violation:
                    # 위반 상태 종료
                    total_duration = current_time - self.gaze_abnormal_start_time
                    print(f"{self.GREEN}[{datetime.now().strftime('%H:%M:%S')}] 시선 정상화 (지속시간: {total_duration:.1f}초){self.END}")
               
                self.is_gaze_abnormal = current_gaze_abnormal
                self.gaze_abnormal_start_time = current_time
                self.is_gaze_violation = False
           
            if self.is_gaze_abnormal:
                duration = current_time - self.gaze_abnormal_start_time
                if duration >= self.SUSTAINED_TIME and not self.is_gaze_violation:
                    self.is_gaze_violation = True
                    direction = "오른쪽" if gaze_ratio < self.gaze_baseline else "왼쪽"
                    # 경고 발급
                    is_terminated = self.issue_warning("시선 이탈", f"{direction} 방향으로 시선 이탈")
                    if is_terminated:
                        return
                elif duration < self.SUSTAINED_TIME and duration > 0.5:
                    direction = "오른쪽" if gaze_ratio < self.gaze_baseline else "왼쪽"
                    deviation = abs(gaze_ratio - self.gaze_baseline)
                    self.print_warning("시선 이탈", f"{direction} 시선 (편차: {deviation:.2f})", duration)
   
    def print_terminal_status(self, face_count, head_direction, gaze_ratio):
        """터미널에 실시간 상태 출력"""
        current_time = time.time()
       
        if current_time - self.last_status_print >= self.PRINT_INTERVAL:
            timestamp = datetime.now().strftime("%H:%M:%S")
            exam_duration = int(current_time - self.exam_start_time) if self.exam_start_time else 0
           
            status_msg = f"[{timestamp}] [{exam_duration:04d}s] "
           
            # 얼굴 감지 상태
            if face_count == 0:
                status_msg += f"{self.RED}얼굴 없음{self.END}"
            elif face_count == 1:
                status_msg += f"{self.GREEN}정상 (1명){self.END}"
            else:
                status_msg += f"{self.RED}다중 인물 ({face_count}명){self.END}"
           
            # 고개 방향 상태
            if head_direction == "Forward":
                status_msg += f" | 고개: {self.GREEN}정면{self.END}"
            else:
                status_msg += f" | 고개: {self.YELLOW}{head_direction}{self.END}"
           
            # 시선 상태
            if self.gaze_baseline is None:
                status_msg += f" | 시선: {self.BLUE}캘리브레이션 중{self.END}"
            elif gaze_ratio != 1:
                if (gaze_ratio >= self.gaze_baseline - self.GAZE_MARGIN and
                    gaze_ratio <= self.gaze_baseline + self.GAZE_MARGIN):
                    status_msg += f" | 시선: {self.GREEN}정상{self.END}"
                else:
                    direction = "오른쪽" if gaze_ratio < self.gaze_baseline else "왼쪽"
                    status_msg += f" | 시선: {self.YELLOW}{direction} 이탈{self.END}"
           
            # 경고 상태 추가
            status_msg += f" | 경고: {self.total_warnings}/{self.MAX_WARNINGS} (고개:{self.head_warnings}, 시선:{self.gaze_warnings})"
           
            print(status_msg)
            self.last_status_print = current_time
   
    def print_violation_alert(self, violation_type, details, is_start=True, duration=0):
        """위반 사항 터미널 알림"""
        timestamp = datetime.now().strftime("%H:%M:%S")
       
        if is_start:
            print(f"\n{self.BOLD}{self.RED}🚨 위반 감지! 🚨{self.END}")
            print(f"{self.RED}┌─────────────────────────────────────────────────────────────┐{self.END}")
            print(f"{self.RED}│ 시간: {timestamp:<20} 유형: {violation_type:<20} │{self.END}")
            print(f"{self.RED}│ 상세: {details:<50} │{self.END}")
            print(f"{self.RED}│ 지속시간: {duration:.1f}초{' ' * 40}│{self.END}")
            print(f"{self.RED}└─────────────────────────────────────────────────────────────┘{self.END}")
            print()
            self.total_violations += 1
            self.log_violation(violation_type, details)
           
        else:
            print(f"{self.GREEN}[{timestamp}] 위반 종료: {violation_type} (총 지속시간: {duration:.1f}초){self.END}")
   
    def print_warning(self, warning_type, details, duration):
        """경고 사항 터미널 출력"""
        timestamp = datetime.now().strftime("%H:%M:%S")
       
        progress = min(duration / self.SUSTAINED_TIME, 1.0) * 100
        bar_length = 20
        filled_length = int(bar_length * progress / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
       
        print(f"{self.YELLOW}[{timestamp}] ⚠️  {warning_type}: {details} [{bar}] {progress:.0f}% ({duration:.1f}s){self.END}")
   
    def log_violation(self, violation_type, details):
        """위반 사항 로그 기록"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "user": self.authenticated_user,
            "type": violation_type,
            "details": details,
            "exam_duration": int(time.time() - self.exam_start_time) if self.exam_start_time else 0,
            "total_warnings": self.total_warnings,
            "head_warnings": self.head_warnings,
            "gaze_warnings": self.gaze_warnings
        }
        self.violation_log.append(log_entry)
   
    def draw_status_info(self, frame, face_count, head_direction, gaze_ratio, x_ratio, y_ratio):
        """상태 정보를 화면에 표시"""
        current_time = time.time()
        exam_duration = int(current_time - self.exam_start_time) if self.exam_start_time else 0
       
        # 기본 정보 표시
        cv2.putText(frame, f"User: {self.authenticated_user}", (30, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
       
        cv2.putText(frame, f"Exam Time: {exam_duration}s", (30, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
       
        cv2.putText(frame, f"Faces: {face_count}", (30, 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
       
        cv2.putText(frame, f"Head: {head_direction}", (30, 120),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
       
        if self.gaze_baseline is not None:
            cv2.putText(frame, f"Gaze: {gaze_ratio:.2f} (Base: {self.gaze_baseline:.2f})", (30, 150),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        else:
            cv2.putText(frame, f"Gaze: {gaze_ratio:.2f} (Calibrating...)", (30, 150),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
       
        # 경고 횟수 표시 (통합)
        warning_color = (0, 255, 255) if self.total_warnings < self.MAX_WARNINGS else (0, 0, 255)
        cv2.putText(frame, f"Total Warnings: {self.total_warnings}/{self.MAX_WARNINGS}", (30, 180),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, warning_color, 2)
       
        cv2.putText(frame, f"Head: {self.head_warnings}, Gaze: {self.gaze_warnings}", (30, 210),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
       
        # 위반 상태 표시
        y_offset = 240
       
        violations = []
        if self.is_multiple_faces_violation:
            violations.append("Multiple Faces")
        if self.is_no_face_violation:
            violations.append("No Face")
        if self.is_head_violation:
            violations.append(f"Head: {head_direction}")
        if self.is_gaze_violation:
            violations.append("Gaze Direction")
       
        if violations:
            cv2.putText(frame, f"VIOLATIONS: {', '.join(violations)}", (30, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
       
        # 시험 중단 상태 표시
        if self.exam_terminated:
            # 부정행위 탐지로 인한 중단 강조 표시
            cv2.putText(frame, "CHEATING DETECTED!", (30, y_offset + 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            cv2.putText(frame, "EXAM TERMINATED", (30, y_offset + 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
            cv2.putText(frame, f"Reason: {self.termination_reason}", (30, y_offset + 120),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
           
            # 화면 전체에 경고 테두리 표시
            cv2.rectangle(frame, (10, 10), (frame.shape[1]-10, frame.shape[0]-10), (0, 0, 255), 5)
       
        # 캘리브레이션 상태 표시
        if self.gaze_baseline is None:
            progress = (self.frame_count / self.BASELINE_FRAMES) * 100
            cv2.putText(frame, f"Eye Calibration: {self.frame_count}/{self.BASELINE_FRAMES} ({progress:.0f}%)",
                       (30, frame.shape[0] - 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            cv2.putText(frame, "Look forward and stay still",
                       (30, frame.shape[0] - 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
       
        # 위반 횟수 표시
        cv2.putText(frame, f"Total Violations: {self.total_violations}",
                   (frame.shape[1] - 300, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255) if self.total_violations > 0 else (0, 255, 0), 2)
   
    def exam_monitoring_phase(self, cap, out=None):
        """시험 감독 단계"""
        print(f"\n{self.BOLD}{self.GREEN}📝 2단계: 시험 감독 시작{self.END}")
        print(f"{self.GREEN}응시자: {self.authenticated_user}{self.END}")
        print(f"{self.CYAN}실시간 부정행위 탐지 시작...{self.END}")
        print(f"{self.YELLOW}키보드 단축키: ESC(종료), M(미러링), D(디버그){self.END}")
        print("=" * 70)
       
        self.exam_start_time = time.time()
       
        while not self.exam_terminated:
            ret, frame = cap.read()
            if not ret:
                print(f"{self.RED}❌ 프레임을 가져올 수 없습니다.{self.END}")
                break
           
            if self.MIRROR_CAMERA:
                frame = cv2.flip(frame, 1)
           
            if out:
                out.write(frame)
           
            # MediaPipe 처리
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img_h, img_w = frame.shape[:2]
           
            results = self.face_mesh.process(frame_rgb)
           
            # 초기값 설정
            face_count = 0
            head_direction = "No Face"
            x_ratio, y_ratio = 0, 0
            gaze_ratio = 1
           
            if results.multi_face_landmarks:
                face_count = len(results.multi_face_landmarks)
               
                # 첫 번째 얼굴로 분석
                best_face = results.multi_face_landmarks[0]
                current_landmarks = self.get_landmarks_coords(best_face, img_w, img_h)
               
                # 머리 방향 분석
                head_direction, x_ratio, y_ratio = self.get_head_direction(current_landmarks, img_w, img_h)
               
                # 시선 분석
                landmarks_normalized = [(lm.x, lm.y) for lm in best_face.landmark]
                gaze_left = self.get_gaze_ratio(self.LEFT_EYE, landmarks_normalized, frame, gray)
                gaze_right = self.get_gaze_ratio(self.RIGHT_EYE, landmarks_normalized, frame, gray)
                current_gaze = (gaze_left + gaze_right) / 2
               
                # 캘리브레이션 처리
                if self.frame_count < self.BASELINE_FRAMES:
                    self.baseline_sum += current_gaze
                    self.frame_count += 1
                   
                    if self.frame_count == self.BASELINE_FRAMES:
                        self.gaze_baseline = self.baseline_sum / self.BASELINE_FRAMES
                        print(f"{self.BOLD}{self.GREEN}✅ 시선 캘리브레이션 완료! (기준값: {self.gaze_baseline:.2f}){self.END}")
                        speak_tts("시선 기준 처리가 완료되었습니다. 시험을 시작합니다.")
                   
                    gaze_ratio = current_gaze
                else:
                    gaze_ratio = current_gaze
               
                # 얼굴 랜드마크 시각화 (라즈베리파이 최적화 - 간소화)
                if self.GAZE_DEBUG_MODE:
                    self.mp_drawing.draw_landmarks(
                        frame, best_face, self.mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=self.mp_drawing.DrawingSpec(
                            color=(0, 255, 255), thickness=1, circle_radius=1)
                    )
           
            # 터미널 상태 출력
            self.print_terminal_status(face_count, head_direction, gaze_ratio)
           
            # 위반 상태 업데이트
            self.update_violation_states(face_count, head_direction, gaze_ratio)
           
            # 화면에 정보 표시
            self.draw_status_info(frame, face_count, head_direction, gaze_ratio, x_ratio, y_ratio)
           
            # 프레임 표시
            cv2.imshow("AI Exam Supervisor - Monitoring", frame)
           
            # 키보드 입력 처리
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord('m') or key == ord('M'):
                self.MIRROR_CAMERA = not self.MIRROR_CAMERA
                print(f"{self.CYAN}카메라 미러링: {'ON' if self.MIRROR_CAMERA else 'OFF'}{self.END}")
            elif key == ord('d') or key == ord('D'):
                self.GAZE_DEBUG_MODE = not self.GAZE_DEBUG_MODE
                print(f"{self.CYAN}디버그 모드: {'ON' if self.GAZE_DEBUG_MODE else 'OFF'}{self.END}")
           
            # 시험이 중단된 경우 3초 대기 후 종료
            if self.exam_terminated:
                for i in range(30):  # 3초 대기 (100ms * 30)
                    ret, frame = cap.read()
                    if ret:
                        if self.MIRROR_CAMERA:
                            frame = cv2.flip(frame, 1)
                        self.draw_status_info(frame, face_count, head_direction, gaze_ratio, x_ratio, y_ratio)
                        cv2.imshow("AI Exam Supervisor - Monitoring", frame)
                    cv2.waitKey(100)
                break
       
        return True
   
    def save_exam_report(self):
        """시험 결과 보고서 저장"""
        if not self.exam_start_time:
            return
       
        exam_duration = int(time.time() - self.exam_start_time)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
       
        report = {
            "exam_info": {
                "user": self.authenticated_user,
                "start_time": datetime.fromtimestamp(self.exam_start_time).strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "duration_seconds": exam_duration,
                "total_violations": self.total_violations,
                "exam_terminated": self.exam_terminated,
                "termination_reason": self.termination_reason,
                "total_warnings": self.total_warnings,
                "head_warnings": self.head_warnings,
                "gaze_warnings": self.gaze_warnings
            },
            "violations": self.violation_log,
            "system_config": self.config
        }
       
        report_path = os.path.join(self.LOG_PATH, f"exam_report_{self.authenticated_user}_{timestamp}.json")
       
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"{self.GREEN}📄 시험 보고서 저장: {report_path}{self.END}")
        except Exception as e:
            print(f"{self.RED}❌ 보고서 저장 실패: {e}{self.END}")
   
    def print_final_report(self):
        """최종 결과 출력"""
        if not self.exam_start_time:
            return
       
        exam_duration = int(time.time() - self.exam_start_time)
       
        print(f"\n{self.BOLD}{self.BLUE}=" * 70 + "{self.END}")
        print(f"{self.BOLD}{self.BLUE}🏁 시험 종료 - 최종 결과{self.END}")
        print(f"{self.BOLD}{self.BLUE}=" * 70 + "{self.END}")
       
        print(f"{self.CYAN}응시자: {self.authenticated_user}{self.END}")
        print(f"{self.CYAN}시험 시간: {exam_duration // 60}분 {exam_duration % 60}초{self.END}")
       
        # 시험 중단 여부 표시
        if self.exam_terminated:
            print(f"{self.BOLD}{self.RED}🚨 부정행위 탐지로 시험 중단됨: {self.termination_reason}{self.END}")
            print(f"{self.RED}⚠️  심각한 부정행위로 인해 시험이 즉시 중단되었습니다!{self.END}")
            print(f"{self.RED}📋 이 결과는 시험 관리자에게 자동 보고됩니다.{self.END}")
        else:
            print(f"{self.GREEN}✅ 정상 종료 - 시험이 완료되었습니다{self.END}")
       
        # 경고 횟수 표시
        print(f"\n{self.BOLD}📊 경고 현황:{self.END}")
        print(f"  • 총 경고 횟수: {self.total_warnings}/{self.MAX_WARNINGS}회")
        print(f"    - 고개 방향 경고: {self.head_warnings}회")
        print(f"    - 시선 이탈 경고: {self.gaze_warnings}회")
       
        if self.total_violations > 0:
            print(f"\n{self.RED}총 위반 횟수: {self.total_violations}회{self.END}")
           
            # 위반 유형별 통계
            violation_types = {}
            for log in self.violation_log:
                vtype = log['type']
                violation_types[vtype] = violation_types.get(vtype, 0) + 1
           
            print(f"\n{self.BOLD}📋 위반 유형별 통계:{self.END}")
            for vtype, count in violation_types.items():
                print(f"  • {vtype}: {count}회")
        else:
            print(f"\n{self.GREEN}✅ 위반 사항 없음{self.END}")
       
        print(f"{self.BOLD}{self.BLUE}=" * 70 + "{self.END}")
   
    def run(self):
        """메인 실행 함수"""
        # 카메라 초기화
        cap = self.find_camera()
        if cap is None:
            print(f"{self.RED}❌ 카메라 연결 실패{self.END}")
            return False
       
        # 비디오 저장 설정
        out = None
        if self.SAVE_VIDEO:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_path = os.path.join(self.LOG_PATH, f"exam_video_{timestamp}.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(video_path, fourcc, self.CAMERA_FPS,
                                (self.CAMERA_WIDTH, self.CAMERA_HEIGHT))
       
        try:
            # 1단계: 신원 확인
            if not self.identity_verification_phase(cap):
                return False
           
            # 단계 전환
            self.system_phase = "EXAM_MONITORING"
            cv2.destroyAllWindows()  # 이전 창 닫기
            time.sleep(1)
           
            # 2단계: 시험 감독
            self.exam_monitoring_phase(cap, out)
           
            return True
           
        except KeyboardInterrupt:
            print(f"\n{self.YELLOW}사용자에 의해 중단되었습니다.{self.END}")
            return False
        except Exception as e:
            print(f"{self.RED}❌ 시스템 오류: {e}{self.END}")
            return False
        finally:
            # 리소스 정리
            cap.release()
            if out:
                out.release()
            cv2.destroyAllWindows()
           
            # 최종 보고서
            if self.authenticated_user:
                self.print_final_report()
                self.save_exam_report()
           
            print(f"{self.CYAN}🔒 AI 시험 감독관 시스템 종료{self.END}")

def speak_tts(text, lang='ko'):
    tts = gTTS(text=text, lang=lang)
    tts_path = "tts_output.mp3"
    tts.save(tts_path)
    os.system(f"mpg123 {tts_path}")
    os.remove(tts_path)

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description="AI 시험 감독관 시스템 v2.1")
    parser.add_argument("--config", default="config.json", help="설정 파일 경로")
    parser.add_argument("--dataset", default="./dataset", help="얼굴 데이터셋 경로")
    parser.add_argument("--camera", type=int, default=0, help="카메라 인덱스")
   
    args = parser.parse_args()
   
    print(f"""
{chr(27)}[96m╔═══════════════════════════════════════════════════════════════════════╗
║                   🤖 AI 시험 감독관 시스템 v2.1                      ║
║                    (라즈베리파이5 최적화 버전)                        ║
║                                                                       ║
║  👤 1단계: 신원 확인 (얼굴 인식)                                      ║
║  🔍 2단계: 실시간 부정행위 탐지                                       ║
║     • 다중 인물 감지 → 즉시 부정행위 판정 및 시험 중단               ║
║     • 화면 이탈 감지 → 즉시 부정행위 판정 및 시험 중단               ║
║     • 고개 방향 추적 → 통합 5회 경고 후 부정행위 판정 및 시험 중단   ║
║     • 시선 방향 추적 → 통합 5회 경고 후 부정행위 판정 및 시험 중단   ║
║                                                                       ║
║  📝 로그 및 보고서 자동 생성                                          ║
╚═══════════════════════════════════════════════════════════════════════╝{chr(27)}[0m
""")
   
    try:
        supervisor = AIExamSupervisorIntegrated(args.config)
        supervisor.run()
    except Exception as e:
        print(f"{chr(27)}[91m❌ 시스템 초기화 실패: {e}{chr(27)}[0m")
        sys.exit(1)

if __name__ == "__main__":
    main()
