from __future__ import annotations

import cv2
import mediapipe as mp  # type: ignore
import numpy as np
from typing import Optional, Literal

# 視線方向を表す型（DOWN: 下向き, UP: 上向き, NEUTRAL: 中立, None: 検出失敗）
GazeDirection = Optional[Literal["DOWN", "UP", "NEUTRAL"]]


class GazeDetector:
    """MediaPipeを使用して視線方向を検知するクラス。

    虹彩の位置から視線の向きを推定し、
    上向き・下向き・中立の3状態を判定します。
    """

    def __init__(self, down_threshold: float = 0.6, up_threshold: float = 0.4) -> None:
        """GazeDetectorを初期化します。

        Args:
            down_threshold: 下向き判定の閾値（虹彩の相対位置）
            up_threshold: 上向き判定の閾値（虹彩の相対位置）
        """
        self.face_mesh: mp.solutions.face_mesh.FaceMesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)  # type: ignore
        self.down_threshold: float = down_threshold
        self.up_threshold: float = up_threshold

    def detect_gaze(self, frame: np.ndarray) -> GazeDirection:
        """フレームから視線方向を検知します。

        Args:
            frame: 入力画像（BGR形式のnumpy配列）

        Returns:
            視線方向（"DOWN", "UP", "NEUTRAL", またはNone）
        """
        rgb_frame: np.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
                left_eye_height: float = left_bottom.y - left_top.y
                right_eye_height: float = right_bottom.y - right_top.y

                # 目が閉じている、または検出が不安定な場合はスキップ
                if left_eye_height < 0.005 or right_eye_height < 0.005:
                    continue

                # 虹彩の相対位置を計算 (0.0=上端, 1.0=下端)
                # Y座標は下に行くほど大きくなるため、(虹彩 - 上) / 高さ で比率が出る
                left_ratio: float = (left_iris.y - left_top.y) / left_eye_height
                right_ratio: float = (right_iris.y - right_top.y) / right_eye_height

                avg_ratio: float = (left_ratio + right_ratio) / 2.0

                if avg_ratio > self.down_threshold:
                    return "DOWN"
                if avg_ratio < self.up_threshold:
                    return "UP"
                return "NEUTRAL"
        return None
