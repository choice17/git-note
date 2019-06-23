## PROTOBUF

- **[Sample0](./pyaudio/example1.py)** 
- **[Sample1](./pyaudio/example2.py)** 
- **[Sample2](./pyaudio/play.py)** 

## Install protobuf compiler  
```
pip install pyaudio
```

## API  

* class pyaudio.PyAudio (master)  
** PyAudio.open 
** PyAudio.get_format_from_width  
** PyAudio.terminate

* class wave (read file)  
** wave.getsampwidth  
** wave.getnchannels  
** wave.getframerate  
** wave.readframes : read frame into array chuncks (important)  

* class stream
** write (output sound)  
** close

## Music note.

* [Musical model for piano](https://dsp.stackexchange.com/questions/46598/mathematical-equation-for-the-sound-wave-that-a-piano-makes)  
* [Music note frequency](http://pages.mtu.edu/~suits/notefreqs.html)  
