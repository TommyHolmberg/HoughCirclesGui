import cv2
import numpy as np
from ImgProcess import ImgProcess


class CircleDetector:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ImgProcess = ImgProcess()

    def detect(self, image, acc_res = 1.2, dist = 1, param1 = 50, param2 = 2000, minRad = 0, maxRad = 0):
        output = image.copy()
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, acc_res, dist, param1=param1, param2=param2, minRadius=minRad, maxRadius=maxRad)
        
        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            """
            if len(circles) > 0:
                circles = circles[np.argsort(circles[:, 2])]
                first_circle = circles[0];
                circles = np.delete(circles, 0, 0)
                x0, y0, r0 = first_circle;
            """
            # loop over the (x, y) coordinates and radius of the circles

            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                """
                closeness = 3
                xWithin = self.ImgProcess.withinRange(x0, x, closeness)
                yWithin = self.ImgProcess.withinRange(y0, y, closeness)
                cSize = 2
                if xWithin and yWithin:
                
                cSize = 2
                cv2.circle(output, (x0, y0), r0, (255, 255, 0), 1)
                cv2.rectangle(output, (x0 - cSize, y0 - cSize), (x0 + cSize, y0 + cSize), (0, 128, 255), -1)
                cv2.circle(output, (x, y), r, (0, 255, 0), 1)
                cv2.rectangle(output, (x - cSize, y - cSize), (x + cSize, y + cSize), (0, 128, 255), -1)
                """
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
      #  cv2.imshow("output", np.hstack([image, output]))
       # cv2.imshow("gray", gray)
       # cv2.waitKey(0)
        return output
