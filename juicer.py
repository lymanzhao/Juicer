#!/usr/bin/python3
# -*- coding: utf-8 -*-


# ffmpeg -i an.mp4 -i vn.mp4 -map_metadata 0 -c copy map.mp4
# ffmpeg -i "E:\TV\美国\看见 See.S01.HDR.2160p.WEB.h265-NiXON[rartv]\see.s01e01.hdr.2160p.web.h265-nixon.mkv" -c copy D:\va.mp4
# ffmpeg -i "E:\TV\美国\看见 See.S01.HDR.2160p.WEB.h265-NiXON[rartv]\see.s01e01.hdr.2160p.web.h265-nixon.mkv" -vn -c copy D:\vn.mp4
# ffmpeg -i "E:\TV\美国\看见 See.S01.HDR.2160p.WEB.h265-NiXON[rartv]\see.s01e01.hdr.2160p.web.h265-nixon.mkv" -an -c copy D:\an.mp4
# pyinstaller -w -c -D --icon=juicer_icon.ico juicer.py
# 


import os,sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import qdarkstyle
from pathlib import Path

import threading
import subprocess
import time


class Juicer(QWidget):


    def __init__(self):
        super().__init__()

        self.initUI()

        self.show()




    def initUI(self):
        #获取显示器分辨率大小
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()

        #设置窗口大小

        self.resize(self.width*0.6, self.height*0.6)

        # 设置窗口标题
        self.setWindowTitle('  Juicer 提取器')
        self.setWindowIcon(QIcon('img/juicer_icon.svg'))


        # 添加垂直布局
        vbox = QVBoxLayout()

        gridlayout1 = QFormLayout()
        vbox.addLayout(gridlayout1)
        self.pathLine = QTextEdit(readOnly=True)
        # self.pathLine.AutoAll
        gridlayout1.addRow("文件", self.pathLine)
        self.pathLine.setPlaceholderText("视频源文件")
        # self.pathLine = QTextEdit.autoFormatting()

        


        gridlayoutODir = QFormLayout()
        vbox.addLayout(gridlayoutODir)
        self.dirLine = QLineEdit(readOnly=True)
        gridlayoutODir.addRow("输出目录", self.dirLine)
        self.dirLine.setPlaceholderText("输出文件夹")

        gridlayoutextr = QFormLayout()
        vbox.addLayout(gridlayoutextr)

        self.extrLine = QTextEdit(readOnly=True)
        self.extrLine.setAlignment(Qt.AlignLeft)
        gridlayoutextr.addRow("", self.extrLine)
        self.extrLine.setPlaceholderText("等待执行")


        hbox = QHBoxLayout()
        gridlayoutNull = QFormLayout()
        gridlayoutNull.addWidget(QLabel())
        hbox.addLayout(gridlayoutNull)


        gridlayout2 = QFormLayout()
        selectButton = QPushButton("选择文件", self)
        selectButton.setFixedWidth(120)
        # selectButton.setAlignment(Qt.AlignRight)
        gridlayout2.addRow("", selectButton)
        # gridlayout2(selectButton,alignment=Qt.AlignRight)
        
        hbox.addLayout(gridlayout2)
        
        selectButton.setToolTip('选择MKV视频源文件')
        selectButton.clicked.connect(self.openFileNamesDialog)

        outdirButton = QPushButton("输出目录", self)
        outdirButton.clicked.connect(self.saveFileDialog)
        outdirButton.setToolTip('存储视频的文件夹')
        gridlayoutoutdir = QFormLayout()
        gridlayoutoutdir.addRow("", outdirButton)
        hbox.addLayout(gridlayoutoutdir)

        extractorButton = QPushButton("提取", self)
        extractorButton.clicked.connect(self.extractor)
        gridlayout3 = QFormLayout()
        gridlayout3.addRow("", extractorButton)
        hbox.addLayout(gridlayout3)

        tbox = QHBoxLayout()

        
        # self.suffixCBox = QCheckBox("mov",self)
        # self.suffixCBox.stateChanged.connect(self.suffixFilename)
        self.suffix = '.mp4'

        # gridlayoutCBox = QFormLayout()
        # gridlayoutCBox.addRow("", self.suffixCBox)
        # tbox.addLayout(gridlayoutCBox)

        # self.muxCBox = QCheckBox("TrueHD", self)
        # self.muxCBox.stateChanged.connect(self.muxCmd)
        self.mux = ''
    
        # gridlayoutmBox = QFormLayout()
        # gridlayoutmBox.addRow("", self.muxCBox)
        self.cmdsuffixCombo = QComboBox(self)
        self.cmdsuffixCombo.setFixedWidth(100)
        self.cmdsuffixCombo.addItem("MP4")
        self.cmdsuffixCombo.addItem("MOV")
        self.cmdsuffixCombo.addItem("TrueHD")
        self.cmdsuffixCombo.activated[str].connect(self.onChangedCmdsuffix)

        gridlayoutComBo = QFormLayout()
        gridlayoutComBo.addRow("", self.cmdsuffixCombo)
        tbox.addLayout(gridlayoutComBo)

        tbox.addLayout(gridlayoutComBo)



        #添加布局
        vlayout = QVBoxLayout()
        vlayout.addLayout(vbox)
        vlayout.addLayout(hbox)
        vlayout.addLayout(tbox)


        self.setLayout(vlayout)

    def onChangedCmdsuffix(self, cmdsuffix):
        if cmdsuffix == "MP4":
            self.suffix = '.mp4'
            print ('mp4')
        if cmdsuffix == "MOV":
            self.suffix = '.mov'
        if cmdsuffix == "TrueHD":
            self.mux = ' -strict experimental '
        


    def suffixFilename(self, state):

        if state == Qt.Checked:
            # print('Checked')
            self.suffix = '.mov'
 
        if state == Qt.Unchecked:
            # print('Unchecked')
            self.suffix = '.mp4'

    def muxCmd(self, state2):
        
        if state2 == Qt.Checked:
            # print('Checked')
            # self.mux = ' -strict -2 '
            self.mux = ' -strict experimental '
            
            
 
        if state2 == Qt.Unchecked:
            # print('Unchecked')
            self.mux = ''  
        

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.inputFiles, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","视频文件 (*.mkv *.mp4)", options=options)
        if self.inputFiles:
            # print(self.inputFiles)
            # self.fileurl = QUrl.fromLocalFile(self.inputFiles)
            self.filelist =",".join(self.inputFiles)
            self.pathLine.setPlainText(str(self.filelist))
        else:
            pass
            # print(str(self.filelist[0]))
            # print (type(inputFiles))


    def saveFileDialog(self):
        self.outputFileDir = QFileDialog.getExistingDirectory(self,"选择目录","")
        if self.outputFileDir:
            # print(self.outputFileDir)
            self.dirLine.setText(str(self.outputFileDir))
        else:
            pass

    def extractor(self):
        try:
            for inputListFile in self.inputFiles:
                self.inputFileName = Path(inputListFile).name
                self.inputFileSuffix = Path(inputListFile).suffix

                inputFilePath = str(inputListFile).replace('\\','/')

                self.outputFilePath = str(self.outputFileDir) + '/' + str(self.inputFileName)
                self.outputFilePathSuffix = str(self.outputFilePath).replace(self.inputFileSuffix,'')

                satusShowLable = self.outputFilePath + '  正在执行视音频提取工作，请稍等……  '
                self.extrLine.append(satusShowLable)

                ffmpeg = os.getcwd().replace('\\','/') + '/bin/ffmpeg.exe'
                ffmpegcmd = str(ffmpeg + " -y -i " + '"' + inputFilePath +'"' + " -c copy " + self.mux + '"' + self.outputFilePathSuffix + self.suffix + '"')

                thread = threading.Thread(target=self.extractorThread,args=(ffmpegcmd,))
                thread.start()




                QApplication.processEvents()

        except AttributeError as err:
            self.extrLine.append('  请检查，文件路径有没有指定  ')
            # self.extrLine.setStyleSheet('color: yellow')

            pass


    def  extractorThread(self,ffmpegcmd):
        ffmpegcmdrun = subprocess.Popen(ffmpegcmd, shell=True, stdout=subprocess.PIPE,stdin = subprocess.PIPE)
        stdout, stderr = ffmpegcmdrun.communicate()
        finalShowText = self.outputFilePathSuffix + self.suffix + '  提取完成  '
        self.extrLine.append(finalShowText)
        # self.extrLine.append(stdout)
        # self.extrLine.append(stderr)

        # self.extrLine.setStyleSheet('color: yellow')
        # satusShowLable = '  '
        # self.extrLine.append(satusShowLable)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ex = Juicer()
    sys.exit(app.exec_())
