#!/usr/bin/python3
import cv2
import numpy as np


# 画像を初期化
def initImg(width, height, red, green, blue):
    imageArray = np.zeros((height, width, 3), np.uint8)
    imageArray[0:height, 0:width] = [blue, green, red]
    return imageArray


# マウスのイベントを受け取る関数
def mouse_event(event, x, y, flags, param):
    global canvas, px, py, drawing, isBlack, isBold, lineColor, lineWidth

    # 右ボタンがクリックされたとき
    if event == cv2.EVENT_RBUTTONDOWN:
        # 初期化画像で上書き
        canvas = initImg(480, 480, 255, 255, 255)
    # マウスが動いたとき
    elif event == cv2.EVENT_MOUSEMOVE:
        # drawingならば線を書く
        if drawing:
            cv2.line(canvas, (px, py), (x, y), lineColor, lineWidth)
            px = x
            py = y
    # 左ボタンが押されたとき
    elif event == cv2.EVENT_LBUTTONDOWN:
        # drawingフラグをTrueにする
        drawing = True
        px = x
        py = y
    # 左ボタンが上がったとき
    elif event == cv2.EVENT_LBUTTONUP:
        # drawingフラグをFalseにする
        drawing = False
    # 左ボタンがダブルクリックされたとき
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        # 線の色を変更する
        if isBlack:
            lineColor = (0, 0, 0)
        else:
            lineColor = (0, 255, 0)
        # 線の色を保持するフラグを反転する
        isBlack = not isBlack
    # 中央ボタンが押されたとき
    elif event == cv2.EVENT_MBUTTONDOWN:
        # 先の太さを変更する
        if isBold:
            lineWidth = 10
        else:
            lineWidth = 2
        # 先の太さを保持するフラグを反転する
        isBold = not isBold


# 各状態の初期値を設定する
drawing = False  # 線は描画されない
isBlack = True  # 線は黒色
isBold = False  # 細い線
lineColor = (0, 0, 0)
lineWidth = 2
px = -1
py = -1

cv2.namedWindow("paint")

# 白い画像で画面を初期化
canvas = initImg(480, 480, 255, 255, 255)

cv2.setMouseCallback("paint", mouse_event)

while True:
    cv2.imshow("paint", canvas)
    # スペースの入力でイベント待ちのループを抜ける
    if cv2.waitKey(10) & 0xFF == ord(" "):
        break
# 全てのウィンドウを破壊
cv2.destroyAllWindows()
