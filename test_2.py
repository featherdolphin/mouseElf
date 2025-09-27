import pyautogui
import time
import threading
from pynput import mouse

# --- 全域變數 ---
# 建立一個清單，用來存放座標
click_point_list = []
# 建立一個「開關」，用來告訴背景的小幫手是否該繼續工作
keep_running = True

# --- 函式定義 ---

# 這是我們交給「背景小幫手」執行的任務
def move_mouse_in_background():
    global keep_running
    print("背景移動任務已啟動...")
    
    # 迴圈會不斷檢查「開關」是不是還開著
    while keep_running:
        # 依序移動到清單中的每一個點
        for x, y in click_point_list:
            # 在移動前，再次檢查開關，確保可以隨時中斷
            if not keep_running:
                break
            
            pyautogui.moveTo(x, y, duration=0.5)
            print(f"已將滑鼠移動到 ({x}, {y})。")
            time.sleep(1)
        
        # 如果只想跑一次就結束，可以在這裡加上 break
        # break 
        
    print("背景移動任務已停止。")

# 這是我們的滑鼠監聽器要做的事
def on_click(x, y, button, pressed):
    global keep_running
    if pressed and button == mouse.Button.middle:
        print('偵測到中鍵點擊，準備結束程式...')
        # 把「開關」關掉
        keep_running = False
        # 讓監聽器自己也停止
        return False

# --- 主程式開始 ---

# 1. 從檔案讀取座標 (這部分完全一樣)
try:
    with open('click_point_list.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            click_point_list.append((int(parts[0]), int(parts[1])))
except FileNotFoundError:
    print("錯誤：找不到 click_point_list.txt 檔案！")
    exit()

print(f"成功載入 {len(click_point_list)} 個座標。")
print("程式將在 10 秒後啟動。點擊滑鼠中鍵可隨時停止。")
time.sleep(10)

# 2. 建立並啟動我們的背景小幫手 (執行緒)
#    - target=move_mouse_in_background 代表要交給他做的任務
mouse_thread = threading.Thread(target=move_mouse_in_background)
mouse_thread.start()

# 3. 啟動滑鼠監聽器，它會佔據主程式，專心等待中鍵點擊
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

print("所有任務完成！")