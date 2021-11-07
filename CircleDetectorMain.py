from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from VideoStream import VideoStream
from ImageFormat import ImageFormat
from CircleDetector import CircleDetector
from ImgProcess import ImgProcess
from houghCirclesGUI import Ui_MainWindow
import cv2, imutils
from enum import Enum
class NoValue(Enum):
    def __repr__(self):
         return '<%s.%s>' % (self.__class__.__name__, self.name)
class StateSettings(NoValue):
    radius = "radius"
    mindist = "mindist"
    contrast = "contrast"
    param1 = "param1"
    param2 = "param2"
    minRad = "minRad"
    maxRad = "maxRad"


class MainWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setupUi()
        self.connectUI()

        self.ImgProcess = ImgProcess()
        self.CircleDetector = CircleDetector()
        self.ImageFormat = ImageFormat()

        self.imageCapture = VideoStream()

        #self.ui.connect(self.imageCapture, self.imageCapture.ImageUpdate, self.ImageUpdateSlot)

        self.imageCapture.ImageUpdate.connect(self.ImageUpdateSlot, qtc.Qt.DirectConnection)
        self.setDefaultValues()

        self.loadState()

    def setupUi(self):
        self.ui = Ui_MainWindow();
        self.ui.setupUi(self)
        self.statevars = [
            self.ui.radiusSpinBox,
            self.ui.minDistSpinBox,
            self.ui.contrastSpinBox,
            self.ui.param1SpinBox,
            self.ui.param2SpinBox,
            self.ui.minRadSpinBox,
            self.ui.maxRadSpinBox
        ]

    def loadState(self):
        settings = qtc.QSettings('CircleDetector', 'CircleDetectorSettings')
        settingslist = list(StateSettings)
        for i in range(len(settingslist)):
            valType = settings.value(settingslist[i].value + "type")
            valStr = settings.value(settingslist[i].value)

            if (valStr != None and valType != None):
                val = valType(valStr)
                self.statevars[i].setValue(val)



    def saveState(self):
        settings = qtc.QSettings('CircleDetector', 'CircleDetectorSettings')
        settingslist = list(StateSettings)
        for i in range(len(settingslist)):
            val = self.statevars[i].value()
            settings.setValue(settingslist[i].value, val)
            settings.setValue(settingslist[i].value + "type", type(val))


    def connectUI(self):
        self.connectSliders()
        self.connectSpinBox()
        self.connectBtns()


    def connectSliders(self):
        self.ui.radiusSlider.valueChanged.connect(self.radiusSliderChange)

    def connectSpinBox(self):
        self.ui.radiusSpinBox.valueChanged.connect(self.radiusSpinBoxChange)

    def connectBtns(self):
        self.ui.stopBtn.clicked.connect(self.StopVideo)
        self.ui.startBtn.clicked.connect(self.StartVideo)
        self.ui.browseFile.clicked.connect(self.loadImageFile)

    def setDefaultValues(self):
        self.framecount = 0
        self.ui.radiusSpinBox.setValue(1.2)


    def radiusSliderChange(self):
        self.radiusValue = self.ui.radiusSlider.value()/10;
        self.ui.radiusSpinBox.setValue(self.radiusValue)

    def radiusSpinBoxChange(self):
        self.radiusValue = self.ui.radiusSpinBox.value();
        self.ui.radiusSlider.setValue(self.radiusValue*10)

    def loadImageFile(self):
        self.filename = qtw.QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        if self.filename is not "":
            if (self.imageCapture.isRunning()):
                self.imageCapture.exit() #Bad practice but it's the only way to get out of HoughCircles
            self.imageCapture.setFile(self.filename)
            self.imageCapture.start()

    def ImageUpdateSlot(self, image):
        imgContrast = self.ImgProcess.apply_brightness_contrast(image, contrast=self.ui.contrastSpinBox.value())
        imgCircles = self.CircleDetector.detect(imgContrast, self.ui.radiusSpinBox.value(), self.ui.minDistSpinBox.value(), self.ui.param1SpinBox.value(), self.ui.param2SpinBox.value(), self.ui.minRadSpinBox.value(), self.ui.maxRadSpinBox.value())
        qtImage = self.ImageFormat.ToQtPixmap(imgCircles)
        self.ui.VideoFeed.setPixmap(qtg.QPixmap.fromImage(qtImage))
        self.framecount += 1
        print('Read a new frame: ',  self.framecount)
        self.imageCapture.wait(1000)

    def StopVideo(self):
        self.imageCapture.stop()

    def StartVideo(self):
        self.imageCapture.start()

    def closeEvent(self, event):
        self.saveState()

if __name__ == '__main__':
    app = qtw.QApplication([])
    mainWin = MainWindow()
    mainWin.show()
    app.exec_()