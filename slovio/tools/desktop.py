try:
    import pyautogui
    GUI_ENABLED = True
except Exception:
    GUI_ENABLED = False

try:
    import pyperclip
    CLIP_ENABLED = True
except Exception:
    CLIP_ENABLED = False

import subprocess
import platform
try:
    from PIL import ImageGrab
    IMG_ENABLED = True
except Exception:
    IMG_ENABLED = False
import base64
from io import BytesIO

def take_screenshot():
    if not IMG_ENABLED: return ""
    try:
        img = ImageGrab.grab()
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception:
        return ""

def _gui_op(func_name, *args):
    if not GUI_ENABLED: return f"Mock {func_name} (GUI disabled)"
    getattr(pyautogui, func_name)(*args)
    return f"Executed {func_name}"

def click(x, y): return _gui_op("click", x, y)
def double_click(x, y): return _gui_op("doubleClick", x, y)
def right_click(x, y): return _gui_op("rightClick", x, y)
def type_text(text): return _gui_op("typewrite", text)
def press_key(key): return _gui_op("press", key)
def hotkey(*keys): return _gui_op("hotkey", *keys)
def scroll(x, y, amount):
    if not GUI_ENABLED: return f"Mock scroll (GUI disabled)"
    pyautogui.moveTo(x, y)
    pyautogui.scroll(amount)
    return f"Scrolled {amount} at {x}, {y}"

def open_app(app_name):
    os_name = platform.system()
    try:
        if os_name == "Windows":
            subprocess.Popen(["start", app_name], shell=True)
        elif os_name == "Darwin":
            subprocess.Popen(["open", "-a", app_name])
        else:
            subprocess.Popen([app_name])
        return f"Opened {app_name}"
    except Exception as e:
        return str(e)

def get_clipboard():
    return pyperclip.paste()

def set_clipboard(text):
    pyperclip.copy(text)
    return "Clipboard updated"
