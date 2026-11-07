import os
import ctypes
import cv2
import keyboard
import mss
import numpy as np
import win32api
import win32con
import win32gui

try:
  ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
  pass

print("Script loaded. Press F8 to start.")
keyboard.wait("f8")
print("Activated!")

keyboard.add_hotkey("esc", lambda: os._exit(0))


def get_game_box():
  hwnd = win32gui.GetForegroundWindow()
  rect = win32gui.GetClientRect(hwnd)
  left, top = win32gui.ClientToScreen(hwnd, (0, 0))
  return {"left": left, "top": top, "width": rect[2], "height": rect[3]}


with mss.mss() as sct:
  while True:
    box = get_game_box()
    sct_img = sct.grab(box)
    frame = cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGRA2BGR)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, np.array([0, 150, 150]), np.array([10, 255, 255]))
    mask2 = cv2.inRange(
        hsv, np.array([170, 150, 150]), np.array([180, 255, 255])
    )
    mask = mask1 | mask2

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:
      c = max(contours, key=cv2.contourArea)
      ((x, y), radius) = cv2.minEnclosingCircle(c)

      if 10 < radius < 50:
        center_x = box["width"] / 2
        center_y = box["height"] / 2

        dx = int(x - center_x)
        dy = int(y - center_y)
        distance = (dx * dx + dy * dy) ** 0.5

        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)

        if distance < 40:
          win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
          win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    if keyboard.is_pressed("esc"):
      break