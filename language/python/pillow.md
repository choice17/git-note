# pillow  

* **[open](#open)**  
* **[withnumpy](#withnumpy)**  

## open  
> image_file = 'levi.jpg'  
```python 
from PIL import Image as IMG  
img = IMG.open(image_file)
print(img.size)
>> 320,480,3  
img_vector = img.getdata()
print(len(img_vector))
>> 460800  
```

## withnumpy  
in python3, image datatype is compatible to numpy array  
for example  
```python  
img = IMG.open(image_file)
img_array = np.array(img)
crop_threshold = 40
img_array = img_array[:,crop_threshold:-crop_threshold,:]
img = IMG.fromArray(img_array)
img.save('levi.bmp')
```

# opencv  

* **[imread](#imread)**  
* **[videocapture](#videocapture)**  
* **[draw](#draw)**  
* **[face_detector](#face_detector)**  

## imread  
```python 
import cv2
```

## videocapture

```python 
import cv2 
import sys
url = 0 #(check for device number), rtsp/ http/ ...   
cap = cv2.VideoCapture(url)
if cap.isOpened():
	sys.exit()
cv2.namedWindow(url, cv2.WindowNormal)
while True:

	if cv2.getWindowProperty(url,0) == -1:
		cap.release()
		sys.exit()

	flag, img = cap.read()
	if flag:
		#img = cv2.cvtColor(img,cv2.BGR2RGB)
		img = img[:,:,::-1]
		cv2.imshow(url,img)
		k = cv2.waitKey(0)
		if k == ord('q'):
			cap.release()
			cv2.destroyAllWindows()
			sys.exit()
```

## draw  
refer to [draw](https://docs.opencv.org/3.1.0/dc/da5/tutorial_py_drawing_functions.html)  
```python
cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)
```
```python
cv2.circle(img,(447,63), 63, (0,0,255), -1)
```
```python
cv2.ellipse(img,(256,256),(100,50),0,0,180,255,-1)
```
and draw with text 
```python
font = cv2.FONT_HERSHEY_SIMPLEX # font style
text_string = 'OpenCV'
position = (10,500) # x,y
font_scale = 4
color = (255,255,255) #white
linewidth = 2
cv2.putText(img, 
	        text_string, 
	        position, 
	        font, 
	        font_scale,
	        color,
	        linewidth,
	        cv2.LINE_AA)
```

	
