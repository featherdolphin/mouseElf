from pynput import mouse

def on_click(x, y, button, pressed):
    # 當按鍵被按下時
    if pressed:
        print(f'在 ({x}, {y}) 位置按下了 {button}')

        # 檢查按下的按鈕是不是滑鼠中鍵
        if button == mouse.Button.middle:
            print('偵測到中鍵點擊，程式結束。')
            # 回傳 False 來停止監聽器
            return False

# 建立一個監聽器
with mouse.Listener(on_click=on_click) as listener:
    print("程式已啟動。點擊滑鼠左鍵記錄座標，點擊中鍵結束。")
    listener.join()