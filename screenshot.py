# client/screenshot.py
import pyautogui
import base64
from io import BytesIO

def take_screenshot():
    image = pyautogui.screenshot()
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()
