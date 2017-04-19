# -*- coding: utf-8 -*-

import ConfigParser
from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QImage
from PyQt4.QtGui import QApplication, QMainWindow, QPushButton
import sys , time , datetime
import cv2
import os
import numpy as np
import Dialog
from Tkinter import *
from pymodbus.client.sync import ModbusSerialClient as ModbusClient  #  與 COM PORT 溝通
import SetROI,setScore,SetSYS,image_ccd,SetPicNum,version,R130NG,SetDelayTime

video = cv2.VideoCapture(0)
video.set(3,1280)
video.set(4,1024)
class ImageWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        super(ImageWidget,self).__init__(parent)
        self.image=None

    def setImage(self,image):
        self.image=image
        sz=image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self,event):
        qp=QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0,0),self.image)
        qp.end()
class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        self.Now_Language = 1
        self.gtpic = False
        start_getPicture = False
        self.getwhichpicture = 0
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        config.read('ROI.ini')
        total_section = config.sections()
        config.set("R1", "image_num", '0')
        config.write(open('ROI.ini', 'wb'))
        self.start_CCD_GO = False
        super(MainWindow,self).__init__(parent)
        
        self.exitAction = QtGui.QAction(u'離開', self)
        self.exitAction.triggered.connect(QtGui.qApp.quit)

        self.f2Action = QtGui.QAction(u"取得開模後相片", self)
        self.f2Action.triggered.connect(self.getPic1)

        self.f7Action = QtGui.QAction(u"取得閉模前相片", self)
        self.f7Action.triggered.connect(self.getPic2)

        self.f3Action = QtGui.QAction(u"設定檢測區域", self)
        self.f3Action.triggered.connect(self.getROI1)

        self.f8Action = QtGui.QAction(u"設定檢測區域", self)
        self.f8Action.triggered.connect(self.getROI2)

        self.f11Action = QtGui.QAction(u"設定射出後樣本", self)
        self.f11Action.triggered.connect(self.getROI1R)

        self.f12Action = QtGui.QAction(u"設定開模前樣本", self)
        self.f12Action.triggered.connect(self.getROI2R)

        self.f4Action = QtGui.QAction(u"開始檢測", self)
        self.f4Action.triggered.connect(self.startCCD)

        self.f5Action = QtGui.QAction(u"停止檢測", self)
        self.f5Action.triggered.connect(self.stopCCD)

        self.f6Action = QtGui.QAction(u"設定分數", self)
        self.f6Action.triggered.connect(self.click_score1)

        self.f9Action = QtGui.QAction(u"設定分數", self)
        self.f9Action.triggered.connect(self.click_score2)

        self.action102_setDelayTime = QtGui.QAction(u"設定延遲時間", self)
        self.action102_setDelayTime.triggered.connect(self.F_SetDelayTime102)

        self.action104_setDelayTime = QtGui.QAction(u"設定延遲時間", self)
        self.action104_setDelayTime.triggered.connect(self.F_SetDelayTime104)

        self.f10Action = QtGui.QAction(u"系統設定", self)
        self.f10Action.triggered.connect(SetSYS.sys_set)

        self.f13Action = QtGui.QAction(u"相片數量", self)
        self.f13Action.triggered.connect(SetPicNum.setpicnum)

        self.f99Action = QtGui.QAction(u"拍攝相片", self)
        self.f99Action.triggered.connect(self.getpic)

        self.VersionAction = QtGui.QAction(u'版本', self)
        self.VersionAction.triggered.connect(self.getVersion)
        
        self.LanguageAction = QtGui.QAction(u'更換語言', self)
        self.LanguageAction.triggered.connect(self.ChangeLanguage)

        menubar = self.menuBar()
        fileMenu1 = menubar.addAction(self.f4Action)
        self.fileMenu2 = menubar.addMenu(u'開模後檢測')
        self.fileMenu3 = menubar.addMenu(u'閉模前檢測')
        self.fileMenu4 = menubar.addMenu(u'設定')
        font = self.fileMenu2.font()
        font.setPointSize(30)
        menubar.setFont(font)
        self.fileMenu2.setFont(font)
        self.fileMenu3.setFont(font)
        self.fileMenu4.setFont(font)
        self.fileMenu2.addAction(self.f2Action)
        self.fileMenu3.addAction(self.f7Action)
        self.fileMenu2.addAction(self.f11Action)
        self.fileMenu3.addAction(self.f12Action)
        self.fileMenu2.addAction(self.f6Action)
        self.fileMenu3.addAction(self.f9Action)
        self.fileMenu2.addAction(self.action102_setDelayTime)
        self.fileMenu3.addAction(self.action104_setDelayTime)
        self.fileMenu4.addAction(self.VersionAction)
        self.fileMenu4.addAction(self.LanguageAction)
        self.fileMenu4.addAction(self.exitAction)
        
        self.videoFrame=ImageWidget()
        self.setCentralWidget(self.videoFrame)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.showFullScreen()
        self.timer=QtCore.QTimer(self)
        
        self.timer.timeout.connect(self.update)
        self.timer.start(100)
    def ChangeLanguage(self):
        if self.Now_Language == 2:
            self.fileMenu2.setTitle(u'開模後檢測')
            self.fileMenu3.setTitle(u'閉模前檢測')
            self.fileMenu4.setTitle(u'設定')
            self.exitAction.setText(u'離開')
            self.f2Action.setText(u"取得開模後相片")
            self.f7Action.setText(u"取得閉模前相片")
            self.action102_setDelayTime.setText(u"設定延遲時間")
            self.action104_setDelayTime.setText(u"設定延遲時間")
            self.f11Action.setText(u"設定射出後樣本")
            self.f12Action.setText(u"設定開模前樣本")
            self.f4Action.setText(u"開始檢測")
            self.f6Action.setText(u"設定分數")
            self.f9Action.setText(u"設定分數")
            self.VersionAction.setText(u'版本')
            self.LanguageAction.setText(u'ChangeLanguage')
            self.Now_Language = 1
        elif self.Now_Language == 1:
            self.fileMenu2.setTitle(u'after_open')
            self.fileMenu3.setTitle(u'before_close')
            self.fileMenu4.setTitle(u'Setting')
            self.exitAction.setText(u'exit')
            self.f2Action.setText(u"Get Template Picture")
            self.f7Action.setText(u"Get Template Picture")
            self.action102_setDelayTime.setText(u"Set Delay Time")
            self.action104_setDelayTime.setText(u"Set Delay Time")
            self.f11Action.setText(u"Set Template")
            self.f12Action.setText(u"Set Template")
            self.f4Action.setText(u"Start")
            self.f6Action.setText(u"Set Score")
            self.f9Action.setText(u"Set Score")
            self.VersionAction.setText(u'Version')
            self.LanguageAction.setText(u'更換語言')
            self.Now_Language = 2
    def getVersion(self):
        version.show()
    def F_SetDelayTime102(self):
        SetDelayTime.show(102)
    def F_SetDelayTime104(self):
        SetDelayTime.show(104)
    def getPic1(self):
        try:
            image_ccd.client.write_registers(0x78,[9090],unit=0x01)
            image_ccd.start_getPicture = 102
            self.start_CCD_GO = True
            image_ccd.ddd = True
        except:
            Dialog.show("尚未連接機台")
    def getPic2(self):
        try:
            image_ccd.client.write_registers(0x78,[9090],unit=0x01)
            image_ccd.start_getPicture = 104
            self.start_CCD_GO = True
            image_ccd.ddd = True
        except:
            Dialog.show("尚未連接機台")
    def click_score1(self):
        setScore.setscore(1)
    def click_score2(self):
        setScore.setscore(2)
    def getROI1(self):       #設定檢測區域
        SetROI.get_ROI(2)
    def getROI2(self):       #設定檢測區域
        SetROI.get_ROI(22)
    def getROI1R(self):       #設定射出前樣本
        SetROI.get_ROI(3)
    def getROI2R(self):       #設定閉模前樣本
        SetROI.get_ROI(33)
    def update(self):
        if self.start_CCD_GO and image_ccd.ddd == True:
            rq = image_ccd.client.write_registers(0x80,[9090],unit=0x01)    #R128  表示在運行中
            #~ result = image_ccd.client.read_holding_registers( 0x78 ,1,unit=0x01) # R120
            #~ R120 = result.registers[0]
            #~ print "GO_R120:",R120
            image_ccd.updateImage()
        else:
            try:
                ret, frame = video.read()
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QtGui.QImage(frame, frame.shape[1], frame.shape[0],frame.strides[0], QtGui.QImage.Format_RGB888)
                image = image.scaled(640,512,QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
                #~ print image.size()
                self.videoFrame.setImage(image)
                #~ # check 
                result = image_ccd.client.read_holding_registers( 0x82 ,1,unit=0x01) # R130
                R130 = result.registers[0]
                if R130 == 2266:
                    R130NG.run()
                result = image_ccd.client.read_holding_registers( 0x78 ,1,unit=0x01) # R120
                R120 = result.registers[0]
                #~ print "NOGO_R120:",R120
                if R120 == 0:
                    cv2.destroyWindow("openCV")
                if self.gtpic :
                    ret, frame = video.read()
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    ms = datetime.datetime.now().microsecond
                    cv2.imwrite("D:/todocv/imm/pic/CCD/pic"+time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+str(ms)+".png",frame)
            except:
                print 'error'
    def getpic(self):
        self.gtpic = not self.gtpic
    
    def startCCD(self): # 開始檢測
        try:
            image_ccd.client.write_registers(0x78,[9090],unit=0x01) # R120
            image_ccd.client.write_registers(0x80,[9090],unit=0x01) # R128
            self.start_CCD_GO = True
            image_ccd.ddd = True
        except:
            Dialog.show("尚未連接機台")
    def stopCCD(self):
        self.start_CCD_GO = False
        image_ccd.client.write_registers(0x78,[2266],unit=0x01)

def main():
    app=QtGui.QApplication(sys.argv)
    w=MainWindow()
    w.show()
    app.exec_()

if __name__=='__main__':
    main()


