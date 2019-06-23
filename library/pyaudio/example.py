'''
non-blocking
播放特定頻率
'''
import numpy as np
import pyaudio
import time
 
# frames
CHUNK = 1024
# channels
CH = 1
 
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
    
    return np.sin(np.arange(n) * interval)
 
    
def sliceData(frame_count, channels):  
    '''
    切出合適的長度，也就是 frame_count * channels * sampleBytes
 
    :Args:
     - frame_count: frames 的數目
     - channels: channels 數目
    '''
    data = sine(frequency=1000, t=3, sampleRate=44100)
    
    # 因會再轉換為 np.float32，故無需乘上 sampleBytes
    size = channels * frame_count
    while True:
        dataSlice = data[:size]
        # 此時小數點會用 np.float32 4byte 表示，故資料長度會變為 4 倍
        dataBytes = dataSlice.astype(np.float32).tostring()
        
        yield dataBytes
        # 刪除已輸出資料
        data = np.delete(data, range(size))
 
    
dataGen = sliceData(CHUNK, CH)
def callback(in_data, frame_count, time_info, status):
    global dataGen
    data = next(dataGen)
 
    return (data, pyaudio.paContinue)
 
 
if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CH, rate=44100, output=True, frames_per_buffer=CHUNK, stream_callback=callback)
 
    # stream.start_stream()
    
    for i in range(1000):
        print(i)    
        
    stream.stop_stream()
    stream.close()
    p.terminate()