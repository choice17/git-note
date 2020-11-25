from ctypes import *

class IMAGE(Structure):
    _fields_ = [("data",c_void_p),
                ("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("size", c_int)]

class COLOR(Structure):
    _fields_ = [("r", c_int),
                ("g", c_int),
                ("b", c_int)]

libfile = "algo.so"
algo = CDLL(libfile, RTLD_GLOBAL)
algo.printstr.argtypes = [c_char_p]
algo.fill.argtypes = [POINTER(IMAGE), POINTER(COLOR)]
algo.run.argtypes = [POINTER(IMAGE)]

import numpy as np

w = 5
h = 4
c = 3
size = w * h * c * 1
r = 255
g = 233
b = 12
img = np.zeros((h,w,c),dtype=np.uint8)
cimg = IMAGE(img.__array_interface__['data'][0], w, h, c, size)
ccolor = COLOR(r, g, b)
#cimg = IMAGE(c_void_p(img.__array_interface__['data'][0]),
#      c_int(w), c_int(h), c_int(c), c_int(size))
import time
D = 1
def f(*args):
    if D:
        print(*args)

jstr = b'{\"od\":\"idx\":1,"rect":[0,0,1,2]}}'
algo.printstr(jstr)

f(img[:,:,0])
f(img[:,:,1])
f(img[:,:,2])
print(">>>>>>>>>>>>>")
ti = time.time()
algo.fill(byref(cimg), byref(ccolor))
print(time.time() - ti)
algo.run(byref(cimg))
t = 10
while (t):
    time.sleep(1)
    f(img[:,:,0])
    f(img[:,:,1])
    f(img[:,:,2])
    t -= 1

algo.cclose()
print("exit python programstar")