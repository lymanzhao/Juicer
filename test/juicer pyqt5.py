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
        self.desktop = QApplication.primaryScreen()
        self.screenRect = self.desktop.availableGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()

        #设置窗口大小

        self.resize(int(self.width*0.6), int(self.height*0.6))

        # 设置窗口标题
        self.setWindowTitle('  Juicer 提取器')
        self.setWindowIcon(QIcon('img/juicer_icon.svg'))

        # 修改成网格布局
        grid = QGridLayout()

        self.pathLine = QTextEdit(readOnly=True)
        self.pathLine.setPlaceholderText("视频源文件")
        grid.addWidget(self.pathLine, 1, 0, 1, 1)

        self.selectButton = QPushButton("选择文件", self)
        self.selectButton.setToolTip('选择MKV视频源文件')
        self.selectButton.clicked.connect(self.openFileNamesDialog)
        self.selectButton.setFixedWidth(160)
        grid.addWidget(self.selectButton, 1, 1)


      
        self.dirLine = QLineEdit(readOnly=True)
        self.dirLine.setPlaceholderText("输出文件夹")
        grid.addWidget(self.dirLine, 2, 0)

        outdirButton = QPushButton("输出目录", self)
        outdirButton.clicked.connect(self.saveFileDialog)
        outdirButton.setToolTip('存储视频的文件夹')
        grid.addWidget(outdirButton, 2, 1)

        self.extrLine = QTextEdit(readOnly=True)
        self.extrLine.setPlaceholderText("等待执行")
        grid.addWidget(self.extrLine, 3, 0, 1, 1)

        self.extractorButton = QPushButton("提取", self)
        self.extractorButton.clicked.connect(self.extractor)
        grid.addWidget(self.extractorButton, 4, 1)

        self.suffix = '.mp4'

        self.mux = ' -c copy '
    

        self.cmdsuffixCombo = QComboBox(self)
        self.cmdsuffixCombo.setFixedWidth(100)
        self.cmdsuffixCombo.addItem("MP4")
        self.cmdsuffixCombo.addItem("MOV")
        self.cmdsuffixCombo.addItem("TrueHD2Eac3")
        self.cmdsuffixCombo.addItem("Atmos")
        self.cmdsuffixCombo.activated[str].connect(self.onChangedCmdsuffix)

        grid.addWidget(self.cmdsuffixCombo, 4, 0,
                       alignment=Qt.AlignRight)


        self.setLayout(grid)

    def onChangedCmdsuffix(self, cmdsuffix):
        if cmdsuffix == "MP4":
            self.suffix = '.mp4'
            self.mux = ' -c copy '
            # print ('mp4')
        if cmdsuffix == "MOV":
            self.mux = ' -c copy '
            self.suffix = '.mov'
            
        if cmdsuffix == "TrueHD2Eac3":
            self.mux = ' -vcodec copy -acodec eac3 '
            self.suffix = '.mp4'

        if cmdsuffix == "Atmos":
            # self.mux = ' -strict -2 '
            self.mux = ' -strict experimental '
            self.suffix = '.mp4'

        

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        # options.setFixedSize(self.width*0.3, self.height*0.5)
        options |= QFileDialog.DontUseNativeDialog
        self.inputFiles, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","视频文件 (*.mkv *.mp4)", options=options)
        if self.inputFiles:
            # print(self.inputFiles)
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
                outputFilePathSuffix = str(self.outputFilePath).replace(self.inputFileSuffix,'')

                self.extractorButton.setEnabled(False)

                satusShowLable = self.outputFilePath + '  正在执行封装工作，请稍等……  '
                self.extrLine.append(satusShowLable)

                ffmpeg = os.getcwd().replace('\\','/') + '/bin/ffmpeg.exe'
                ffmpegcmd = str(ffmpeg + " -y -i " + '"' + inputFilePath +'"' + self.mux + '"' + outputFilePathSuffix + self.suffix + '"')

                thread = threading.Thread(target=self.extractorThread, args=(
                    ffmpegcmd, outputFilePathSuffix,))
                thread.start()

                QApplication.processEvents()

        except AttributeError as err:
            self.extrLine.append('  请检查，文件路径  ')
            # self.extrLine.setStyleSheet('color: yellow')
            pass

    def extractorThread(self, ffmpegcmd, outputFilePathSuffix):
        ffmpegcmdrun = subprocess.Popen(
            ffmpegcmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = ffmpegcmdrun.communicate()
        finalShowText = outputFilePathSuffix + self.suffix + '  提取完成  '
        self.extrLine.append(finalShowText)
        self.extractorButton.setEnabled(True)
        


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside2'))
    ex = Juicer()
    sys.exit(app.exec_())
