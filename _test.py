import pyautogui
import time

# 給你 3 秒鐘的時間切換視窗或準備
print("程式即將在 3 秒後移動滑鼠...")
time.sleep(3)

# 將滑鼠在 2 秒內，平順地移動到 (500, 500) 的位置
pyautogui.moveTo(500, 500, duration=2)

print("滑鼠移動完成！")