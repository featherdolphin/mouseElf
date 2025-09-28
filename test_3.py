import time
import pyautogui
import threading
import queue  # 1. 匯入我們新的訂單軌道工具
from pynput import mouse

# --- 全域變數 ---
# 建立一個「開關」，用來告訴廚師們是否該下班了
keep_running = True
# 建立一個共享的訂單軌道 (任務佇列)
task_queue = queue.Queue()

# --- 函式定義 ---

# 「廚師」的工作邏輯：從佇列中取餐點來做
def worker():
    global keep_running
    print("一位工作者 (Worker) 已上線，等待任務...")
    
    # 只要還沒下班，就持續工作
    while keep_running:
        try:
            # 嘗試從訂單軌道上取下一項任務，最多等待 1 秒
            # 如果 1 秒內沒新任務，它會拋出 queue.Empty 錯誤
            x, y = task_queue.get(timeout=1)
            
            # --- 執行任務 ---
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            print(f"工作者 {threading.current_thread().name} 已點擊 ({x}, {y})")
            
            # 告訴佇列：這項任務我已經完成了
            task_queue.task_done()
            time.sleep(1)
            # --- 任務結束 ---

        except queue.Empty:
            # 如果訂單軌道是空的，就再回到迴圈的開頭檢查一次是否該下班
            continue
            
    print(f"工作者 {threading.current_thread().name} 已下班。")

# 滑鼠監聽器，用來發出「全體下班」的指令
def on_click(x, y, button, pressed):
    global keep_running
    if pressed and button == mouse.Button.middle:
        print('偵測到中鍵點擊，通知所有工作者準備下班...')
        keep_running = False
        return False

# --- 主程式開始 (老闆的角色) ---

# 1. 生產者：讀取檔案，把所有任務(座標)放進訂單軌道
try:
    with open('click_point_list.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            task = (int(parts[0]), int(parts[1]))
            task_queue.put(task) # 將任務放入佇列
except FileNotFoundError:
    print("錯誤：找不到 click_point_list.txt 檔案！")
    exit()

print(f"成功將 {task_queue.qsize()} 個任務放入佇列。")
print("程式將在 10 秒後啟動。點擊滑鼠中鍵可隨時停止。")
time.sleep(10)

# 2. 建立並啟動我們的「廚師」(Worker 執行緒)
#    - target=worker 代表交給他做的任務
#    - daemon=True 代表如果主程式結束了，他也會跟著結束
worker_thread = threading.Thread(target=worker, daemon=True, name="Worker-1")
worker_thread.start()

# 3. 啟動滑鼠監聽器，專心等待中鍵點擊
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

print("老闆已下達停止指令，等待所有任務完成...")
# task_queue.join() # 如果你希望確保所有任務都完成才結束，可以取消這行的註解

print("所有任務完成！")