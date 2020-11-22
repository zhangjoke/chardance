import warnings
warnings.simplefilter("ignore", DeprecationWarning)#防止报警告
import pyaudio
import wave

import numpy as np
import curses

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(False)
MAX_Y, MAX_X = stdscr.getmaxyx()

CHUNK = 1024#缓冲流


wf = wave.open("tmp.wav", 'rb')#以只读的方式打开wav文件

#创建播放器
p = pyaudio.PyAudio()
#打开数据流  output=True表示音频输出
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),#设置声道数
                rate=wf.getframerate(),#设置流的频率
                output=True)


data = wf.readframes(CHUNK)#音频数据初始化

while data != '':#直到音频放完
    stream.write(data)#播放缓冲流的音频
    data = wf.readframes(CHUNK)#更新
    numpydata = np.fromstring(data, dtype=np.int16)#把data由字符串以十六进制的方式转变为数组
    transforamed=np.real(np.fft.fft(numpydata))#傅里叶变换获取实数

    total = transforamed.size
    count= int(total / MAX_X)#设置间隔
    x = 0
    stdscr.erase()
    while x < MAX_X - 1:
        value =abs(int(transforamed[x]/420000))#对数据取整和绝对值
        x += 1
        for y in range(0, value):
            stdscr.addstr(MAX_Y -2 - y, x, "┃")
    stdscr.refresh()

stream.stop_stream()
stream.close()
#关闭流
p.terminate()
curses.endwin()
