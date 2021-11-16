#!/usr/bin/python3
import io

import cv2
import numpy as np
import picamera

# 各種設定

# ioライブラリからのio.BytesIOオブジェクトを生成
stream = io.BytesIO()
camera = picamera.PiCamera()
# 領域のサイズを設定
camera.resolution = (256, 256)

# 上下方向・左右方向の反転への設定
camera.hflip = True
camera.vflip = True

# ゴマ塩フィルタ
def saltpepper(img):
    # y,xを走査
    for y in range(256):
        for x in range(256):
            # 乱数（0から1）が0.01より小さければ
            if np.random.rand() < 0.01:
                # ランダムな色のピクセルを設定
                img[y, x] = random_pixcel()
    return img

# ランダムな色のピクセルを設定する関数
def random_pixcel(): 
    # r, g, bそれぞれに対して、二分の一の確率で0か255を設定
    r = 0
    g = 0
    b = 0
    if np.random.rand() > 0.5:
        r = 255
    if np.random.rand() > 0.5:
        g = 255
    if np.random.rand() > 0.5:
        b = 255
    # ランダムな色を持つ配列として返す
    # rgbとして返しているが、それぞれに対してランダムで色を決めているので、順番は問題ではない
    return [r, g, b]

while(True):
    # カメラから画像を取得
    camera.capture(stream, format="jpeg")
    # カメラから取得した画像をnumpyの配列として宣言
    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
    stream.seek(0)
    
    # カラー画像として読み込み
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    # hsv形式の画像にする
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = img_hsv[:, :, 0]
    s = img_hsv[:, :, 1]
    v = img_hsv[:, :, 2]

    # 0で初期化したマスク画像を生成
    mask = np.zeros(h.shape, dtype=np.uint8)
    # 各画素に対し条件を満たしたら255を代入
    mask[((h > 30) & (h >85)) & (s > 128)] = 255

    contours, _ = cv2.findCoutours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (192, 192, 192), 2)
    
    if(

    cv2.imshow("counter area", img)
    if cv2.waitKey(10) & 0xFF == ord(" "):
       break

cv2.imwrite("caputureImage.jpg", img)
cv2.destroyAllWindows()
