import cv2
from ImProcess import contrast, apply_brightness_contrast, withinRange
import numpy as np


vidcap = cv2.VideoCapture('test_move_around_1.mp4')

success,image = vidcap.read()
count = 0
window_name = 'video'
window_name2 = 'proc'
while success:
  #cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
  #image_gray = image.copy();
  output = image.copy()


  contrastimg = apply_brightness_contrast(output, 0, 70)
  cv2.imshow(window_name2, image)
  gray = cv2.cvtColor(contrastimg, cv2.COLOR_BGR2GRAY);

  circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 1)

  # ensure at least some circles were found
  if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")

    if len(circles) > 0:
      circles = circles[np.argsort(circles[:, 2])]
      first_circle = circles[0];
      circles = np.delete(circles, 0, 0)
      x0,y0,r0 = first_circle;

    # loop over the (x, y) coordinates and radius of the circles

    for (x, y, r) in circles:
      # draw the circle in the output image, then draw a rectangle
      # corresponding to the center of the circle
      closeness = 3
      xWithin = withinRange(x0, x, closeness)
      yWithin = withinRange(y0, y, closeness)
      cSize = 2
      if xWithin and yWithin:
        cv2.circle(output, (x0, y0), r0, (0, 255, 0), 1)
        cv2.rectangle(output, (x0 - cSize, y0 - cSize), (x0 + cSize, y0 + cSize), (0, 128, 255), -1)
        cv2.circle(output, (x, y), r, (0, 255, 0), 1)
        cv2.rectangle(output, (x - cSize, y - cSize), (x + cSize, y + cSize), (0, 128, 255), -1)
    # show the output image
    print("shape", image.shape)
    cv2.imshow("output", np.hstack([image, output]))
    cv2.waitKey(50)
  success,image = vidcap.read()

  #print('Read a new frame: ', success)
  count += 1