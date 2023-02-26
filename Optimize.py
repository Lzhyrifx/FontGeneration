import numpy as np
import cv2 as cv
import time


class Sketcher:
    def __init__(self, windowname, dests, colors_func):
        self.prev_point = None
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv.namedWindow(self.windowname, 0)
        cv.imshow(self.windowname, self.dests[0])

    def on_mouse(self, event, x, y, flags, _):
        point = (x, y)
        if event == cv.EVENT_LBUTTONDOWN:
            self.prev_point = point
        elif event == cv.EVENT_LBUTTONUP:
            self.prev_point = None
        if self.prev_point and flags & cv.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv.line(dst, self.prev_point, point, color, 30)
        self.dirty = True
        self.prev_point = point
        self.show()


def main(x):
    img = cv.imread("FontImage/OriginalSingleWord/Image" + x + ".jpg", cv.IMREAD_COLOR)
    if img is None:
        pass
        return
    img_mask = img.copy()
    inpaintmask = np.zeros(img.shape[:2], np.uint8)
    Sketcher('image', [img_mask, inpaintmask], lambda: ((255, 255, 255), 255))
    while True:
        ch = cv.waitKey()
        if ch == 27:
            break
        if ch == ord('t'):
            t1 = time.time()
            res = cv.inpaint(src=img_mask, inpaintMask=inpaintmask, inpaintRadius=3, flags=cv.INPAINT_TELEA)
            t2 = time.time()
            cv.imshow('FMM', res)
            cv.imwrite('FontImage/IndividualCharacter/Image{}.jpg'.format(x), res)
        break


for i in range(0, 10000):
    main(f"{i}")
    cv.destroyAllWindows()
