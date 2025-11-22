import cv2
import mediapipe as mp

class MouthDetector:
    def __init__(self, threshold=0.05):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.threshold = threshold

    def detect_gesture(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # 口のランドマーク: 上唇(13), 下唇(14)
                upper_lip = face_landmarks.landmark[13]
                lower_lip = face_landmarks.landmark[14]

                # 顔の高さ基準: 眉間(10) と 顎(152)
                forehead = face_landmarks.landmark[10]
                chin = face_landmarks.landmark[152]

                # 顔の縦幅
                face_height = chin.y - forehead.y

                # 口の開き具合
                mouth_open_dist = lower_lip.y - upper_lip.y

                # 顔の大きさに対する口の開きの比率
                if face_height > 0:
                    ratio = mouth_open_dist / face_height
                    if ratio > self.threshold:
                        return True
        
        return False
