# PYDICOM

## introduction  

pydicom is a image library to open .DCM image 

DCM file usually includes details MPI/patient information in the image header.  

## installation  

`pip install pydicom`  

## read as image  

```python  
import pydicom as D
import matplotlib.pyplot as plt

imagefile = "MR000000.DCM"
f = D.read_file(imagefile)
imgdata = f.pixel_array

# example
# imgdata.shape => [512, 512] 
# imgdata.max() => 602

plt.imshow(imgdata, cmap=plt.cm.bone)
plt.show()
```  
