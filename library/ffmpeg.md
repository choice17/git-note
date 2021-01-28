# FFMPEG 

* **Content**  
* **[ffmpeg](#ffmpeg)**  
* **[ffprobe](#ffprobe)**  
* **[ffplay](#ffplay)**  
* **[ffserver](#ffserver)**  
* **[libav](#libav)**  
* **[sdl](#sdl)**  
* **[compile](#compile)**  
* **[ffmpeg_c_api](#c_api)**  

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

build example

```python
## pyav_app.py
import os
## to link ffmpeg dll in executable
os.environ['PATH'] += os.pathsep + os.getcwd() + os.pathsep + os.path.dirname(os.getcwd())

def main():
    app = App()
    app.run()

if __name__ == '__main__':
    main()

## pyav_app.sepc

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

### c_api  

<details>
<summary>open media</summary>

```c
int open_media(const char *filename, AVFormatContext **avFmtCtx)
{
	*avFmtCtx = avformat_alloc_context();
	if (!*avFmtCtx) {
		printf("failed to alloc memory for format");
		return -1;
	}

	if (avformat_open_input(avFmtCtx, filename, NULL, NULL) != 0) {
		printf("failed to open input file %s", filename);
		return -1;
	}

	if (avformat_find_stream_info(*avFmtCtx, NULL) < 0) {
		printf("failed to get stream info");
		return -1;
	}

	return 0;
}
```

</details>

<details>
<summary>fill_codec_info</summary>

```c
int fill_codec_info(AVStream *av_stream, AVCodec **av_codec, AVCodecContext **av_codecCtx)
{
	*av_codec = avcodec_find_decoder(av_stream->codecpar->codec_id);
	if (!*av_codec) {
		printf("failed to find the codec");
		return -1;
	}

	*av_codecCtx = avcodec_alloc_context3(*av_codec);
	if (!*av_codecCtx) {
		printf("failed to alloc memory for codec context");
		return -1;
	}

	if (avcodec_parameters_to_context(*av_codecCtx, av_stream->codecpar) < 0) {
		printf("failed to fill codec context");
		return -1;
	}

	if (avcodec_open2(*av_codecCtx, *av_codec, NULL) < 0) {
		logging("failed to open codec");
		printf -1;
	}

	return 0;
}

```

</details>

<details>
<summary>prepare_encoder</summary>

```c
int prepare_encoder(StreamingContext *encoder, AVCodecContext *decoder_ctx, AVRational input_framerate,
                    StreamingParams sp)
{
	encoder->video_stream = avformat_new_stream(encoder->avFmtCtx, NULL);

	encoder->video_codec = avcodec_find_encoder_by_name(sp.video_codec);
	if (!encoder->video_codec) {
		printf("could not find the proper codec");
		return -1;
	}

	encoder->video_codecCtx = avcodec_alloc_context3(encoder->video_codec);
	if (!encoder->video_codecCtx) {
		printf("could not allocated memory for codec context");
		return -1;
	}

	av_opt_set(encoder->video_codecCtx->priv_data, "preset", "main", 0);
	if (sp.codec_priv_key && sp.codec_priv_value) {
		av_opt_set(encoder->video_codecCtx->priv_data, sp.codec_priv_key, sp.codec_priv_value, 0);
	}
	encoder->video_codecCtx->height = decoder_ctx->height;
	encoder->video_codecCtx->width = decoder_ctx->width;
	encoder->video_codecCtx->sample_aspect_ratio = decoder_ctx->sample_aspect_ratio;

	if (encoder->video_codec->pix_fmts) {
		encoder->video_codecCtx->pix_fmt = encoder->video_codec->pix_fmts[0];
	} else {
		encoder->video_codecCtx->pix_fmt = decoder_ctx->pix_fmt;
	}

	encoder->video_codecCtx->bit_rate = 2 * 1000 * 1000;
	encoder->video_codecCtx->rc_buffer_size = 4 * 1000 * 1000;
	encoder->video_codecCtx->rc_max_rate = 2 * 1000 * 1000;
	encoder->video_codecCtx->rc_min_rate = 2.5 * 1000 * 1000;

	encoder->video_codecCtx->time_base = av_inv_q(input_framerate);
	encoder->video_stream->time_base = encoder->video_codecCtx->time_base;

	if (avcodec_open2(encoder->video_codecCtx, encoder->video_codec, NULL) < 0) {
		printf("could not open the codec");
		return -1;
	}
	avcodec_parameters_from_context(encoder->video_stream->codecpar, encoder->video_codecCtx);
	return 0;
}


```

</details>

<details>
<summary>transform_pix_fmt</summary>

```c
int transform_pix_fmt(AVFrame *in_frame, AVFrame *out_frame, AVCodecContext *pCodecContext,
                           enum AVPixelFormat in_pixFmt, enum AVPixelFormat out_pixFmt)
{
	struct SwsContext *sws_ctx;

	sws_ctx = sws_getContext(pCodecContext->width, pCodecContext->height, in_pixFmt, pCodecContext->width,
	                         pCodecContext->height, out_pixFmt, SWS_BILINEAR, NULL, NULL, NULL);

	sws_scale(sws_ctx, (uint8_t const *const *)in_frame->data, in_frame->linesize, 0, pCodecContext->height,
	          out_frame->data, out_frame->linesize);

	return 0;
}


```

</details>

<details>
<summary>yuv420_to_rgb</summary>

```c
int yuv420_to_rgb(AVFrame *pFrame, FrameImage *image)
{
	int size_per_channel = image->width * image->height;
	int u_value, v_value;

	memcpy(image->data, pFrame->data[0], size_per_channel);

	for (int y = 0; y < image->height; y += 2) {
		for (int x = 0; x < image->width; x += 2) {
			u_value = *(pFrame->data[1] + pFrame->linesize[1] * y / 2 + x / 2);
			image->data[size_per_channel + y * image->width + x] = u_value;
			image->data[size_per_channel + y * image->width + x + 1] = u_value;
			image->data[size_per_channel + (y + 1) * image->width + x] = u_value;
			image->data[size_per_channel + (y + 1) * image->width + x + 1] = u_value;

			v_value = *(pFrame->data[2] + pFrame->linesize[2] * y / 2 + x / 2);
			image->data[2 * size_per_channel + y * image->width + x] = v_value;
			image->data[2 * size_per_channel + y * image->width + x + 1] = v_value;
			image->data[2 * size_per_channel + (y + 1) * image->width + x] = v_value;
			image->data[2 * size_per_channel + (y + 1) * image->width + x + 1] = v_value;
		}
	}
	return SUCCESS;
}



```

</details>

<details>
<summary>decode_packet</summary>

```c
int decode_packet(AVCodecContext *pCodecContext, AVPacket *input_packet, AVFrame *output_frame, int frame_no)
{
	int response = avcodec_send_packet(pCodecContext, input_packet);

	if (response < 0) {
		return FAILURE;
	}

	while (response >= 0) {
		response = avcodec_receive_frame(pCodecContext, output_frame);
		if (response == AVERROR(EAGAIN) || response == AVERROR_EOF) {
			break;
		} else if (response < 0) {
			return -1;
		}

		if (response >= 0) {
			if (frame_no == pCodecContext->frame_number - 1) {
				return 0;
			}
		}
	}
	return 0;
}




```

</details>

<details>
<summary>encode_pkt</summary>

```c
static void encode_pkt(AVCodecContext *enc_ctx, AVFrame *frame, AVPacket *pkt, FILE *outfile)
{
	int ret;

	if (frame)
		printf("Send frame %3" PRId64 "\n", frame->pts);

	ret = avcodec_send_frame(enc_ctx, frame);
	if (ret < 0) {
		printf(stderr, "Error sending a frame for encoding\n");
		exit(1);
	}

	while (ret >= 0) {
		ret = avcodec_receive_packet(enc_ctx, pkt);
		printf("error msg %s", av_err2str(ret));
		if (ret == AVERROR(EAGAIN)) {
			logging("it is EAGAIN");
		}
		if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
			break;
		else if (ret < 0) {
			printf("Error during encoding\n");
			exit(1);
		}
		fwrite(pkt->data, 1, pkt->size, outfile);
	}
	av_packet_unref(pkt);
}

```

</details>

<details>
	<summary> allocate frame buffer </summary>

```
int alloc_frame_dataBuf(AVFrame *pFrame, AVCodecContext *pCodecContext, enum AVPixelFormat pixFmt, uint8_t **buffer)
{
	int numBytes = av_image_get_buffer_size(pixFmt, pCodecContext->width, pCodecContext->height, 1);

	*buffer = (uint8_t *)av_malloc(numBytes * sizeof(uint8_t));

	return 0;
}
```
</details>

<details>
	<summary> fetch frame by number </summary>
	
```
int fetch_frame_by_nb(char* filename, int frame_nb, Image *image)
{

	AVPacket *input_packet = NULL;
	AVFormatContext *avFmtCtx = NULL;
	AVCodecContext *avCodexCtx = NULL;
	AVCodec *codec;
	AVFrame *input_frame;
	AVFrame *output_frame;

	open_media(filename, &avFmtCtx);
	prepare_decoder(decoder);

	input_frame = av_frame_alloc();
	output_frame = av_frame_alloc();

	uint8_t *output_buffer = NULL;
	alloc_frame_dataBuf(output_frame, decoder->video_codecCtx, AV_PIX_FMT_YUV444P, &output_buffer);

	av_image_fill_arrays(output_frame->data, output_frame->linesize, output_buffer, AV_PIX_FMT_YUV444P,
	                     decoder->video_codecCtx->width, decoder->video_codecCtx->height, 1);

	input_packet = av_packet_alloc();

	int start = 0;
	int nb_gop = -1;
	int i = 0;
	int target_gop = frame_no / 20;
	frame_no = frame_no % 20;
	while (av_read_frame(decoder->avFmtCtx, input_packet) >= 0) {
		if (decoder->avFmtCtx->streams[input_packet->stream_index]->codecpar->codec_type ==
		    AVMEDIA_TYPE_VIDEO) {
			char *data = input_packet->data + 4;
			if (*data == 0x67) nb_gop++;
			if (nb_gop == target_gop && *data == 0x67) start = 1;

			if (start == 1) {
				response = decode_packet(decoder->video_codecCtx, input_packet, input_frame, frame_no);

				if (response == FAILURE) {
					printf("failure to decode packet");
					break;
				}

				else if (response == FINISH) {
					transform_pixel_format(input_frame, output_frame, decoder->video_codecCtx,
					                           AV_PIX_FMT_YUV420P, AV_PIX_FMT_YUV444P);
					avframe_to_image(input_frame, image);
					break;
				}
			}
		}
		av_packet_unref(input_packet);
	}

	av_packet_free(&input_packet);
	av_frame_free(&input_frame);
	av_frame_free(&output_frame);

	avformat_close_input(&avFmtCtx);
	avformat_free_context(avFmtCtx);
	decoder->avFmtCtx = NULL;

	avcodec_free_context(&video_codecCtx);
	video_codecCtx = NULL;

	return SUCCESS;
}
```

</details>


<details>
<summary> basic video file decode encode pipeline </summary>
	
```c
// setup input av info
AVFormatContext *ipFormatContext = NULL;
AVPacket *ipPacket = NULL;
ipFormatContext = avformat_alloc_context();
ret = avformat_open_input(&ipFormatContext, filename, NULL, NULL);

// setup output codec variable
AVFormatContext *opFormatContext = NULL;
AVCodecContext *opvideo_codecCtx = NULL;
AVPacket *opPacket = NULL;
AVCodec *opvideo_codec;

// setup output/encoder info
FILE *fp_out = fopen(out_file_name, "wb");
avformat_alloc_output_context2(&opFormatContext, NULL, NULL, ofilename);
opvideo_codec = avcodec_find_encoder(AV_CODEC_ID_H264);
opvideo_codecCtx = avcodec_alloc_context3(ovideo_codec);

opvideo_codecCtx->bit_rate = 2000000;
opvideo_codecCtx->width = 1920;
opvideo_codecCtx->height = 1080;
opvideo_codecCtx->framerate = (AVRational){ 25, 1 };
opvideo_codecCtx->time_base = (AVRational){ 1, 25 };

opvideo_codecCtx->gop_size = 10;
opvideo_codecCtx->max_b_frames = 0;
opvideo_codecCtx->pix_fmt = AV_PIX_FMT_YUV420P;

if (opvideo_codec->id == AV_CODEC_ID_H264) {
  av_opt_set(opvideo_codecCtx->priv_data, "preset", "slow", 0); // for high profile
}

if (avcodec_open2(opvideo_codecCtx, ovideo_codec, NULL) < 0) {
    printf("Could not open codec: %s", av_err2str(ret));
}

// setup encoder image format
AVFrame *input_frame = av_frame_alloc();
if (!input_frame) {
	printf("failed to allocated memory for AVFrame");
	return -1;
}
input_frame->format = AV_PIX_FMT_YUV444P;
input_frame->width = ovideo_codecCtx->width;
input_frame->height = ovideo_codecCtx->height;
av_frame_get_buffer(input_frame, 0);

// setup encoder output frame
AVFrame *output_frame = av_frame_alloc();
if (!output_frame) {
    printf("failed to allocated memory for AVFrame");
    return -1;
}
output_frame->format = AV_PIX_FMT_YUV420P;
output_frame->width = ovideo_codecCtx->width;
output_frame->height = ovideo_codecCtx->height;
ret = av_frame_get_buffer(output_frame, 0);

// prepare decoder output packet
AVPacket *output_packet = av_packet_alloc();
if (!output_packet) {
    printf("could not allocate memory for output packet");
    return -1;
}

ipFormatContext = avformat_alloc_context();
if (avformat_open_input(ipFormatContext, filename, NULL, NULL) != 0) return FAILURE;

//Read packets of a media file to get stream information
//This is useful for file formats with no headers such as MPEG
if (avformat_find_stream_info(*ipFormatContext, NULL) < 0) {
	printf("failed to get stream info");
	return -1;
}

struct SwsContext *sws_ctx;
sws_ctx = sws_getContext(ipCodecContext->width, ipCodecContext->height, AV_PIX_FMT_YUV444P, opCodecContext->width,
			 opCodecContext->height, AV_PIX_FMT_YUV420P, SWS_BILINEAR, NULL, NULL, NULL);

int f_nb = 0;
for (int j = 0; j < ipFormatContext->nb_streams; j++) {
    if (ipFormatContext->streams[j]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO) {
         ivideo_info->height = ipFormatContext->streams[j]->codecpar->height;
	 ivideo_info->width = ipFormatContext->streams[j]->codecpar->width;
   	 input_packet = av_packet_alloc();
	 output_packet = av_packet_alloc();
	 while (av_read_frame(ipFormatContext, ipPacket) >= 0) {
	 
	 	int response = avcodec_send_packet(ipCodecContext, input_packet);
		// decode frame
		if (response < 0) continue;
		while (response >= 0) { // receive_frame return frame number
			response = avcodec_receive_frame(ipCodecContext, input_frame);
			if (response == AVERROR(EAGAIN) || response == AVERROR_EOF) break; // success;
			else if (response < 0) break;//decode fail;
			if (response >= 0) {
				if (frame_no == ipCodecContext->frame_number - 1) response = -2;//finish;
		}
		
		// reformat image for encoder
		sws_scale(sws_ctx, (uint8_t const *const *)input_frame->data, input_frame->linesize, 0, opCodecContext->height,
	  	output_frame->data, output_frame->linesize);
		
		// do image processing here ...

		// make writable
		ret = av_frame_make_writable(output_frame);
		
		// update frame pts (frame number)
		output_frame->pts = f_nb++;

		// encode(encoder->video_codecCtx, output_frame, output_packet, fp_out);
		/* send the frame to the encoder */
		ret = avcodec_send_frame(opCodecContext, output_frame);
		if (ret < 0) exit(1);
		output_packet = 
		while (ret >= 0) {
			ret = avcodec_receive_packet(opvideo_codecCtx, output_packet);
			if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) break;
			else if (ret < 0) exit(1);
			printf("Write packet %3" PRId64 " (size=%5d)\n", output_packet->pts, output_packet->size);
			fwrite(output_packet->data, 1, output_packet->size, fp_out);
		}
		av_packet_unref(output_packet);
	}
     }
}

uint8_t endcode[] = { 0, 0, 1, 0xb7 };
encode(ovideo_codecCtx, NULL, output_packet, fp_out);
if (encoder->video_codec->id == AV_CODEC_ID_MPEG1VIDEO || encoder->video_codec->id == AV_CODEC_ID_MPEG2VIDEO)
    fwrite(endcode, 1, sizeof(endcode), fp_out);
fclose(fp_out);

avformat_free_context(opFormatContext);
avcodec_free_context(opvideo_codecCtx);

av_frame_free(&input_frame);
av_frame_free(&output_frame);

av_packet_free(&output_packet);

avformat_close_input(&ipFormatContext);
av_packet_free(&input_packet);
```
</details>

<details>
	<summary> encode frame</summary>
	
```c

int encode_frame(StreamingContext *decoder, StreamingContext *encoder, AVFrame *input_frame)
{
	input_frame->pict_type = AV_PICTURE_TYPE_NONE;
	AVPacket *output_packet = av_packet_alloc();
	response = avcodec_send_frame(encoder->video_codecCtx, input_frame);
	while (response >= 0) {
		response = avcodec_receive_packet(encoder->video_codecCtx, output_packet);
		if (response == AVERROR(EAGAIN) || response == AVERROR_EOF) break;
		else if (response < 0) goto fail;
		output_packet->stream_index = decoder->video_index;
		output_packet->duration = encoder->video_stream->time_base.den / encoder->video_stream->time_base.num /
		                          decoder->video_stream->avg_frame_rate.num *
		                          decoder->video_stream->avg_frame_rate.den;

		av_packet_rescale_ts(output_packet, decoder->video_stream->time_base, encoder->video_stream->time_base);
		response = av_interleaved_write_frame(encoder->avFmtCtx, output_packet);
		if (response != 0) {
			printf("Error %d while receiving packet from decoder: %s", response, av_err2str(response));
			goto fail;
		}
	}

	av_packet_unref(output_packet);
	av_packet_free(&output_packet);
	return SUCCESS;

fail:
	av_packet_unref(output_packet);
	av_packet_free(&output_packet);
	return FAILURE;

```
</details>

