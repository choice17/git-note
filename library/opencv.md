# OPENCV

**Content**    
* **[installation](#installation)**  
* **[videocapture](#videocapture)**  
* **[waitKey](#waitkey)**  
* **[namedwindow](#namedwindow)**  
* **[rect](#rect)**  
* **[circle](#circle)**  
* **[line](#line)**  
* **[selfdefinedmarker](#selfdefinemarker)**  
* **[polyfill](#polyfill)**  
* **[facedetection](#facedetection)**  
* **[cross-compile-ffmpeg](#compile)**  

## installation 

Python 

```bash
pip install opencv-python==x.x.x 
```

C++  
* window
```bash  
wget link-to-source  
cmake gui 
> choose source
> select build folder 
> select compiler (vs14) or (codeblock) <-- IDE dependent  
> config
> generate 

if vs14
> open opencv.sln in {PATH}/opencv/build
> install 
> build
> test on example
> in new project 
> add linker 
> add lib 
> add bin  

if codeblock 
> open opencv.cpb in {PATH}/opencv/build
> build
> install
> test on example
> in new proj
> add linker
> add lib
> add bin
```

* linux
```bash 
> sudo apt-get update
> sudo apt-get install build-essential make cmake gcc g++ 
> wget {link-to-opencv-source} {opencv-contrib}
> unzip {opencv.zip} {opencv-contrib.zip}
> cd {opencv}
> mkdir build
> cmake -Dlist-of-option
> cd build 
> make
> make install 
```

## videocapture  

## waitkey  

The most simple usage of VideoCapture()  

```python  
import cv2

cap = cv2.VideoCapture(url) # or 0-N or camera device  

if not cap.isOpened():      # check if it can seek url
    exit()

while True:
    f, fr = cap.read()
    if f:
        cv2.imshow(url, fr)
else:
    	cap.release()
        exit()
    K = cv2.waitKey(1)      # waitkey is 4 window refresh
    if K in [27, ord('q'):  # esc-27, key-q = ord('q')
        cap.release()
	exit()


```

## namedwindow  

```python  
cap = cv2.VideoCapture(url)

'''1. create namedWindow
where flags are 
:None - fixed window size with img size
:cv2.WINDOW_NORMAL - allow window auto resize  
:cv2.WINODW_OPENGL - need to be compiled during building opencv'''

cv2.namedWindow(url, {flag})
cv2.windowResize(url, (w, h)) 

while cv2.getWindowProperties(url, -1) != 0:
    f, fr = cap.read()
    if f:
    	cv2.imshow(url, fr)
    else:
        break

cap.release()
cv2.destroyAllWindows() # explicit detroy windows if there is further steps
```

## imread  

fname = 'lena.jpg'
img =  cv2.imread(fname)
img = cv2.cvtColor(img, cv2.BGR2RGB)  # cv2 default chn is bgr  

## resize  

```python
'''resize
params
=======
:dsize - (w,h), if 0, then outputw = fx*x
:fx - x ratio 
:fy - y ratio  
'''

img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5) # if dsize=(0,0)
# or 
img = cv2.resize(img, (640, 480))

```

## rect  

```python
cv2.rect(img, (pt1x, pt1y), (pt2x, pt2y), {linewidth:int}, {color:(chn1,2,3)}, cv2.LINE_AA)
```

## circle  

```python  
cv2.circle(img, (x, y), radius, {linewidth:int * -1=fill}, {color:(chr1,2,3)})
```

## selfdefinedmarker  

## polyfill  

```python  
import numpy as np

class Tri(object):
    def __init__(self):
    	self.coord=np.array([
		[0, 2],
		[-2, 1],
		[2, 1]])
    def transform(self, rotation: float, shift: tuple):
	
	
        return self
	
    def shift(self, x, y):
    	return self

    def getvertices(self):
    	return self.coord

    def rotation(self, angle: float):
    '''rotation by angle
    params:
    ========
    :angle - radian in float +ve anticlock
    ''''
    	return self.coord


cv2.polyfill(img, [Tri().transform(11/7, (100, 100))], (0, 255, 0))

```

## facedetection   

using vialo jones cascade face detector 
1. use integral image  
2. training using adaboost on haar features
3. cascade the haar feature detection  
4. searching for image pyramid

```python 

img = cv2.imread(fname)

detector = cv2.cascadeDetector('{facedetector.xml}')

result_boxes = detector.detect(img)  

```

## compile  

https://www.freedesktop.org/wiki/Software/pkg-config/CrossCompileProposal/

After cross-compile ffmpeg, we have to export pkg-config-path and ld-library-path  
note. CMAKE prerequisite. cmake, pkg-config

example configure for cross-compile ffmpeg, it should enable avresample  

```
./configure --prefix=$HOME/env/arm/ffmpeg --shlibdir=$HOME/env/arm/ffmpeg/share --disable-ffplay --arch=armv7a --cross-prefix=${CROSS_COMPILE} --target-os=linux --extra-cflags="-mfloat-abi=softfp" --extra-cxxflags="-mfloat-abi=softfp" --enable-avresample
```

```
export LD_LIBRARY_PATH=$HOME/env/arm/ffmpeg/lib:$LD_LIBRARY_PATH
export C_INCLUDE_PATH=$HOME/env/arm/ffmpeg/include:$C_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=$HOME/env/arm/ffmpeg/include:$CPLUS_INCLUDE_PATH
export PKG_CONFIG_PATH=$HOME/env/arm/ffmpeg/lib/pkgconfig:$PKG_CONFIG_PATH
# for /usr/bin/pkgconfig
export SYSROOT=/usr/bin/
export PKG_CONFIG_SYSROOT_DIR=${SYSROOT}
export PKG_CONFIG_LIBDIR=${SYSROOT}
```

setup toolchain file or toolchain config in cmake-gui

```
/* toolchain.make */
set( CMAKE_SYSTEM_NAME Linux)
set( CMAKE_SYSTEM_PROCESSOR arm )
set( CMAKE_C_COMPILER ${CROSS_PREFIX}gcc )
set( CMAKE_CXX_COMPILER ${CROSS_PREFIX}g++ )
set( CMAKE_INSTALL_PREFIX ${INSTALL_PREFIX} )


http://www.theeureka.net/blog/tag/cross-compile-opencv/

opencv        $ cd build
opencv/build/ $ cmake .. -DCMAKE_TOOLCHAIN_FILE=../toolchain.make
```

or config toolchain in cmake

```
cmake .. \
-DCMAKE_BUILD_TYPE=Release \
-DCMAKE_C_FLAGS=-mfloat-abi=softfp \
-DCMAKE_CXX_FLAGS=-mfloat-abi=softfp \
-DBUILD_DOCS=0 \
-DBUILD_EXAMPLES=0 \
-DBUILD_JASPER=1 \
-DBUILD_JAVA=0 \
-DBUILD_JPEG=1 \
-DBUILD_PNG=1 \
-DBUILD_PROTOBUF=1 \
-DBUILD_SHARED_LIBS=1 \
-DBUILD_TESTS=0 \
-DBUILD_ZLIB=1 \
-DBUILD_opencv_java_buildings_generator=0 \
-DBUILD_opencv_js=0 \
-DBUILD_opencv_python_bindings_generator=0 \
-DBUILD_opencv_ts=0 \
-DBUILD_opencv_world=1 \
-DBUILD_TESTS=0 \
-DCMAKE_AR=${CROSS_COMPILE}ar \
-DCMAKE_C_COMPILER=${CROSS_COMPILE}gcc \
-DCMAKE_CXX_COMPILER=${CROSS_COMPILE}g++ \
-DCMAKE_FIND_ROOT_PATH=${CROSS_COMPILE_SYSROOT} \
-DCMAKE_LINKER=${CROSS_COMPILE}ld \
-DCMAKE_NM=${CROSS_COMPILE}nm \
-DCMAKE_OBJCOPY=${CROSS_COMPILE}objcopy \
-DCMAKE_OBJDUMP=${CROSS_COMPILE}objdump \
-DCMAKE_RANLIB=${CROSS_COMPILE}ranlib \
-DCMAKE_STRIP=${CROSS_COMPILE}strip \
-DCMAKE_SYSTEM_NAME=Linux \
-DCMAKE_STRIP=${CROSS_COMPILE}strip \
-DCMAKE_INSTALL_PREFIX=$HOME/opencv/install \
-DWITH_PNG=0 \
-DWITH_PROTOBUF=0 \
-DWITH_PTHREADS_PF=0 \
-DWITH_FFMPEG=1
```
