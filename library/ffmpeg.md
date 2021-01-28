# FFMPEG 

* **Content**  
* **[ffmpeg](#ffmpeg)**  
* **[ffprobe](#ffprobe)**  
* **[ffplay](#ffplay)**  
* **[ffserver](#ffserver)**  
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

**extract frame number**  
`ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 <file>`  

**extract video**  
`ffmpeg -i {input} -map 0:v output.mp4` 

**force output**  
`ffmpeg -y -i {input} {output}` 

**verbose** `-v 0-64 or -v {fatal, debug, critical, quiet, ...}`  

**show all 264/264 nalu info**  
`ffmpeg -i in.264 -c copy -bsf:v trace_headers -f null - 2> NALUS.txt`  

**snapshot** 
`ffmpeg -i {input} {output} -vframe 1 image.png`  

**pipe**  
`ffmpeg -i {input} -f image2pipe -pix_fmt {rgb24/bgr24/mjpeg/png} -`  

**display**  
`ffmpeg -i {input} -f sdl test`  

**write video from images**
`ffmpeg -framerate 25 -i "%09d.jpg" -c:v libx264 output.mp4`

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

**pipe NALU and SEI data to stdout**
`ffmpeg -rtsp_transport tcp  -y -v fatal  -i "rtsp://192.168.0.1:8554/live/0" -vf scale=1280:720 -map v:0 -an -vs
ync 2 -hide_banner  -f image2pipe -codec rawvideo  -pix_fmt bgr24 -  -c:v copy -f rawvideo -bsf:v 'filter_units=pass_typ
es=6' -`

**stream to m3u8**
```$ ffmpeg -y \
 -i sample.mov \
 -codec copy \
 -bsf h264_mp4toannexb \
 -map 0 \
 -f segment \
 -segment_time 10 \
 -segment_format mpegts \
 -segment_list "/Library/WebServer/Documents/vod/prog_index.m3u8" \
 -segment_list_type m3u8 \
 "/Library/WebServer/Documents/vod/fileSequence%d.ts"
```
```
$ ffmpeg -y \
    -i sample.mov \
    -hls_time 9 \
    -hls_segment_filename "/Library/WebServer/Documents/vod/fileSequence%d.ts" \
    -hls_playlist_type vod \
    /Library/WebServer/Documents/vod/prog_index.m3u8
```

**streaming with ffserver**  

For loop to avoid connection failures. This command allows ffmpeg to streaming in rasbperry pi 3 linux raspbian env with camera connected in `/dev/video`.
```
#!/bin/bash


while true; do
	ffmpeg -r 50 -s 640x480 -f video4linux2 -i /dev/video0 http://localhost:8090/feed1.ffm
	sleep 5 
done
```

## ffserver  

Although ffserver is no-longer being maintaining, it is still useful for streaming service or you may use live555 for alternative.

`ffserver -d -f <ffserver.conf>` to input ffserver config  

* RTSP  
```python 
### ffserver.conf  ###
HttpPort 8090 
RtspPort 8554
HttpBindAddress 0.0.0.0 
MaxClients 1000 
MaxBandwidth 10000 
NoDaemon 

<Feed feed1.ffm> 
File /tmp/feed1.ffm 
FileMaxSize 5M 
</Feed> 

<Stream live/0>
Feed feed1.ffm
Format rtp
VideoCodec mpeg4
VideoFrameRate 50
VideoBufferSize 80000
VideoBitRate 100
VideoQMin 1
VideoQMax 5
VideoSize 640x480
PreRoll 0
Noaudio
</Stream>
```

* HTTP 
```
HttpPort 8090 
HttpBindAddress 0.0.0.0 
MaxClients 3 
MaxBandwidth 10000
NoDaemon 

<Feed feed1.ffm> 
File /tmp/feed1.ffm 
FileMaxSize 5M 
</Feed> 

<Stream live/0>
Feed feed1.ffm
Format mpjpeg
VideoFrameRate 25
VideoBufferSize 80000
VideoBitRate 300
VideoQMin 2
VideoQMax 30
VideoSize 640x480
VideoIntraOnly
Noaudio

Strict -1
</Stream>
```


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

**pyinstaller**  
```python
# pyav_app.py
import os
# to link ffmpeg dll in executable
os.environ['PATH'] += os.pathsep + os.getcwd() + os.pathsep + os.path.dirname(os.getcwd())

def main():
    app = App()
    app.run()

if __name__ == '__main__':
    main()



# pyav_app.sepc

import sys
sys.setrecursionlimit(10000)

import re
import glob
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

av_hidden_imports = collect_submodules("av")
av_remove_key = ['avcodec-58.dll', 'avfilter-7.dll', 'avutil-56.dll', 'avformat-58.dll',
                 'swscale-5.dll', 'swresample-3.dll', 'avdevice-58.dll', 'postproc-55.dll']

a = Analysis(['Multiplayer.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[('opencv_ffmpeg341_64.dll','.')],
             hiddenimports=['fractions','numpy'] + av_hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=['PyQt4', 'PyQt5'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

Key = ['mkl'] + av_remove_key #,'libopenblas']

def remove_from_list(input, keys):
        outlist = []
        for item in input:
            name, _, _ = item
            flag = 0
            
            for key_word in keys:
                if name.find(key_word) > -1:
                    if name.find('dll') > -1:
                        flag = 1
            if flag == 1:
                print(name,'skip!!!!!!!!!!!!!!!!!!!!!!!')
            else:
                print(name,'append!!!!!!!!!!!!!!!!!!!!!!!')
                outlist.append(item)
            
        return outlist
    a.binaries = remove_from_list(a.binaries, Key)

exe = EXE(pyz,
	  a.scripts,
	  a.binaries,
	  a.zipfiles,
	  a.datas,
	  exclude_binaries=False,#True,
	  name='Multiplayer',
	  debug=False,
	  strip=False,
	  upx=True,
	  console=True,
	  icon='LOGO_Augentix_icon.ico')
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

## Cross compile  

* Compile ffmpeg in window (https://superuser.com/questions/1425350/how-to-compile-the-best-version-of-ffmpeg-for-windows)
* Also in git(https://github.com/m-ab-s/media-autobuild_suite)

<details>
	<summary>cross compile example</summary>

// workspace

sudo apt-get install mingw-w64
https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/host/x86_64-w64-mingw32-4.8
```
$workspace/
$workspace/ffmpeg_build/build
$workspace/ffmpeg_build/source/FFmpeg
$workspace/ffmpeg_build/source/install_nasm.sh
$workspace/ffmpeg_build/source/install_sdl.sh
$workspace/ffmpeg_build/source/install_libx265.sh
$workspace/ffmpeg_build/source/install_other.sh
$tools/x86_64-w64-mingw32
```
// sdl2 make

for decoder only
```
// ffmpeg_sources/FFmpeg
/* configure */
if enabled sdl2; then
   - SDL2_CONFIG="{cross_prefix}sdl2-config" 
   + SDL2_CONFIG="sdl2-config" 

PATH=$PATH:$SDL_BUILD_PATH/bin ./configure \
--arch=x86 \
--target-os=mingw32 \
--cross-prefix=$tools/x86_64-w64-mingw32-4.8/bin/x86_64-w64-mingw32- \
--enable-shared \
--prefix=$workspace/ffmpeg_build/build/FFmpeg/install \
--enable-sdl2
```
```
// ffmpeg_sources/install_nasm.sh
wget https://www.nasm.us/pub/nasm/releasebuilds/2.13.03/nasm-2.13.03.tar.bz2 && \
    tar xjvf nasm-2.13.03.tar.bz2 && \
    cd nasm-2.13.03 && \
    ./autogen.sh && \
    PATH="$HOME/bin:$PATH" ./configure --prefix="$workspace/ffmpeg_build/build" --bindir="$HOME/bin" && \
    make && \
    make install
```
```
// ffmpeg_sources/install_sdl.sh
wget https://www.libsdl.org/release/SDL2-2.0.10.tar.gz && \
tar xvzf SDL2-2.0.10.tar.gz && \
cd SDL2-2.0.10 && \
PATH=$PATH:$tools/x86_64-w64-mingw32/bin ./configure --prefix=$workspace/ffmpeg_build/build/sdl2-2.0.0.10 \
--host=x86_64-w64-mingw32 \
&& \
make -j16 -s && \
make install
```
</details>
