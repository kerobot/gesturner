import tkinter as tk
import win32gui  # type: ignore
import win32con  # type: ignore
from typing import Final


class Overlay:
    """ジェスチャー検知状態を表示するオーバーレイウィンドウ。

    常に最前面に表示され、クリックスルー可能な半透明ウィンドウで、
    ジェスチャーの検知状態（Neutral/Detected）を視覚的に通知します。
    """

    WINDOW_TITLE: Final[str] = "Gesturner Status"

    def __init__(self) -> None:
        """オーバーレイウィンドウを初期化します。

        tkinterでウィンドウを作成し、Win32 APIを使用して
        クリックスルー可能な最前面ウィンドウに設定します。
        """
        self.root: tk.Tk = tk.Tk()
        self.root.title(self.WINDOW_TITLE)
        self.root.geometry("200x50+50+50")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.7)
        self.root.overrideredirect(True)

        self.label: tk.Label = tk.Label(
            self.root, text="Neutral", font=("Arial", 20), fg="white", bg="green"
        )
        self.label.pack(expand=True, fill="both")

        # ウィンドウハンドルを取得する前に描画を確定させる
        self.root.update()

        hwnd: int = win32gui.FindWindow(None, self.WINDOW_TITLE)
        style: int = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(
            hwnd,
            win32con.GWL_EXSTYLE,
            style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT,
        )
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 180, win32con.LWA_ALPHA)

    def update_status(self, is_detected: bool) -> None:
        """検知状態に応じて表示を更新します。

        Args:
            is_detected: ジェスチャーが検知された場合True、未検知の場合False
        """
        if is_detected:
            self.label.config(text="Detected", bg="red")
        else:
            self.label.config(text="Neutral", bg="green")

    def start(self) -> None:
        """ウィンドウのメインループを開始します（ブロッキング動作）。"""
        self.root.mainloop()
