import cv2
import mediapipe as mp

class GazeDetector:
    def __init__(self, down_threshold=0.6):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.down_threshold = down_threshold

    def detect_gaze(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # 左目のランドマーク (上まぶた: 159, 下まぶた: 145, 虹彩: 468)
                left_top = face_landmarks.landmark[159]
                left_bottom = face_landmarks.landmark[145]
                left_iris = face_landmarks.landmark[468]

                # 右目のランドマーク (上まぶた: 386, 下まぶた: 374, 虹彩: 473)
                right_top = face_landmarks.landmark[386]
                right_bottom = face_landmarks.landmark[374]
                right_iris = face_landmarks.landmark[473]

                # 目の高さを計算
                left_eye_height = left_bottom.y - left_top.y
                right_eye_height = right_bottom.y - right_top.y

                # 目が閉じている、または検出が不安定な場合はスキップ
                if left_eye_height < 0.005 or right_eye_height < 0.005:
                    continue

                # 虹彩の相対位置を計算 (0.0=上端, 1.0=下端)
                # Y座標は下に行くほど大きくなるため、(虹彩 - 上) / 高さ で比率が出る
                left_ratio = (left_iris.y - left_top.y) / left_eye_height
                right_ratio = (right_iris.y - right_top.y) / right_eye_height

                avg_ratio = (left_ratio + right_ratio) / 2.0
                
                return avg_ratio > self.down_threshold
        return False
