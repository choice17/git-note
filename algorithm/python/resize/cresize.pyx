import numpy as np
cimport cython
from cython.view cimport array
"""
https://docs.python.org/3/library/struct.html#format-characters
http://opencvpython.blogspot.com/2012/06/fast-array-manipulation-in-numpy.html
"""

cdef int FBIT = 13
cdef int HBIT = 1 << (FBIT - 1)
cdef int VBIT = 1 << FBIT

ctypedef unsigned char uint8

@cython.cdivision(True)
cdef inline int cCR(int x, int y):
    return (x << FBIT) / y

cdef inline int cSR(int x):
    return (x + HBIT) >> FBIT

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef uint8[:,:,:] cresizeANN(uint8 [:,:,:] im, int w, int h):
    cdef int ih, iw, ic
    cdef int w_r, h_r, p, i, j, k
    ih = int(im.shape[0])
    iw = int(im.shape[1])
    ic = int(im.shape[2])
    cdef uint8[:,:,:] img = array(shape=(h,w,ic), itemsize=sizeof(uint8), format='B')
    w_r = cCR(iw,w)
    h_r = cCR(ih,h)
    p = 0

    for i in range(h):
        hi = cSR(i * h_r)
        for j in range(w):
            wi = cSR(j * w_r)
            for k in range(ic):
                img[i,j,k] = im[hi, wi, k]
    return img

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef uint8[:,:,:] cresizeABL(uint8[:,:,:] im, int w, int h):
    cdef int im_h, im_w, im_c, h_r, w_r, i, j, k
    cdef int h0, n_h0, n_h1, h0V, w0, n_w0, n_w1, w0V
    cdef int row_pix0, row_pix1
    im_h = int(im.shape[0])
    im_w = int(im.shape[1])
    im_c = int(im.shape[2])
    h_r = cCR(im_h, h)
    w_r = cCR(im_w, w)
    cdef uint8[:,:,:] img = array(shape=(h,w,im_c), itemsize=sizeof(uint8), format='B')

    for j in range(h):
        h0 = j * h_r
        n_h0 = h0 >> FBIT 
        n_h1 = n_h0 + 1
        h0 = (h0 + HBIT) % VBIT
        h0V = VBIT-h0
        for k in range(w):
            w0 = k * w_r
            n_w0 = w0 >> FBIT 
            n_w1 = n_w0 + 1
            w0 = (w0 + HBIT) % VBIT
            w0V = VBIT-w0
            for i in range(im_c):
                row_pix0 = cSR((im[n_h0, n_w0, i] * w0 + im[n_h0, n_w1, i] * w0V))
                row_pix1 = cSR((im[n_h1, n_w0, i] * w0 + im[n_h1, n_w1, i] * w0V))
                img[j, k, i] = cSR((row_pix0 * h0 + row_pix1 * h0V))
                #img[j, k, i] = CLIP(img[j, k, i], 0, 255)
    return img
