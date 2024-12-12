
import pyautogui

# Lấy cửa sổ đang hoạt động trên cùng
def minimize_window():
    window = pyautogui.getActiveWindow()
    window.minimize()
def close_window():
    pyautogui.hotkey('alt', 'f4')
def maximize_window():
    window = pyautogui.getActiveWindow()
    window.maximize()
