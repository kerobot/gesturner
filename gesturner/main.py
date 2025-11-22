import os
# 0 = 全て表示, 1 = INFOを非表示, 2 = WARNINGを非表示, 3 = ERRORを非表示
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'

import cv2
import time
from threading import Thread
# from gesturner.gaze_detector import GazeDetector
from gesturner.mouth_detector import MouthDetector
from gesturner.overlay import Overlay
from gesturner.key_controller import send_down_key
from gesturner.debug_window import DebugWindow

def run():
    # gaze_detector = GazeDetector()
    mouth_detector = MouthDetector()
    overlay = Overlay()
    debug_window = DebugWindow()

    last_look_down_time = None
    LOOK_DOWN_DURATION = 1.0

    def camera_loop():
        nonlocal last_look_down_time
        cap = cv2.VideoCapture(0)
        last_key_sent_time = 0

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # gaze_detected = gaze_detector.detect_gaze(frame)
            mouth_detected = mouth_detector.detect_gesture(frame)
            overlay.update_status(mouth_detected)
            debug_window.update(frame, mouth_detected, last_key_sent_time)

            if mouth_detected:
                if last_look_down_time is None:
                    last_look_down_time = time.time()
                elif time.time() - last_look_down_time > LOOK_DOWN_DURATION:
                    send_down_key()
                    last_key_sent_time = time.time()
                    last_look_down_time = None
            else:
                last_look_down_time = None

            if cv2.waitKey(5) & 0xFF == 27:
                break

        cap.release()
        debug_window.close()
        cv2.destroyAllWindows()

    Thread(target=camera_loop, daemon=True).start()
    overlay.start()

if __name__ == "__main__":
    run()
