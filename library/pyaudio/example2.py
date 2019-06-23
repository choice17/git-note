'''
播放特定頻率
piano notes
https://dsp.stackexchange.com/questions/46598/mathematical-equation-for-the-sound-wave-that-a-piano-makes

music notes frequency
http://pages.mtu.edu/~suits/notefreqs.html
'''
import numpy as np
import pyaudio
 
 
def sine(frequency, t, sampleRate):
    '''
    產生 sin wave
 
    :Args:
     - frequency: 欲產生的頻率 Hz
     - t: 播放時間長度 seconds
     - sampleRate: 取樣頻率 1/s
    '''
    # 播放數量
    n = int(t * sampleRate) 
    # 每秒轉動的角度再細分為取樣間隔
    interval = 2 * np.pi * frequency / sampleRate
    sine_0 = np.sin(np.arange(n) * interval * 3) * (-1/4)
    sine_1 = np.sin(np.arange(n) * interval)  * (1/4)    
    sine_2 = np.cos(np.arange(n) * interval) * (1.73 /2)
    
    return sine_0 + sine_1 + sine_2
 
 
def play_tone(stream, frequency=440, t=1, sampleRate=44100):
    '''
    播放特定頻率
 
    :Args:
     - stream: 
     - frequency: 欲產生的頻率 Hz
     - t: 播放時間長度 seconds
     - sampleRate: 取樣頻率 1/s
    '''
    data = sine(frequency, t, sampleRate)
    data = sine(frequency, t, sampleRate)
    
    # 因 format 為  pyaudio.paFloat32，故轉換為 np.float32 並轉換為 bytearray
    stream.write(data.astype(np.float32).tostring())
 
 
if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1, rate=44100, output=True)
 
    fre = [261.6, 293.7, 329.6, 349.2, 392.0, 440, 493.9,
           523.3, 587.33, 659.25, 698.46, 783.99, 880.00, 987.77 ]
    for _ in range(2):
        for f in fre:
            play_tone(stream, 
             frequency=f, #Hz
             t=0.5) #seconds
        for f in fre[::-1]:
            play_tone(stream, 
             frequency=f, #Hz
             t=0.5) #seconds

    stream.close()
    p.terminate()
 