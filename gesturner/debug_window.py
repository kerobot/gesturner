from __future__ import annotations

import cv2
import time
import win32gui  # type: ignore
import win32con  # type: ignore
import numpy as np
from typing import Optional


class DebugWindow:
    """デバッグ用のプライバシー保護ウィンドウ。

    カメラ映像を低解像度・二値化して表示し、
    ジェスチャー検知状態とキー送信状況を視覚的に確認できます。
    """

    def __init__(self, window_name: str = "Gesture Debug") -> None:
        """デバッグウィンドウを初期化します。

        Args:
            window_name: ウィンドウのタイトル名
        """
        self.window_name: str = window_name
        self.window_initialized: bool = False

    def update(
        self,
        frame: np.ndarray,
        mouth_detected: bool,
        gaze_direction: Optional[str],
        last_key_sent_time: float,
    ) -> None:
        """デバッグ情報を表示更新します。

        Args:
            frame: 入力画像（BGR形式）
            mouth_detected: 口開閉検知の状態
            gaze_direction: 視線方向
            last_key_sent_time: 最後にキーを送信した時刻
        """
        # プライバシー保護処理: 解像度を落として二値化
        h, w = frame.shape[:2]
        # 1/8に縮小
        small: np.ndarray = cv2.resize(
            frame, (w // 8, h // 8), interpolation=cv2.INTER_LINEAR
        )
        # グレースケール化
        gray: np.ndarray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        # 二値化
        _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        # 表示サイズを元の半分にする
        display_h: int = h // 2
        display_w: int = w // 2
        # 最近傍補間で拡大（ドット感を出す）
        display_frame: np.ndarray = cv2.resize(
            binary, (display_w, display_h), interpolation=cv2.INTER_NEAREST
        )
        # カラー形式に戻す（テキスト描画のため）
        display_frame = cv2.cvtColor(display_frame, cv2.COLOR_GRAY2BGR)

        # 口の検出状況を表示する
        status_text: str = "Mouth: Detected" if mouth_detected else "Mouth: Neutral"
        cv2.putText(
            display_frame,
            status_text,
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        # 目の検出状況を表示する
        gaze_text: str = f"Gaze: {gaze_direction}" if gaze_direction else "Gaze: --"
        cv2.putText(
            display_frame,
            gaze_text,
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        # キー送信直後の場合はキー押下を表示する
        if time.time() - last_key_sent_time < 1.0:
            cv2.putText(
                display_frame,
                "KEY SENT",
                (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
            )

        # 撮影したフレームを表示
        cv2.imshow(self.window_name, display_frame)

        if not self.window_initialized:
            hwnd: int = win32gui.FindWindow(None, self.window_name)
            if hwnd:
                # 最前面に表示し、アクティブ化しない設定を行う
                # HWND_TOPMOST: 最前面
                # SWP_NOACTIVATE: ウィンドウをアクティブにしない
                # 位置を指定 (Overlayの下: x=50, y=50+50+10=110)
                x: int = 50
                y: int = 110
                win32gui.SetWindowPos(
                    hwnd,
                    win32con.HWND_TOPMOST,
                    x,
                    y,
                    0,
                    0,
                    win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE,
                )

                # 拡張スタイル WS_EX_NOACTIVATE を追加して、クリックしてもアクティブにならないようにする
                ex_style: int = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                win32gui.SetWindowLong(
                    hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_NOACTIVATE
                )

                self.window_initialized = True

    def close(self) -> None:
        """デバッグウィンドウを閉じます。"""
        cv2.destroyWindow(self.window_name)
