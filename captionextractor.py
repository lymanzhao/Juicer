import os,sys

import subprocess

# ffmpeg -i Life.of.Pi.has.subtitles.mkv-map 0:s:0 sub1.srt
# 列出当前目录下所有的文件
# 文件路径通过资源管理器地址栏直接复制粘贴，filepaths = "D:\Downloads\MasterClass - Salman Rushdie Teaches Storytelling and Writing"
filepaths = input("文件夹路径:")   
files = os.listdir(filepaths)
print (files)
ffmpeg = os.getcwd().replace('\\','/') + '/bin/ffmpeg.exe'


for filename in files:
    portion = os.path.splitext(filename)
#     # 如果后缀是.txt
    if portion[1] == ".mkv":
        inputFilePathSuffix = filepaths+ "\\" +portion[0] + ".mkv"
        outputFilePathSuffix = filepaths+ "\\" +portion[0] + ".srt"
        print (outputFilePathSuffix)
        ffmpegcmd = str(ffmpeg + " -i " + '"' + inputFilePathSuffix + '"' +  " -map 0:s:0 " + '"' + outputFilePathSuffix + '"')
        
        ffmpegcmdrun = subprocess.Popen(ffmpegcmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = ffmpegcmdrun.communicate()
        print ('====================================================================' + outputFilePathSuffix + ' 字幕提取完成 ==================================================================== ')