# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LabelApp.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import cv2
from mplwidget import MplWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(388, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LaneNumber = QtWidgets.QLabel(self.centralwidget)
        self.LaneNumber.setGeometry(QtCore.QRect(110, 70, 71, 20))
        self.LaneNumber.setObjectName("LaneNumber")
        self.Filename = QtWidgets.QLabel(self.centralwidget)
        self.Filename.setGeometry(QtCore.QRect(130, 0, 131, 20))
        self.Filename.setObjectName("Filename")
        self.CurrentFrame = QtWidgets.QLabel(self.centralwidget)
        self.CurrentFrame.setGeometry(QtCore.QRect(110, 110, 111, 16))
        self.CurrentFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.CurrentFrame.setObjectName("CurrentFrame")
        self.LaneNumberEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.LaneNumberEdit.setGeometry(QtCore.QRect(190, 70, 31, 20))
        self.LaneNumberEdit.setObjectName("LaneNumberEdit")
        self.SelectBtn = QtWidgets.QPushButton(self.centralwidget)
        self.SelectBtn.setGeometry(QtCore.QRect(280, 40, 71, 21))
        self.SelectBtn.setObjectName("SelectBtn")
        self.DrawBttn = QtWidgets.QPushButton(self.centralwidget)
        self.DrawBttn.setGeometry(QtCore.QRect(280, 80, 75, 23))
        self.DrawBttn.setObjectName("DrawBttn")
        self.xPoint = QtWidgets.QLabel(self.centralwidget)
        self.xPoint.setGeometry(QtCore.QRect(30, 70, 16, 16))
        self.xPoint.setObjectName("xPoint")
        self.LineLength = QtWidgets.QLabel(self.centralwidget)
        self.LineLength.setGeometry(QtCore.QRect(30, 40, 71, 16))
        self.LineLength.setObjectName("LineLength")
        self.yPoint = QtWidgets.QLabel(self.centralwidget)
        self.yPoint.setGeometry(QtCore.QRect(30, 110, 16, 16))
        self.yPoint.setObjectName("yPoint")
        self.xPointEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.xPointEdit.setGeometry(QtCore.QRect(50, 70, 31, 20))
        self.xPointEdit.setObjectName("xPointEdit")
        self.yPointEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.yPointEdit.setGeometry(QtCore.QRect(50, 100, 31, 20))
        self.yPointEdit.setObjectName("yPointEdit")
        self.LineLengthEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.LineLengthEdit.setGeometry(QtCore.QRect(100, 40, 41, 20))
        self.LineLengthEdit.setObjectName("LineLengthEdit")
        self.ImportBtn = QtWidgets.QPushButton(self.centralwidget)
        self.ImportBtn.setGeometry(QtCore.QRect(280, 150, 75, 23))
        self.ImportBtn.setObjectName("ImportBtn")
        self.MplWidget = MplWidget(self.centralwidget)
        self.MplWidget.setGeometry(QtCore.QRect(40, 190, 301, 231))
        self.MplWidget.setObjectName("MplWidget")
        self.Record = QtWidgets.QLabel(self.centralwidget)
        self.Record.setGeometry(QtCore.QRect(50, 150, 151, 16))
        self.Record.setObjectName("Record")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 388, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.LaneNumber.setText(_translate("MainWindow", "Lane Number: "))
        self.Filename.setText(_translate("MainWindow", "No File Selected"))
        self.CurrentFrame.setText(_translate("MainWindow", "Current Frame: "))
        self.SelectBtn.setText(_translate("MainWindow", "Select File"))
        self.DrawBttn.setText(_translate("MainWindow", "Draw Line"))
        self.xPoint.setText(_translate("MainWindow", "x: "))
        self.LineLength.setText(_translate("MainWindow", "Line Length: "))
        self.yPoint.setText(_translate("MainWindow", "y: "))
        self.ImportBtn.setText(_translate("MainWindow", "Import CSV"))
        self.Record.setText(_translate("MainWindow", "None"))

class Main(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.cap=None
        self.frame=None
        self.lineParams={"x":None,"y":None,"Length":None,"LaneNum":None,"CheckBox":False}
        self.FrameNum=0
        self.lastLabel=0
        self.currentFile=None
        self.csvData=[]
        self.currentData=None
        self.lastRecordedFrame=0
        
        #Buttons
        self.SelectBtn.clicked.connect(self.browse)
        self.DrawBttn.clicked.connect(self.drawLine)
        self.ImportBtn.clicked.connect(self.importFile)
        self.Record.setText("")

    def importFile(self):
        filename=self.currentFile.split('.')
        filename=filename[0]+"_"+"Lane"+self.LaneNumberEdit.text()+".csv"
        self.csvData = np.reshape(self.csvData,(-1, self.lineParams["Length"]+1))
        np.savetxt(filename,self.csvData , fmt='%d')
        self.Record.setText("Dosya oluşturuldu")

    def drawLine(self):
        errorCheck=False
        try:
            self.lineParams["x"]=int(self.xPointEdit.text())
        except:
            self.xPointEdit.setText("")
            errorCheck=True
        try:
            self.lineParams["y"]=int(self.yPointEdit.text())
        except:
            self.yPointEdit.setText("")
            errorCheck=True
        try:
            self.lineParams["Length"]=int(self.LineLengthEdit.text())
        except:
            self.LineLengthEdit.setText("")
            errorCheck=True

        if(errorCheck==False):
            x,y,l=self.getParams()
            self.lineParams["CheckBox"]=True
            img=self.frame.copy()
            img=cv2.line(img, (y,x), (y+l,x+1), (255,255,255), 1)
            self.updateImage(img)
            self.updateMtl()

    def getParams(self):
        x=self.lineParams['x']
        y=self.lineParams['y']
        l=self.lineParams["Length"]
        return x,y,l

    def browse(self):
        filePath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', 'C:\\Users\\Eren\\Desktop\\VCNET\\dataset')
        filename=filePath[0].split("/")
        self.currentFile=filename[-1]
        self.Filename.setText("Video Name: "+filename[-1])
        self.cap = cv2.VideoCapture(filePath[0])

        ret, self.frame = self.cap.read()
        self.frame=gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.updateImage(self.frame)

        self.lineParams["CheckBox"]=False
        self.FrameNum=1
        self.CurrentFrame.setText("Current Frame: {}".format(self.FrameNum))
        
    def updateMtl(self):
        x,y,l=self.getParams()
        roi_gray = self.frame[x:x+1,y:y+l]
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(roi_gray[0])
        self.MplWidget.canvas.axes.set_title('Signal')
        self.MplWidget.canvas.axes.set_ylim([0,255])
        self.MplWidget.canvas.draw()


    def updateImage(self,img):
        #cv2.namedWindow('LabelApp',cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('LabelApp', 800,480)
        cv2.imshow('LabelApp',img)

    def getNextFrame(self):
        x,y,l=self.getParams()
        ret, self.frame = self.cap.read()
        self.FrameNum+=1
        self.CurrentFrame.setText("Current Frame: {}".format(self.FrameNum))
        self.frame=gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        if (self.lineParams["CheckBox"]==True):
            img=self.frame.copy()
            img=cv2.line(img, (y,x), (y+l,x+1), (255,255,255), 1)
            self.updateImage(img)
            self.updateMtl()
        else:
            self.updateImage(self.frame)

    def keyPressEvent(self, event):
        x,y,l=self.getParams()
        if event.key() == QtCore.Qt.Key_S:
            if(self.FrameNum==self.lastRecordedFrame):
                self.Record.setText("Zaten kaydedildi")
            else:
                self.csvData=np.append(self.csvData,self.currentData)
                #self.getNextFrame()
                self.Record.setText("Frame {} kaydedildi".format(self.lastLabel))
                self.lastRecordedFrame=self.lastLabel
        if event.key() == QtCore.Qt.Key_D:
            self.getNextFrame()
            self.Record.setText("")
        if event.key() == QtCore.Qt.Key_0:
            #self.csvData=np.append(self.csvData,np.append(self.frame[x:x+1,y:y+l],0))
            self.currentData=np.append(self.frame[x:x+1,y:y+l],0)
            self.Record.setText("Label 0 atandı")
            self.lastLabel=self.FrameNum
        if event.key() == QtCore.Qt.Key_1:
            #self.csvData=np.append(self.csvData,np.append(self.frame[x:x+1,y:y+l],1))
            self.currentData=np.append(self.frame[x:x+1,y:y+l],1)
            self.Record.setText("Label 1 atandı")
            self.lastLabel=self.FrameNum

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
