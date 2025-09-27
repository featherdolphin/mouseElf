import pyautogui
import time

print("程式已啟動，請移動滑鼠。按下 Ctrl-C 即可結束。")

try:
    while True:
        # 取得並印出目前的滑鼠座標
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\n程式已結束。')