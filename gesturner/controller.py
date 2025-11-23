from __future__ import annotations

import time
from typing import Optional, TypedDict

import numpy as np

from gesturner.gaze_detector import GazeDetector
from gesturner.mouth_detector import MouthDetector
from gesturner.key_controller import send_down_key, send_up_key


class ProcessResult(TypedDict):
    """ジェスチャー処理結果を格納する型定義。

    Attributes:
        mouth_detected: 口が開いているかどうか
        gaze_direction: 視線方向（"DOWN", "UP", "NEUTRAL", None）
        last_key_sent_time: 最後にキーを送信した時刻（Unix時間）
    """

    mouth_detected: bool
    gaze_direction: Optional[str]
    last_key_sent_time: float


class GestureController:
    """ジェスチャー検知とキー送信を制御するコントローラー。

    口の開閉と視線方向を継続的に監視し、
    一定時間ジェスチャーが持続した場合にキー入力を送信します。
    """

    def __init__(self) -> None:
        """GestureControllerを初期化します。"""
        # 検知器の初期化
        self.gaze_detector: GazeDetector = GazeDetector()
        self.mouth_detector: MouthDetector = MouthDetector()

        # 口開閉検知の状態管理
        self.last_look_down_time: Optional[float] = None  # 口が開き始めた時刻
        self.LOOK_DOWN_DURATION: float = 1.0  # キー送信までの継続時間（秒）

        # 上視線検知の状態管理
        self.last_look_up_time: Optional[float] = None  # 上を向き始めた時刻
        self.LOOK_UP_DURATION: float = 1.0  # キー送信までの継続時間（秒）

        # 最後にキーを送信した時刻
        self.last_key_sent_time: float = 0.0

    def process(self, frame: np.ndarray) -> ProcessResult:
        """
        フレームを処理してジェスチャーを検知し、条件を満たせばキーを送信する。

        Returns:
            ProcessResult: 検知状態やデバッグ情報を含む辞書
        """
        # 検知
        gaze_direction: Optional[str] = self.gaze_detector.detect_gaze(frame)
        mouth_detected: bool = self.mouth_detector.detect_gesture(frame)

        current_time: float = time.time()

        # 口パク（下スクロール）
        if mouth_detected:
            if self.last_look_down_time is None:
                self.last_look_down_time = current_time
            elif current_time - self.last_look_down_time > self.LOOK_DOWN_DURATION:
                send_down_key()
                self.last_key_sent_time = current_time
                self.last_look_down_time = None  # アクション実行後はリセット
        else:
            self.last_look_down_time = None

        # 上を見る（上スクロール）
        if gaze_direction == "UP":
            if self.last_look_up_time is None:
                self.last_look_up_time = current_time
            elif current_time - self.last_look_up_time > self.LOOK_UP_DURATION:
                send_up_key()
                self.last_key_sent_time = current_time
                self.last_look_up_time = None  # アクション実行後はリセット
        else:
            self.last_look_up_time = None

        return ProcessResult(
            mouth_detected=mouth_detected,
            gaze_direction=gaze_direction,
            last_key_sent_time=self.last_key_sent_time,
        )
