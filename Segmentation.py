import os

import cv2

input_folder = 'FontImage/Process'
output_folder = 'FontImage/OriginalSingleWord'

size = (128, 128)
for filename in os.listdir(input_folder):
    img = cv2.imread(os.path.join(input_folder, filename))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = img[y:y + h, x:x + w]

        if roi.shape[0] >= size[0] and roi.shape[1] >= size[1]:
            roi = cv2.resize(roi, size, interpolation=cv2.INTER_AREA)
            cv2.imwrite('FontImage/OriginalSingleWord/Image{}.jpg'.format(x), roi)
