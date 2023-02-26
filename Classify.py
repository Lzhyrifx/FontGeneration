import cv2
import os


for filename in os.listdir('FontImage/Temp'):
    # 读取图像
    img = cv2.imread(os.path.join('FontImage/Temp', filename))

    # 将图像转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 使用Canny算法进行边缘检测
    edges = cv2.Canny(gray, 50, 150)

    # 查找轮廓
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历轮廓并计算形状特征
    is_text = False
    for contour in contours:
        # 计算轮廓面积
        area = cv2.contourArea(contour)

        # 计算轮廓周长
        perimeter = cv2.arcLength(contour, True)

        # 计算轮廓凸包
        hull = cv2.convexHull(contour)

        # 根据形状特征进行判断
        if area > 2000 and perimeter > 50 and len(hull) > 3:
            is_text = True
            break

    # 根据处理结果保存到不同的文件夹中
    if is_text:
        cv2.imwrite(os.path.join('FontImage/Process', filename), img)
