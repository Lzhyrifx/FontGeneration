import os
import cv2
import numpy as np

img = cv2.imread("FontImage/Multiword/Image1.jpg")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
threshold_img = cv2.threshold(gray_img, 60, 40, cv2.THRESH_BINARY_INV)[1]

sp = img.shape
t = 0
gray_value_x = np.sum(threshold_img // 255, axis=1)
text_rect_x = []
for i in range(len(gray_value_x)):
    if gray_value_x[i] > 10:
        if not text_rect_x or i - text_rect_x[-1][1] > 5:
            text_rect_x.append([i - 1, i + 1])
        else:
            text_rect_x[-1][1] = i + 1

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 3))
dilate_img = cv2.dilate(threshold_img, kernel)

text_rect = []
for rect in text_rect_x:
    cropImg = dilate_img[rect[0]:rect[1], 0:sp[1]]
    gray_value_y = np.sum(cropImg // 255, axis=0)
    text_rect_y = []
    for i in range(len(gray_value_y)):
        if gray_value_y[i] > 2:
            if not text_rect_y or i - text_rect_y[-1][1] > 5:
                text_rect_y.append([i - 1, i + 1])
            else:
                text_rect_y[-1][1] = i + 1
    for rect_y in text_rect_y:
        text_rect.append([rect[0], rect[1], rect_y[0], rect_y[1]])
        a = abs(rect[0])
        b = abs(rect[1])
        c = abs(rect_y[0])
        d = abs(rect_y[1])
        cropImg_rect = img[a:b, c:d]

        t += 1
        filename = f"FontImage/Temp/Image{t}.jpg"
        while os.path.exists(filename):
            t += 1
            filename = f"FontImage/Temp/Image{t}.jpg"
        cv2.imwrite(filename, cropImg_rect)

for rect in text_rect:
    img = cv2.rectangle(img, (rect[2], rect[0]), (rect[3], rect[1]), (255, 0, 0), thickness=2)

cv2.namedWindow("Image", 0)
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
