import tkinter as tk
import win32gui
import win32con

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gesturner Status")
        self.root.geometry("200x50+50+50")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.7)
        self.root.overrideredirect(True)

        self.label = tk.Label(self.root, text="Neutral", font=("Arial", 20), fg="white", bg="green")
        self.label.pack(expand=True, fill="both")

        # ウィンドウハンドルを取得する前に描画を確定させる
        self.root.update()

        hwnd = win32gui.FindWindow(None, "Gesturner Status")
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 180, win32con.LWA_ALPHA)

    def update_status(self, is_detected):
        if is_detected:
            self.label.config(text="Detected", bg="red")
        else:
            self.label.config(text="Neutral", bg="green")

    def start(self):
        self.root.mainloop()
