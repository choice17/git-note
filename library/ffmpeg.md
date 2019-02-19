# FFMPEG 

* **Content**  
* **[ffmpeg](#ffmpeg)**  
* **[ffprobe](#ffprobe)**  
* **[ffplay](#ffplay)**  
* **[libav](#libav)**  
* **[sdl](#sdl)**  
* **[compile](#compile)**  

## ffmpeg  

ffmpeg is a commandline tool which enable 
numerous functionalities for codec filtering and as a streaming and mediaplayer  

simple demo on public rtsp server 

`ffmpeg -i rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_114k.mov save.mp4`  

**input file** `-i`

**output file** `save.mp4`   

**scaling** `-vf scale={int}x{int}`  

**filter** scale with crop  "crop=<size_x>:<size_y>:<start_pt_x>:<start_pt_y>"  
`-vf "crop=in_w/2:in_h:in_w/2:0,scale=1200:400"`  

**codec** `-c:{chn:v/a/v} {codec, or copy}`  

**stop time** `-t xx:xx:xx.xxx`   

**start time** `-ss xx:xx:xx.xxx`  

**output format** `-f {output format} {output file}`  
options  
`-f rtp_mpegts rtp://192.168.1.147:8554`  
`-f matroska output.mkv`  

**add subtitle**   
`ffmpeg -i {inputfile} -i {subtitle} -map 0:0 -map 1:0 -c:copy -f matroska output.mkv`  
: map {inputfile#}:{channel#}  

**extract subtitle**  
`ffmpeg -i {input} -f srt/ass {-/output.ass/.srt}` 

**extract video**  
`ffmpeg -i {input} -map 0:v output.mp4` 

**force output**  
`ffmpeg -y -i {input} {output}` 

**verbose** `-v 0-64 or -v {fatal, debug, critical, quiet, ...}`  

**snapshot** 
`ffmpeg -i {input} {output} -vframe 1 image.png`  

**pipe**  
`ffmpeg -i {input} -f image2pipe -pix_fmt {rgb24/bgr24/mjpeg/png} -`  

**display**  
`ffmpeg -i {input} -f sdl test`  

**rtsptransport** explicit tcp transport for rtsp  
`ffmpeg -rtsp_transport tcp -i {rtsp} output.mp4`  

**re set frame rate** for static video file  
`ffmpeg -re -i {file} output.mp4`  open with native rate  
`ffmpeg -r {frame rate} -i {file} output.mp4`  change fr rate  

**list available device** for dshow  
`ffmpeg -list_devices true -f dshow -i dummy`  
`chcp 65001 & ffmpeg -list_devices true -f dshow -i dummy`  to encode str  

**display streaming from local device**  
`ffmpeg -f dshow -i video="HP Truevision Full HD" -pix_fmt yuv420p -window_size qcif -f sdl "test"`  

**streaming from local device**  
`ffmpeg -f dshow -i video="HP Truevision Full HD":audio="Microphone (Intel® Smart Sound Technology)"  -pix_fmt yuv420p -window_size qcif -f mpgets udp://127.0.0.1:8888`  

**filter nal packet type**   
`ffmpeg -i INPUT -c:v copy -bsf:v 'filter_units=pass_types=1-5' OUTPUT`  
`ffmpeg -i INPUT -c:v copy -bsf:v 'filter_units=remove_types=35|38-40' OUTPUT`  
`ffmpeg -i TT.h264  -c:v copy -bsf:v 'filter_units=pass_types=6' -f rawvideo -`  

**add nal sei_user_data**    
`ffmpeg -i INPUT.h264 -c:v libx264 -sn -an -bsf:v h264_metadata=sei_user_data='086f3693-  
b7b3-4f2c-9653-21492feee5b8+hello' OUTPUT.h264`  

## ffprobe  

`ffprobe -i {input} `  

## ffplay  

`ffplay -vf scale={}x{} -i {input}`  

## libav  

* [pyav](#pyav) 
* [libav](#libav)  

## pyav  

installation  
```bash 
conda install conda-forge -c av 
```  

**open**  
```python  
import av 
option = {}
option[ffmpegoption] = ffmpegoption
cap = av.open(url, option)

```

**decode**
```python
for pid, packets in cap.demux():
    
    for fidx, frame in packets.decode():
	if packets.type == 'video':
	   img = frame.to_ndarray()

	if packets.type == 'subtitle':
	   sub = frame.decode('ass').split()
```

## sdl  
[reference](http://lazyfoo.net/tutorials/SDL/index.php)   
pysdl2  
sdl2.dll  

**window**  

**surface**  

**biltscale**

**texture**  

**renderer**  


**rendercopy**  

## compile 

linker for ffmpeg lib [ref](https://fritzone.wordpress.com/2010/05/11/link-with-static-ffmpeg/)  

1. Configure your ffmpeg to generate static libraries:  

```
./configure –enable-static –enable-gpl –enable-libfaac –enable-libfaad –enable-libx264 –enable-nonfree
make && make install
(in the ffmpeg directory)
```

2. Now, link your application:

```
gcc -Wall -g live_mystuff.c -o my_app \
/usr/local/src/ffmpeg/libswscale/libswscale.a \
/usr/local/src/ffmpeg/libavdevice/libavdevice.a \
/usr/local/src/ffmpeg/libavformat/libavformat.a \
/usr/local/src/ffmpeg/libavcodec/libavcodec.a \
/usr/local/src/ffmpeg/libavutil/libavutil.a \
-lpthread -lbz2 -lm -lz -lfaac -lmp3lame -lx264 -lfaad
```
And DO NOT change the order of the libraries above, otherwise you’ll get lots of link errors like:  

```
/usr/local/src/ffmpeg/libavformat/libavformat.a(allformats.o): In function `av_register_all’:
/usr/local/src/ffmpeg/libavformat/allformats.c:47: undefined reference to `avcodec_register_all’
```

3. sample player prog  

[REFERENCE simplest ffplay](./simplest_ffplay_makefile)  
```
player/
      |-src/ffplay.cc
      |-Makefile
```
