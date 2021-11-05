import cv2, imutils
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import sys

class VideoStream(qtc.QThread):
  ImageUpdate = qtc.pyqtSignal(qtg.QImage)

  def run(self):
    self.play()

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    count = 0


  def setFile(self, filepath):
    self.filepath = filepath


  def play(self):
    self.Playing = True
    if self.filepath:
      capture = cv2.VideoCapture(self.filepath)
      success, image = capture.read()
      window_name = 'video'
      count = 0
      while self.Playing:
        self.tmp = image
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        FlippedImage = cv2.flip(frame, 1)
        conertToQTFormat = qtg.QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], qtg.QImage.Format_RGB888)
        qtImage = conertToQTFormat.scaled(640, 480, qtc.Qt.KeepAspectRatio)
        self.ImageUpdate.emit(qtImage)
        success, newimage = capture.read()
        if success:
          image = newimage
          print('Read a new frame: ', success)
        count += 1

  def stop(self):
      self.Playing = False
