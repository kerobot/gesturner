import time
from gesturner.gaze_detector import GazeDetector
from gesturner.mouth_detector import MouthDetector
from gesturner.key_controller import send_down_key, send_up_key

class GestureController:
    def __init__(self):
        self.gaze_detector = GazeDetector()
        self.mouth_detector = MouthDetector()
        
        self.last_look_down_time = None
        self.LOOK_DOWN_DURATION = 1.0
        
        self.last_look_up_time = None
        self.LOOK_UP_DURATION = 1.0
        
        self.last_key_sent_time = 0

    def process(self, frame):
        """
        フレームを処理してジェスチャーを検知し、条件を満たせばキーを送信する。
        
        Returns:
            dict: 検知状態やデバッグ情報を含む辞書
        """
        # 検知
        gaze_direction = self.gaze_detector.detect_gaze(frame)
        mouth_detected = self.mouth_detector.detect_gesture(frame)
        
        current_time = time.time()
        
        # 口パク（下スクロール）
        if mouth_detected:
            if self.last_look_down_time is None:
                self.last_look_down_time = current_time
            elif current_time - self.last_look_down_time > self.LOOK_DOWN_DURATION:
                send_down_key()
                self.last_key_sent_time = current_time
                self.last_look_down_time = None # アクション実行後はリセット
        else:
            self.last_look_down_time = None
            
        # 上を見る（上スクロール）
        if gaze_direction == "UP":
            if self.last_look_up_time is None:
                self.last_look_up_time = current_time
            elif current_time - self.last_look_up_time > self.LOOK_UP_DURATION:
                send_up_key()
                self.last_key_sent_time = current_time
                self.last_look_up_time = None # アクション実行後はリセット
        else:
            self.last_look_up_time = None
            
        return {
            "mouth_detected": mouth_detected,
            "gaze_direction": gaze_direction,
            "last_key_sent_time": self.last_key_sent_time
        }
