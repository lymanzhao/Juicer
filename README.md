#  Jucicer extractor

![](img/juicer_icon.svg)

Jucicer extractor 是应剪辑师楚老师的需求，将.mkv文件中的视音频直接重新打包到mp4文件中，以便给Adobe Premiere，Davinci Resolve等专业软件使用，而不需要转码，破坏画面。

主流的转码软件再次编码，对画质影响不提，如果是4K、h265、10 bit源码，再次编码时间非常久，效率低，并且对高画质、杜比音频等都会再次编码降低质量。

Jucicer extractor 仅仅使用文件封装技术，支持多线程，几乎不耗CPU和显卡性能，瓶颈主要在磁盘IO性能，以及少量内存。



##  其他注意

没有限制多线程数量，多文件同时打包的时候注意观察计算机性能。

重命名文件使用覆盖方式

GUI使用PyQT5

编解码使用了 ffmpeg

pyinstaller 打包exe程序，关闭主程，ffmpeg子线程有可能不会跟着停止，如数量过多会导致机器长时间无响应直至死机。

可选输出mov文件，需要注意quicktime player不支持某些特定编码和封装

解决TrueHD版本的Experimental功能



### 主程序界面

![](img/02.png)

### Windows操作系统进程情况

![](img/01.png)

### 新改界面

![](img/03.png)

