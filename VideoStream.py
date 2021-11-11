import cv2, imutils
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import sys
import numpy as np
import mimetypes
import os
import glob



class VideoStream(qtc.QThread):
  ImageUpdate = qtc.pyqtSignal(object)
  FinishedImagesInFolder = qtc.pyqtSignal(object)
  FinishedPlaying = qtc.pyqtSignal()
  def run(self):
    self.play()

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    count = 0
    mimetypes.init()


  def setFile(self, filepath):
    self.filepath = filepath
    self.mime = self.getMime(self.filepath);
    self.isFile = os.path.isfile(self.filepath)
    self.isDirectory = os.path.isdir(self.filepath)
    if self.isDirectory:
      self.addTrailingSlashIfMissing();


  def play(self):
    self.Playing = True
    if self.filepath:
      if self.isFile:
        while self.Playing:
          self.sendImage()
      elif self.isDirectory:
        self.playDir()
    self.FinishedPlaying.emit()

  def playDir(self):
    ext = ['png', 'jpg', 'jpeg', 'gif', 'bmp']  # Add image formats here
    files = []
    [files.extend(glob.glob(self.filepath + '*.' + e)) for e in ext]
    for file in files:
      self.filepath = file
      self.sendImage()

    self.FinishedImagesInFolder.emit(files)

  def sendImage(self):
    image = self.getImage()
    if type(image) != type(None):
      self.ImageUpdate.emit(image)

  def addTrailingSlashIfMissing(self):
    self.filepath = os.path.join(self.filepath, '')



  def getImage(self):
    try:
      if self.mime in ['video']:
        capture = cv2.VideoCapture(self.filepath)
        success, image = capture.read()
      else:
        image = cv2.imread(self.filepath, cv2.IMREAD_UNCHANGED)

      if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    except:
      image = None

    return image

  def stop(self):
      self.Playing = False

  def getMime(self, file):
    mimestart = mimetypes.guess_type(file)[0]

    if mimestart != None:
      mimestart = mimestart.split('/')[0]

    return mimestart
