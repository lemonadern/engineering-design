#!/usr/bin/python3
import cv2
import numpy as np


# 初期化された（何もない）画像を生成する
def initImg(width, height, red, green, blue):
    imageArray = np.zeros((height, width, 3), np.uint8)
    imageArray[0:height, 0:width] = [blue, green, red]
    return imageArray


# マウスのイベントを受け取る関数
def mouse_event(event, x, y, flags, param):
    global lenna, img
    # マウスの左ボタンが押されたとき
    if event == cv2.EVENT_LBUTTONDOWN:
        # 元の画像(Lenna.jpg)と同じサイズの画像を生成
        canvas = initImg(lenna.shape[0], lenna.shape[1], 0, 0, 0)
        # クリックされた座標の左上の領域をスライスし、その部分を画像lennaで置き換える
        canvas[0:y, 0:x] = lenna[0:y, 0:x]
        # 置き換えたものを、表示画像として代入
        img = canvas


# 元画像を読み込む
lenna = cv2.imread("./Lenna.jpg")
# 表示画像（img）を、元画像と全く同じものとして初期化
img = lenna

cv2.namedWindow("triming")
cv2.setMouseCallback("triming", mouse_event)

while True:
    # 表示画像(img)を表示
    cv2.imshow("triming", img)
    # スペースの入力でイベント待ちのループを抜ける
    if cv2.waitKey(10) & 0xFF == ord(" "):
        break
# 全てのウィンドウを破壊
cv2.destroyAllWindows()
