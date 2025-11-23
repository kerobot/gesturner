from __future__ import annotations

import cv2
import mediapipe as mp  # type: ignore
import numpy as np


class MouthDetector:
    """MediaPipeを使用して口の開閉を検知するクラス。

    顔のランドマークから口の開き具合を計算し、
    閾値を超えたら口が開いていると判定します。
    """

    def __init__(self, threshold: float = 0.05) -> None:
        """MouthDetectorを初期化します。

        Args:
            threshold: 口の開き判定の閾値（顔の高さに対する比率）
        """
        self.face_mesh: mp.solutions.face_mesh.FaceMesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)  # type: ignore
        self.threshold: float = threshold

    def detect_gesture(self, frame: np.ndarray) -> bool:
        """フレームから口の開閉を検知します。

        Args:
            frame: 入力画像（BGR形式のnumpy配列）

        Returns:
            口が開いている場合True、閉じている場合False
        """
        rgb_frame: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
                face_height: float = chin.y - forehead.y

                # 口の開き具合
                mouth_open_dist: float = lower_lip.y - upper_lip.y

                # 顔の大きさに対する口の開きの比率
                if face_height > 0.0:
                    ratio: float = mouth_open_dist / face_height
                    if ratio > self.threshold:
                        return True

        return False
