#!/usr/bin/python3

import cv2
import numpy as np
import io
import picamera

stream = io.BytesIO()
camera = picamera.PiCamera()
camera.resolution = (256, 256)

camera.hflip = True
camera.vflip = True

def saltpepper(img):
    for y in range(256):
        for x in range(256):
            if np.random.rand() < 0.01:
                img[y, x] = random_pixcel()
    return img

def random_pixcel(): 
    r = 0
    g = 0
    b = 0
    if np.random.rand() > 0.5:
        r = 255
    if np.random.rand() > 0.5:
        g = 255
    if np.random.rand() > 0.5:
        b = 255
    return [r, g, b]

while(True):
    camera.capture(stream, format="jpeg")
    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
    stream.seek(0)
    
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = img_hsv[:, :, 0]
    s = img_hsv[:, :, 1]
    v = img_hsv[:, :, 2]

    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h > 30) & (h >85)) & (s > 128)] = 255

    contours, _ = cv2.findCoutours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (192, 192, 192), 2)
    
    if(

    cv2.imshow("counter area", img)
    if cv2.waitKey(10) & 0xFF == ord(" "):
       break

cv2.imwrite("caputureImage.jpg", img)
cv2.destroyAllWindows()