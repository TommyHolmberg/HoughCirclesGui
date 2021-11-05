from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from VideoStream import VideoStream

from houghCirclesGUI import Ui_MainWindow
import cv2, imutils

class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.ui = Ui_MainWindow();
        self.ui.setupUi(self)

        self.ui.radiusSlider.valueChanged.connect(self.radiusChange)
        self.ui.minDistSlider.valueChanged.connect(self.minDistChange)
        self.ui.contrastSlider.valueChanged.connect(self.contrastChange)
        self.ui.browseFile.clicked.connect(self.loadImageFile)
        self.ui.stopBtn.clicked.connect(self.StopVideo)

        self.imageCapture = VideoStream()

        self.imageCapture.ImageUpdate.connect(self.ImageUpdateSlot)

        self.framecount = 0;

    def radiusChange(self):
        self.radiusValue = self.ui.radiusSlider.value();

    def minDistChange(self):
        self.minDistValue = self.ui.minDistSlider.value();

    def contrastChange(self):
        self.contrastValue = self.ui.contrastSlider.value();

    def loadImageFile(self):

        self.filename = qtw.QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        self.imageCapture.setFile(self.filename)
        self.imageCapture.start()

    def ImageUpdateSlot(self, image):
        self.ui.VideoFeed.setPixmap(qtg.QPixmap.fromImage(image))
        self.framecount += 1
        print('Read a new frame: ',  self.framecount)

    def StopVideo(self):
        self.imageCapture.Stop()

if __name__ == '__main__':
    app = qtw.QApplication([])
    mainWin = MainWindow()
    mainWin.show()
    app.exec_()