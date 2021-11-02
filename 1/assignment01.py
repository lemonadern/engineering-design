#!/usr/bin/python3
import cv2

# マウスのイベントを受け取る関数
def mouse_event(event, x, y, flags, param):
    global flag
    # 左ボタンが押されたとき
    if event == cv2.EVENT_LBUTTONDOWN:
        # 変数flagをトグルする
        flag = not flag
        
# 現在の状態を、変数flagとして保持
flag = True

# 2種の画像を読み込み
img_f = cv2.imread("./Lenna.jpg")
img_b = cv2.imread("./warai_b.png")

cv2.namedWindow("toggle")
cv2.setMouseCallback("toggle", mouse_event)

while(True):
    # flagがTrueのとき
    if flag:
        # img_fを表示する
        cv2.imshow("toggle", img_f)
    else:
        #それ以外はimg_bを表示する
        cv2.imshow("toggle", img_b)
    # スペースが入力されたら、イベント待ちのループから離脱
    if cv2.waitKey(10) & 0xFF == ord(" "):
        break
# 全てのウィンドウを破壊
cv2.destroyAllWindows()