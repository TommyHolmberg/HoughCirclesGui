import cv2
from PyQt5 import QtCore
from PyQt5.QtGui import QImage

class ImageFormat:
    def ToQtPixmap(self, image):
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #FlippedImage = cv2.flip(frame, 1)
        convertToQTFormat = QImage(frame.data, frame.shape[1], frame.shape[0],
                                      QImage.Format_RGB888)
        qtImage = convertToQTFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
        return qtImage