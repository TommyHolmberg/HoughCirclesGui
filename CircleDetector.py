import cv2
import numpy as np
from ImgProcess import ImgProcess


class CircleDetector:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ImgProcess = ImgProcess()
        self.reset()

    def reset(self):
        self.circlesRaw = []
        self.circles = []
        self.accCircles = []
        self.accCirclesRaw = []

    def detect(self, image, acc_res = 1.2, dist = 1, param1 = 50, param2 = 2000, minRad = 0, maxRad = 0):
        output = image.copy()
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        self.circlesRaw = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, acc_res, dist, param1=param1, param2=param2, minRadius=minRad, maxRadius=maxRad)


        if self.circlesRaw is not None:
            self.accCirclesRaw.append(self.circlesRaw[0])
            # convert the (x, y) coordinates and radius of the circles to integers
            self.circles = np.round(self.circlesRaw[0, :]).astype("int")
            self.accCircles.append(self.circles)
            # loop over the (x, y) coordinates and radius of the circles

            for (x, y, r) in self.circles :
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        return output
