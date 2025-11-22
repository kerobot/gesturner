import cv2
import time
import win32gui
import win32con

class DebugWindow:
    def __init__(self, window_name='Gesture Debug'):
        self.window_name = window_name
        self.window_initialized = False

    def update(self, frame, is_detected, last_key_sent_time):
        # プライバシー保護処理: 解像度を落として二値化
        h, w = frame.shape[:2]
        # 1/8に縮小
        small = cv2.resize(frame, (w//8, h//8), interpolation=cv2.INTER_LINEAR)
        # グレースケール化
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        # 二値化
        _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        
        # 表示サイズを元の半分にする
        display_h, display_w = h // 2, w // 2
        # 最近傍補間で拡大（ドット感を出す）
        display_frame = cv2.resize(binary, (display_w, display_h), interpolation=cv2.INTER_NEAREST)
        # カラー形式に戻す（テキスト描画のため）
        display_frame = cv2.cvtColor(display_frame, cv2.COLOR_GRAY2BGR)

        # 検出状況を表示する
        status_text = "Detected" if is_detected else "Neutral"
        cv2.putText(display_frame, f"Status: {status_text}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # キー送信直後の場合はキー押下を表示する
        if time.time() - last_key_sent_time < 1.0:
            cv2.putText(display_frame, "KEY SENT", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # 撮影したフレームを表示
        cv2.imshow(self.window_name, display_frame)

        if not self.window_initialized:
            hwnd = win32gui.FindWindow(None, self.window_name)
            if hwnd:
                # 最前面に表示し、アクティブ化しない設定を行う
                # HWND_TOPMOST: 最前面
                # SWP_NOACTIVATE: ウィンドウをアクティブにしない
                # 位置を指定 (Overlayの下: x=50, y=50+50+10=110)
                x = 50
                y = 110
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, 0, 0, 
                                      win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
                
                # 拡張スタイル WS_EX_NOACTIVATE を追加して、クリックしてもアクティブにならないようにする
                ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_NOACTIVATE)
                
                self.window_initialized = True

    def close(self):
        cv2.destroyWindow(self.window_name)
