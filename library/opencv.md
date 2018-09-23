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

