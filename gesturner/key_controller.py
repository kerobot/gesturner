"""キーボード入力を送信するユーティリティモジュール。

PyAutoGUIを使用して各種キー入力をシミュレートします。
"""

import pyautogui


def send_left_key() -> None:
    """左矢印キーを送信します。"""
    pyautogui.press("left")


def send_right_key() -> None:
    """右矢印キーを送信します。"""
    pyautogui.press("right")


def send_up_key() -> None:
    """上矢印キーを送信します。"""
    pyautogui.press("up")


def send_down_key() -> None:
    """下矢印キーを送信します。"""
    pyautogui.press("down")


def send_enter_key() -> None:
    """Enterキーを送信します。"""
    pyautogui.press("enter")


def send_escape_key() -> None:
    """Escapeキーを送信します。"""
    pyautogui.press("escape")


def send_space_key() -> None:
    """スペースキーを送信します。"""
    pyautogui.press("space")


def send_tab_key() -> None:
    """Tabキーを送信します。"""
    pyautogui.press("tab")


def send_backspace_key() -> None:
    """Backspaceキーを送信します。"""
    pyautogui.press("backspace")
