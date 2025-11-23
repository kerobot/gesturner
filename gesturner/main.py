"""Gesturnerアプリケーションのメインエントリーポイント。

カメラからの映像をリアルタイムで解析し、
ジェスチャー（口の開閉・視線方向）を検知してキー入力を送信します。
"""

import os
import argparse
from threading import Thread
from typing import Optional

import cv2
import numpy as np

# TensorFlow/MediaPipeのログレベル設定
# 0 = 全て表示, 1 = INFOを非表示, 2 = WARNINGを非表示, 3 = ERRORを非表示
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "0"

from gesturner.overlay import Overlay
from gesturner.debug_window import DebugWindow
from gesturner.controller import GestureController, ProcessResult


def run() -> None:
    """アプリケーションを起動します。

    コマンドライン引数を解析し、カメラループとUIを初期化して実行します。
    --debugオプションでデバッグウィンドウを表示できます。
    """
    parser = argparse.ArgumentParser(description="Gesturner application")
    parser.add_argument("--debug", action="store_true", help="Enable debug window")
    args = parser.parse_args()

    controller: GestureController = GestureController()
    overlay: Overlay = Overlay()
    debug_window: Optional[DebugWindow] = DebugWindow() if args.debug else None

    def camera_loop() -> None:
        """カメラからフレームを取得し、ジェスチャー検知を実行するループ。

        バックグラウンドスレッドで実行され、継続的にジェスチャーを監視します。
        ESCキー（キーコード27）で終了できます。
        """
        """カメラからフレームを取得し、ジェスチャー検知を実行するループ。
        
        バックグラウンドスレッドで実行され、継続的にジェスチャーを監視します。
        ESCキー（キーコード27）で終了できます。
        """
        # カメラデバイスを開く（デバイスID: 0）
        cap: cv2.VideoCapture = cv2.VideoCapture(0)

        while cap.isOpened():
            success: bool
            frame: np.ndarray
            success, frame = cap.read()
            if not success:
                break

            # ジェスチャー処理と判定
            result: ProcessResult = controller.process(frame)

            mouth_detected: bool = result["mouth_detected"]
            gaze_direction: Optional[str] = result["gaze_direction"]
            last_key_sent_time: float = result["last_key_sent_time"]

            # UI更新
            is_any_detected: bool = mouth_detected or (gaze_direction == "UP")
            overlay.update_status(is_any_detected)

            if debug_window:
                debug_window.update(
                    frame, mouth_detected, gaze_direction, last_key_sent_time
                )

            # ESCキーが押されたら終了
            if cv2.waitKey(5) & 0xFF == 27:
                break

        # リソースの解放
        cap.release()
        if debug_window:
            debug_window.close()
        cv2.destroyAllWindows()

    # カメラループをバックグラウンドスレッドで起動
    Thread(target=camera_loop, daemon=True).start()
    # メインスレッドでオーバーレイUIを実行（ブロッキング）
    overlay.start()


if __name__ == "__main__":
    run()
