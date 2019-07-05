'''
播放特定頻率
piano notes
https://dsp.stackexchange.com/questions/46598/mathematical-equation-for-the-sound-wave-that-a-piano-makes

music notes frequency
http://pages.mtu.edu/~suits/notefreqs.html

music input
https://stackoverflow.com/questions/26478315/getting-volume-levels-from-pyaudio-for-use-in-arduino

music synthesis
https://music.stackexchange.com/questions/71531/why-doesnt-my-synthesized-note-sound-natural
fft freq analysis
harmonics
attacks
'''
import numpy as np
import pyaudio
 

fre = [130.81, 146.83, 164.81, 174.61, 196.00, 220.00, 246.94, #c3
        261.6, 293.7, 329.6, 349.2, 392.0, 440, 493.9, #c4
       523.3, 587.33, 659.25, 698.46, 783.99, 880.00, 987.77, #c5
       1046.50, 1174.66, 1318.51, 1396.91, 1567.98, 1760.00, 1975.53, #c6
       2093.00, 2349.32, 2637.02, 2793.83, 3135.96, 3520.00, 3951.07] #c7]
core = [261.6, 293.7, 329.6, 349.2, 392.0, 440, 493.9]
fullfre = [f/4 for f in core] +\
          [f/2 for f in core] +\
          core +\
          [f*2 for f in core] +\
          [f*4 for f in core] +\
          [f*8 for f in core] +\
          [f*16 for f in core]

[c3,d3,e3,f3,g3,a3,b3,
 c4,d4,e4,f4,g4,a4,b4,
 c5,d5,e5,f5,g5,a5,b5,
 c6,d6,e6,f6,g6,a6,b6,
 c7,d7,e7,f7,g7,a7,b7] = fre
[D1,D2,D3,D4,D5,D6,D7,
 E1,E2,E3,E4,E5,E6,E7,
 F1,F2,F3,F4,F5,F6,F7,
 G1,G2,G3,G4,G5,G6,G7,
 A1,A2,A3,A4,A5,A6,A7] = fre
N = {D1:"D1",D2:"D2",D3:"D3",D4:"D4",D5:"D5",D6:"D6",D7:"D6",
 E1:"E1",E2:"E2",E3:"E3",E4:"E4",E5:"E5",E6:"E6",E7:"E7",
 F1:"F1",F2:"F2",F3:"F3",F4:"F4",F5:"F5",F6:"F6",F7:"F7",
 G1:"G1",G2:"G2",G3:"G3",G4:"G4",G5:"G5",G6:"G6",G7:"G7",
 A1:"A1",A2:"A1",A3:"A1",A4:"A1",A5:"A1",A6:"A1",A7:"A1"}

def sine(frequency, t, sampleRate,shift=np.pi/4):
    '''
    :Args:
     - frequency: Hz
     - t: seconds
     - sampleRate: 1/s
    '''
    
    n = int(t * sampleRate) 
    
    interval = 2 * np.pi * frequency / sampleRate
    sn = int((shift / (2 * np.pi)) * interval)
    sn_2 = int((shift / 2 / (2 * np.pi)) * interval)
    #sine_0 = np.sin(np.arange(n) * interval * 3) * (-1/4)
    #sine_1 = np.sin(np.arange(n) * interval)  * (1/4)
    sine_2 = np.cos(np.arange(-sn, n-sn) * interval ) * 1 - 0.5
    sine_2 = np.where(sine_2 >= 0, sine_2, 0)
    sine_3 = np.cos(np.arange(n) * interval ) * (1.73/4)
    sine_4 = np.cos(np.arange(n) * interval / 2) * (1.73/4)
    sine_5 = np.cos(np.arange(-sn_2,n-sn_2) * interval / 4) * (1.73/4)
    sine_6 = np.cos(np.arange(-sn,n-sn) * interval / 8) * (1.73/16)
    sine_7 = np.cos(np.arange(-sn,n-sn) * interval / 16) * (1.73/32)
    #sine_6 = np.cos(np.arange(-sn,n-sn) * interval / 8) * (1.73/6)

    a_sn = int((np.pi/4 / 2 / (2 * np.pi)) * (np.pi / n / 2))
    a = np.cos(np.arange(n) * np.pi / n / 2) * 0.9
    a_ = np.cos(np.arange(a_sn,n+a_sn) * np.pi / n / 2) * 1
    a *= a_
    #res = (sine_0 + sine_1 + sine_2) *a
    res = (sine_3 - sine_2 + sine_4 - sine_5 + sine_6 - sine_7) * a
    #res = sine_2 * a
    return res
    #return sine_2
 

def piano(frequency, t, sampleRate,shift=np.pi/4):
    n = int(t * sampleRate)
    Fin  =2 * np.pi / sampleRate
    interval = Fin * frequency
    sn = int((shift / (2 * np.pi)) * interval)
    #sine_2 = np.cos(np.arange(-sn, n-sn) * interval ) * 1 - 0.95
    #sine_2 = np.where(sine_2 >= 0, sine_2, 0)

    s0 = np.cos(np.arange(n) * interval) * 0.5
    s0 += np.cos(np.arange(n) * interval * 80) * 0.3
    s1 = np.cos(np.arange(n) * interval*2) * 0.5 * 0.1

    s2 = np.cos(np.arange(n) * interval*4) * 0.5 * 0.1 * 0.5
    s3 = np.cos(np.arange(n) * interval*8) * 0.5 * 0.1 * 0.6
    s4 = np.cos(np.arange(n) * interval*16) * 0.5 * 0.1 * 0.1

    #cD = np.cos(np.arange(n) * Fin) * 0.5 * 0.1
    #cD *= np.random.randn(n) * 0.5 * 0.05
    c0 = np.cos(np.arange(n) * interval * 0.5) * 0.5 * 0.1 * 0.5
    c1 = np.cos(np.arange(n) * interval * 1.5) * 0.5 * 0.1 * 0.15
    c2 = np.cos(np.arange(n) * interval * 2.5) * 0.5 * 0.1 * 0.1
    c3 = np.cos(np.arange(n) * interval * 3.5) * 0.5 * 0.1 * 0.08
    c4 = np.cos(np.arange(n) * interval * 4.5) * 0.5 * 0.1 * 0.07

    s = s0 + s1 + s2 + s3 + s4 
        #c0 + c1 + c2 + c3 + c4 # + cD

    """
    a_sn = int((np.pi/4 / 2 / (2 * np.pi)) * (np.pi / n / 2))
    a = np.cos(np.arange(n) * np.pi / n / 2) * 0.8
    a_ = np.cos(np.arange(a_sn,n+a_sn) * np.pi / n / 2) * 1
    a *= a_
    """
    a_sn = int((np.pi/4 / 2 / (2 * np.pi)) * (np.pi / n / 2))
    a_sn2 = int((np.pi / 2 / (2 * np.pi)) * (np.pi / n / 2))
    a = np.cos(np.arange(n) * np.pi / n / 2) * 0.8
    a_ = np.cos(np.arange(a_sn,n+a_sn) * np.pi / n / 2) * 1
    a__ = np.cos(np.arange(a_sn2,n+a_sn2) * np.pi / n / 2) * 1
    a *= a_# * a__)
    a *= a__
 
    res = s * a 
    return res

def play_tone(stream, frequency=440, t=1, sampleRate=44100):
    '''
    :Args:
     - stream: 
     - frequency: Hz
     - t: seconds
     - sampleRate: 1/s
     - piano tone
    '''

    if type(frequency) == list:
        ratio = 1 / len(frequency)
        data = piano(frequency[0], t, sampleRate) * ratio
        for f in frequency[1:]:
            data += piano(f, t, sampleRate) * ratio
    else:
        #data = sine(frequency, t, sampleRate) * 0.7
        data = piano(frequency, t, sampleRate) * 0.7
    
    _len = data.shape[0]
    res = np.empty((_len,2),dtype=np.float32)
    res[:,0] = data.astype(np.float32)
    res[:,1] = res[:,0]
    #data = data.astype(np.float32).tostring()
    #data += data
    stream.write(res.flatten().tostring())

def main():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=2, rate=44100, output=True)
    
    """
    com = [e4,d4,c4,b3,a3,g3,a3,b3]
    comt = [2,2,2,2,2,2,2,2,2]
    com2 = [[e5,g4],[d5,g4],[c5,e4],[b4,e4],[a4,c4],[g4,c4],[a4,c4],[b4,e4]]
    com2t = [2,2,2,2,2,2,2,2,2]
    com3 = [[e5,g4],[d5,g4],a4,c5,b4,g4,a4,e4,[a4,f4],[g4,d4],f4]
    com3t = [2,1,1,2,1,1,2,1,1,2,1,1]
    com4 = [c5,b4,c5,e4,g4,b4,c5,e5,g5,e5,a5,f5,e5,d5,f5,e5,d5,c5,b4,a4,f4,c5,b4,g4,c5,b4]
    com4t = [0.5,0.5,0.5,0.5,1,1,1,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5]
    """

    com = [E3,E2,E1,D7,D6,D5,D6,D7]
    comt = [2,2,2,2,2,2,2,2,2]
    com2 = [[E5,F3],[E5,F2],[E3,F1],[E3,E7],[E1,E6],[E1,E5],[E1,E6],[E2,E7]]
    com2t = [2,2,2,2,2,2,2,2,2]
    com3 = [[E5,F3],[E5,F2],E4,F1,E7,E5,E6,E5,E3,[E4,E6],[E2,E5],E4]
    com3t = [2,1,1,2,1,1,2,1,1,2,1,1]
    com4 = [F1,E7,F1,E3,E5,E7,F1,F3,F5,F3,F5,F6,F4,F3,F2,F4,F3,F2,F1,E7,E6,E4,F1,E7,E5,F1,E7]
    com4t = [0.5,0.5,0.5,0.5,1,1,1,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5]
    com5 = [F1,E7,F1,E3,E5,E7,F1,F3,F1,F5,F3,F5,F6,F4,F3,F2,F4,F3,F2,F1,E7,E6,E5,E4,F1,E5,E7,F2,E5]
    com5t = [0.5,0.5,0.5,0.5,1,1,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.75,0.25,0.5,0.25,0.25]
    com6 = [F3,E5,F3,F2,F1,F2,F2,F3,F4,F3,F2,F3,F1,F1,F1,E7,F1,E7,E5,E3,E3,E5,E6,E7,F1,E5,E3,E5,[E4,E6],E4,E6,F1,F1,E7,E7,F1,F2,F5]
    com6t = [0.75,0.25,0.25,0.25,0.25,0.25,0.75,0.25,0.25,0.25,0.25,0.25,0.75,0.25,0.5,0.25,0.25,0.5,0.25,0.25,0.5,0.5,1,0.5,0.5,1,0.5,0.5,1,0.25,0.25,0.5,0.75,0.25,0.25,0.25,0.25,0.25]
    comE = [[E2,E7]]
    comEt = [4]
    coms = [[com,comt],[com2,com2t],[com3,com3t],[com4,com4t],[com5,com5t],
           [com6,com6t],[comE,comEt]]
    i = 0
    for _cs,_ts in coms:
        print("com", i)
        j = 0
        for c, t in zip(_cs, _ts):
            if type(c) == list:
                print("[[%s,%s],%.2f]"%(N[c[0]],N[c[1]],t))
            else:
                print("[%s,%.1f]"%(N[c],t))
            play_tone(stream, 
                 frequency=c, #Hz
                 t=t/2) #seconds
            j+=1
        i += 1
        """
        for c,t in zip(com,comt):
            play_tone(stream, 
             frequency=c, #Hz
             t=t/2) #seconds
        for c,t in zip(com2,com2t):
            play_tone(stream, 
             frequency=c, #Hz
             t=t/2) #seconds
        for c,t in zip(com3,com3t):
            play_tone(stream, 
             frequency=c, #Hz
             t=t/2) #seconds
        for c,t in zip(com4,com4t):
            play_tone(stream, 
             frequency=c, #Hz
             t=t/2) #seconds
        """

    stream.close()
    p.terminate()
 
 
def main2():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=2, rate=44100, output=True)
    for f in fullfre:
        print(f)
        play_tone(stream, 
             frequency=f, #Hz
             t=1) #seconds



if __name__ == '__main__':
    main()

