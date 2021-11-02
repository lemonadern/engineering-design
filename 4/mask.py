#!/usr/bin/python3
import io

import cv2
import numpy as np
import picamera

stream = io.BytesIO()
camera = picamera.PiCamera()
camera.resolution = (256, 256)

#  上下左右反転の設定
camera.hflip = True
camera.vflip = True

# 線の色を設定
lineColor = (0, 255, 0)
# 線の太さを設定
lineWidth = 2

while True:
    # カメラ画像を取得
    camera.capture(stream, format="jpeg")
    # 画像をnumpy配列に変換
    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
    stream.seek(0)

    # カラー画像として読み込み
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    # hsv画像に変換
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = img_hsv[:, :, 0]
    s = img_hsv[:, :, 1]
    v = img_hsv[:, :, 2]

    # mask画像を生成
    mask = np.zeros(h.shape, dtype=np.uint8)
    # 画像の各ピクセルに対して、緑色ならマスク画像に255を設定する
    mask[((h > 30) & (h < 85)) & (s > 128)] = 255

    # findContoursで輪郭を検出
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # imgに対して(192,192,192)の色・幅２の線で輪郭を描く
    cv2.drawContours(img, contours, -1, (192, 192, 192), 2)
    # 配列contoursが空でなければ（ReferenceErrorを防ぐ）
    if len(contours) != 0:
        # 輪郭とその中身の面積を初期化
        mContour = contours[0]
        maxArea = 0.0
        # contoursの中で最大の面積のものを求める
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > maxArea:
                maxArea = area
                mContour = contour
        # 最大の面積のものに対して、指定したlineColor, lineWidthで輪郭線を引く
        cv2.drawContours(img, [mContour], 0, lineColor, lineWidth)
        # fitLineを用いて、領域に合うような直線の成分を取得
        # 該当領域のそれぞれの点からの距離が最小になるような直線を示す成分を返す
        vx, vy, x0, y0 = cv2.fitLine(mContour, cv2.DIST_L2, 0, 0.01, 0.01)
        # x1は画像の左端、x2は画像の右端の座標
        x1 = 0
        x2 = 256
        # vxが非常に小さい値で無い場合
        # ZeroDivisionErrorの防止と、y1, y2がcのlong intに収まる範囲の値にするための措置
        if vx >= 0.00001:
            # 直線の式から求められるy1, y2の値
            y1 = (vy / vx) * (x1 - x0) + y0
            y2 = (vy / vx) * (x2 - x0) + y0
            # 求めた座標を利用して直線を引く
            cv2.line(img, (x1, y1), (x2, y2), lineColor, lineWidth)
    # imgを表示
    cv2.imshow("contour image", img)
    if cv2.waitKey(10) & 0xFF == ord(" "):
        break

cv2.imwrite("caputureImage.jpg", img)
cv2.destroyAllWindows()
