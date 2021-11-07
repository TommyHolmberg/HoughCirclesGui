import cv2, imutils
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import sys
import numpy as np
import mimetypes





class VideoStream(qtc.QThread):
  ImageUpdate = qtc.pyqtSignal(object)

  def run(self):
    self.play()

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    count = 0
    mimetypes.init()


  def setFile(self, filepath):
    self.filepath = filepath
    self.mime = self.getMime(self.filepath);


  def play(self):
    self.Playing = True
    if self.filepath:
      while self.Playing:
        self.ImageUpdate.emit(self.getImage())



  def getImage(self):
    if self.mime in ['video']:
      capture = cv2.VideoCapture(self.filepath)
      success, image = capture.read()
    else:
      image = cv2.imread(self.filepath, cv2.IMREAD_UNCHANGED)

    return image

  def stop(self):
      self.Playing = False

  def getMime(self, file):
    mimestart = mimetypes.guess_type(file)[0]

    if mimestart != None:
      mimestart = mimestart.split('/')[0]

    return mimestart
