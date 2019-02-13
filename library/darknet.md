# Darknet 

## Reference  

* **[Official Github page](https://github.com/pjreddie/darknet.git)**  
* **[Official Webpage](https://pjreddie.com/darknet/yolo/)**  
* **[Pretrained Weight](#weights)**  
* **[Sample Command](#commands)**  
* **[Build Flow - Window](#buildflow)**  
* **[Python API](#./darknet/darknet.py)**  

## python api  

* Directory  
```python
~/darknet/
         |-darknet.py
         |-libdarknet.so
         |-cfg/
         |    |-yolov3-tiny.cfg
         |    |-coco.data
         |-weights/
         |        |-yolov3-tiny.weights
         |-data/
         |     |-coco.names

```  
* Makefile  

This make file is targeted to Window environment
To get rid of make error, we can simply ignore example/go.o.  

## buildflow  

To build in master branch newest commit 61c9d02ec461e30d5 in windows.  
You may need to do 3 steps.

* Step0. Prerequisite mingw-64 in your window environ with Msys  
* Step1. Add <time.h> in include/darknet.h  
* Step2. Remove go.o in Makefile  
* Step3. Comment out the run_go() function in examples/darknet.c  

Then a simple make call in console should work it out.

## weights

* [yolov2-tiny-voc](https://pjreddie.com/media/files/yolov2-tiny-voc.weights)
* [yolov2](https://pjreddie.com/media/files/yolov2.weights)
* [yolov2-voc](https://pjreddie.com/media/files/yolov2-voc.weights)
* [yolov3-tiny-coco](https://pjreddie.com/media/files/yolov3-tiny.weights)  
* [yolov3-coco](https://pjreddie.com/media/files/yolov3.weights)


## commands  


* detection  
`./darknet detector test cfg/coco.data cfg/yolov3.cfg yolov3.weights data/dog.jpg`  

* detection on camera using CUDA and OPENCV  
`./darknet detector demo cfg/coco.data cfg/yolov3.cfg yolov3.weights`  

* train on detection  
`./darknet detector train cfg/voc.data cfg/yolov3-voc.cfg darknet53.conv.74`

