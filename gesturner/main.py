import os
import argparse
# 0 = 全て表示, 1 = INFOを非表示, 2 = WARNINGを非表示, 3 = ERRORを非表示
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'

import cv2
from threading import Thread
from gesturner.overlay import Overlay
from gesturner.debug_window import DebugWindow
from gesturner.controller import GestureController

def run():
    parser = argparse.ArgumentParser(description='Gesturner application')
    parser.add_argument('--debug', action='store_true', help='Enable debug window')
    args = parser.parse_args()

    controller = GestureController()
    overlay = Overlay()
    debug_window = DebugWindow() if args.debug else None

    def camera_loop():
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # ジェスチャー処理と判定
            result = controller.process(frame)
            
            mouth_detected = result["mouth_detected"]
            gaze_direction = result["gaze_direction"]
            last_key_sent_time = result["last_key_sent_time"]

            # UI更新
            is_any_detected = mouth_detected or (gaze_direction == "UP")
            overlay.update_status(is_any_detected)
            
            if debug_window:
                debug_window.update(frame, mouth_detected, gaze_direction, last_key_sent_time)

            if cv2.waitKey(5) & 0xFF == 27:
                break

        cap.release()
        if debug_window:
            debug_window.close()
        cv2.destroyAllWindows()

    Thread(target=camera_loop, daemon=True).start()
    overlay.start()

if __name__ == "__main__":
    run()
