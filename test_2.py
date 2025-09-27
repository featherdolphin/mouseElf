import pyautogui
import time

# 先建立一個空的清單，用來存放從檔案讀取的座標
click_point_list = []

# --- 這是我們新增的區塊 ---
try:
    # 'r' 代表「讀取」這個檔案
    with open('click_point_list.txt', 'r') as f:
        # 一行一行地讀取檔案內容
        for line in f:
            # 移除每行前後可能有的空白或換行符號
            clean_line = line.strip()
            # 用逗號 , 把字串切開，變成像 ['500', '500'] 這樣的清單
            parts = clean_line.split(',')

            # int把切開的兩個部分，從str「文字」轉換成「數字」
            x = int(parts[0])
            y = int(parts[1])

            # 最後，把這組座標加到我們的 click_point_list.txt 裡
            click_point_list.append((x, y))
# 防呆機制
except FileNotFoundError:
    print("錯誤：找不到 click_point_list.txt 檔案！請確認檔案存在於同一個資料夾。")
    exit()
# --- 新增區塊結束 ---


print(f"成功從檔案載入 {len(click_point_list.txt)} 個座標。")
print("程式將在 3 秒後，開始執行連續點擊...")
time.sleep(3)

# 
for x, y in click_point_list:
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.click()
    print(f"已在 ({x}, {y}) 執行點擊。")
    time.sleep(1)

print("所有任務完成！")