import numpy as np
cimport cython
from cython.view cimport array
"""
https://docs.python.org/3/library/struct.html#format-characters
"""
"""
https://homes.cs.washington.edu/~jmschr/lectures/Parallel_Processing_in_Python.html

access numpy array as pointer
"""
cdef int FBIT = 13
cdef int HBIT = 1 << (FBIT - 1)
cdef int VBIT = 1 << FBIT

cdef int SBIT = 5
cdef int hSBIT = 1 << (SBIT - 1)
cdef int vSBIT = 1 << SBIT

@cython.cdivision(False)
cdef inline int CR(int x, int y):
    return ((x << FBIT)/y)

@cython.cdivision(False)
cdef inline int DR(int x):
    return (x + HBIT) >> FBIT

_XINV = np.array([[-1,  3, -2,  0],
                 [ 3, -6, -3,  6],
                 [-3,  3,  6,  0],
                 [ 1,  0, -1,  0]], dtype=np.int32)
_cXINV = (_XINV << SBIT) / 6
_cYINV = _XINV.T

cdef int[:,:] XINV = _XINV
cdef int[:,:] cXINV = _cXINV.astype(np.int32)
cdef int[:,:] cYINV = _cYINV.astype(np.int32)

fXINV = _XINV.astype(np.float32)
fcXINV = _cXINV.astype(np.float32)
fcYINV = _cYINV.astype(np.float32)

ctypedef unsigned char uint8
ctypedef fused my_type:
    int
    double
    long long

ctypedef fused arr_type:
    int[:,:]
    double[:,:]
    long long[:,:]
    uint8[:,:]

cdef inline int clip(int x, int upper, int lower):
    x = upper if (x > upper) else x
    x = lower if (x < lower) else x
    return x

cdef inline float clipf(float x, float upper, float lower):
    x = upper if (x > upper) else x
    x = lower if (x < lower) else x
    return x

cdef inline float clipg(my_type x, my_type upper, my_type lower):
    x = upper if (x > upper) else x
    x = lower if (x < lower) else x
    return x

cdef inline int reflect(int x, int up, int low):
    x = -x if (x < low) else x
    x = (up+up-x) if (x > up) else x
    return x

@cython.cdivision(True)
cdef inline int cCR(int x, int y):
    return (x << FBIT) / y

cdef inline int cSR(int x):
    return (x + HBIT) >> FBIT

@cython.cdivision(True)
cdef inline int sCR(int x, int y):
    return (x << SBIT) / y

cdef inline int sSR(int x):
    return (x + hSBIT) >> SBIT


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef uint8[:,:,:] cresizeANN(uint8 [:,:,:] im, int h, int w):
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
cpdef uint8[:,:,:] cresizeFNN(uint8 [:,:,:] im, int h, int w):
    cdef int ih, iw, ic
    cdef int i, j, k
    cdef float w_r, h_r
    ih = int(im.shape[0])
    iw = int(im.shape[1])
    ic = int(im.shape[2])
    cdef uint8[:,:,:] img = array(shape=(h,w,ic), itemsize=sizeof(uint8), format='B')
    w_r = float(iw) / w
    h_r = float(ih) / h

    for i in range(h):
        ih = int((h_r * i))
        for j in range(w):
            iw = int((w_r * j))
            for k in range(ic):
                img[i,j,k] = im[ih, iw, k]
    return img

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef uint8[:,:,:] cresizeABL(uint8[:,:,:] im, int h, int w):
    cdef int im_h, im_w, im_c, h_r, w_r, i, j, k, tmp
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
        h0 = h0  - (n_h0 << FBIT)
        h0V = VBIT-h0
        for k in range(w):
            w0 = k * w_r
            n_w0 = w0 >> FBIT 
            n_w1 = n_w0 + 1
            w0 = w0 - (n_w0 << FBIT)
            w0V = VBIT-w0
            for i in range(im_c):
                row_pix0 = cSR((im[n_h0, n_w0, i] * w0V + im[n_h0, n_w1, i] * w0))
                row_pix1 = cSR((im[n_h1, n_w0, i] * w0V + im[n_h1, n_w1, i] * w0))
                img[j, k, i] = cSR((row_pix0 * h0V + row_pix1 * h0))
                #img[j, k, i] = CLIP(img[j, k, i], 0, 255)
    return img

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef uint8[:,:,:] cresizeFBL(uint8[:,:,:] im, int h, int w):
    cdef int im_h, im_w, im_c, i, j, k, tmp
    cdef int n_h0, n_h1, n_w0, n_w1
    cdef float h_r, w_r, h0, w0, h0V, w0V, row_pix0, row_pix1

    im_h = int(im.shape[0])
    im_w = int(im.shape[1])
    im_c = int(im.shape[2])
    h_r = (<float>im_h) / h
    w_r = (<float>im_w) / w
    cdef uint8[:,:,:] img = array(shape=(h,w,im_c), itemsize=sizeof(uint8), format='B')

    for j in range(h):
        h0 = h_r * j
        n_h0 = int(h0)
        n_h1 = int((h0+0.5))
        h0 -= n_h0
        h0V = 1.0-h0
        for k in range(w):
            w0 = w_r * k
            n_w0 = int(w0)
            n_w1 = int((n_w0+0.5))
            w0 -= n_w0
            w0V = 1.0-w0
            for i in range(im_c):
                row_pix0 = (<float>im[n_h0, n_w0, i]) * w0V + (<float>im[n_h0, n_w1, i]) * w0
                row_pix1 = (<float>im[n_h1, n_w0, i]) * w0V + (<float>im[n_h1, n_w1, i]) * w0
                img[j, k, i] = int(((row_pix0 * h0V) + (row_pix1 * h0)))
                #img[j, k, i] = CLIP(img[j, k, i], 0, 255)
    return img


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef uint8[:,:,:] cresizeABC(uint8[:,:,:] im, int h, int w):
    """
    @brief 
    Sample code:
    https://stackoverflow.com/questions/52700878/bicubic-interpolation-python
    
    BiCubic Interpolation explain:
    http://www.ahinson.com/algorithms_general/Sections/InterpolationRegression/InterpolationBicubic.pdf
    @param im = src image
    @param h = dst height
    @param w = dst width
    @retval img = resize 2d array with shape = (h, w)
    """
    cdef int ih, iw, ic, ih_, iw_
    cdef int h_r, w_r
    cdef int i, j, k, q
    cdef int y, _H, H, py, pyy
    cdef int x, _W, W, px, pxx

    ih = int(im.shape[0])
    iw = int(im.shape[1])
    ic = int(im.shape[2])

    cdef uint8[:,:,:] img = np.empty((h,w,ic),dtype=np.uint8)#array(shape=(h,w,ic), itemsize=sizeof(uint8), format='B')
    F = np.empty((4,4), dtype=np.int32)
    PPY = np.empty((4), dtype=np.int32)
    PPX = np.empty((4), dtype=np.int32)
    Cr = np.empty((4,4), dtype=np.int32)
    R = np.empty((4), dtype=np.int32)
    Cc = np.empty((4), dtype=np.int32)
    pix = np.empty((1), dtype=np.int32)

    PPY[3] = VBIT
    PPX[3] = VBIT

    ih_ = ih-1
    iw_ = iw-1

    h_r = CR(ih, h)
    w_r = CR(iw, w)
    
    for j in range(h):
        y = j * h_r
        _H = y >> FBIT
        H = _H << FBIT

        py = y - H
        pyy = DR(py * py)
        pyyy = DR(pyy * py)
        PPY[2] = py
        PPY[1] = pyy
        PPY[0] = pyyy

        for k in range(w):
            x = k * w_r
            _W = x >> FBIT
            W = _W << FBIT

            px = x - W
            pxx = DR(px * px)
            pxxx = DR(pxx * px)
            PPX[2] = px
            PPX[1] = pxx
            PPX[0] = pxxx

            d0w = clip(_W-1, iw_, 0)
            d1w = clip(_W  , iw_, 0)
            d2w = clip(_W+1, iw_, 0)
            d3w = clip(_W+2, iw_, 0) 
            for i in range(ic):
                for q in range(4):
                    d0h = clip(_H+q-1, ih_, 0)
                    F[q,0] = int(im[d0h, d0w, i])
                    F[q,1] = int(im[d0h, d1w, i])
                    F[q,2] = int(im[d0h, d2w, i])
                    F[q,3] = int(im[d0h, d3w, i])
                Cr = ((F@XINV) + HBIT) / VBIT
                #print('px:',px,'\n',PPX,'\n')
                #print("CR PPX",Cr.shape, PPX.shape, type(Cr), type(PPX), Cr.dtype, PPX.dtype)
                R  = (Cr@PPX + HBIT) / VBIT
                #np.true_divide(R , VBIT, out=R)
                Cc = (cYINV@R + HBIT) / VBIT
                #np.true_divide(Cc , VBIT, out=Cc)
                pix = (Cc@PPY + HBIT) / VBIT
                #np.true_divide(pix, VBIT, out=pix)
                px = clip(pix,255,0)
                img[j,k,i] = px
                #print((j,k,i),(img[j,k,i],pix))

    return img


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef uint8[:,:,:] cresizeFBC(uint8[:,:,:] im, int h, int w):
    """
    @brief 
    Sample code:
    https://stackoverflow.com/questions/52700878/bicubic-interpolation-python
    
    BiCubic Interpolation explain:
    http://www.ahinson.com/algorithms_general/Sections/InterpolationRegression/InterpolationBicubic.pdf
    @param im = src image
    @param h = dst height
    @param w = dst width
    @retval img = resize 2d array with shape = (h, w)
    """
    cdef int ih, iw, ic, ih_, iw_
    cdef float h_r, w_r
    cdef int i, j, k, q
    cdef float y, H, py, pyy, pyyy
    cdef float x, W, px, pxx, pxxx
    cdef int d0w, d1w, d2w, d3w
    cdef int d0h
    ih = int(im.shape[0])
    iw = int(im.shape[1])
    ic = int(im.shape[2])

    cdef uint8[:,:,:] img = np.empty((h,w,ic),dtype=np.uint8)#array(shape=(h,w,ic), itemsize=sizeof(uint8), format='B')
    #cdef float[:,:] F = np.empty((4,4), dtype=np.float32)
    #cdef float[:] PPY = np.empty((4), dtype=np.float32)
    #cdef float[:] PPX = np.empty((4), dtype=np.float32)
    #cdef float[:,:] Cr = np.empty((4,4), dtype=np.float32)
    #cdef float[:] R = np.empty((4), dtype=np.float32)
    #cdef float[:] Cc = np.empty((4), dtype=np.float32)
    #cdef int[:] pix = np.empty((1), dtype=np.int32)
    F = np.empty((4,4), dtype=np.float32)
    PPY = np.empty((4), dtype=np.float32)
    PPX = np.empty((4), dtype=np.float32)
    Cr = np.empty((4,4), dtype=np.float32)
    R = np.empty((4), dtype=np.float32)
    Cc = np.empty((4), dtype=np.float32)
    pix = np.empty((1), dtype=np.int32)
    PPY[3] = 1
    PPX[3] = 1

    ih_ = ih-1
    iw_ = iw-1

    h_r = float(ih) / h
    w_r = float(iw) / w
    
    for j in range(h):
        y = h_r * j
        H = <int> y
        py = y - H
        pyy = py * py
        pyyy = pyy * py
        PPY[2] = py
        PPY[1] = pyy
        PPY[0] = pyyy

        for k in range(w):
            x = k * w_r
            W = <int> x
            px = x - W
            pxx = px * px
            pxxx = pxx * px
            PPX[2] = px
            PPX[1] = pxx
            PPX[0] = pxxx
            d0w = <int> clipg(W-1, iw_, 0)
            d1w = <int> clipg(W  , iw_, 0)
            d2w = <int> clipg(W+1, iw_, 0)
            d3w = <int> clipg(W+2, iw_, 0) 
            for i in range(ic):
                for q in range(4):
                    d0h = <int> clipg((H+q-1), ih_, 0)
                    F[q,0] = float(im[d0h, d0w, i])
                    F[q,1] = float(im[d0h, d1w, i])
                    F[q,2] = float(im[d0h, d2w, i])
                    F[q,3] = float(im[d0h, d3w, i])

                Cr = F@fXINV
                R  = Cr@PPX
                Cc = fcYINV@R
                pix = Cc@PPY
                px = pix
                px = clip(<int>px, 255, 0)
                img[j,k,i] = <uint8> (px)
                #print((j,k,i),(img[j,k,i],pix))

    return img
"""
https://www.reddit.com/r/C_Programming/comments/3dbwy9/cython_2d_memoryview_to_c_pointer_error/
"""
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef void cdot(int[:,:] x, int[:,:] y, int[:,:] z, int h1, int w1, int h2, int w2, int bs):
    cdef int i, j, k, _sum
    _sum = 0
    if h2 == 0: 
        h2 = w2
    if bs==1:
        for i in range(h1):
            for j in range(w2):
                for k in range(w1):
                    _sum += x[i,k] * y[k,j]
                z[i,j] = cSR(_sum)
                _sum = 0
    elif bs==2:
        for i in range(h1):
            for j in range(w2):
                for k in range(w1):
                    _sum += x[i,k] * y[k,j]
                z[i,j] = sSR(_sum)
                _sum = 0
    else:
        for i in range(h1):
            for j in range(w2):
                for k in range(w1):
                    _sum += x[i,k] * y[k,j]
                z[i,j] = _sum
                _sum = 0
"""
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef int[:,:] Test(int[:,:] x, int[:,:] y, int bs) nogil:
    cdef int h1,w1,h2,w2
    h1 = x.shape[0]
    w1 = x.shape[1]
    h2 = y.shape[0]
    w2 = y.shape[1]
    #cdef int[:,:] z = np.zeros((h1,w2),dtype=np.int32)
    cdot(x,y,z,h1,w1,h2,w2,bs)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef int[:,:] cConv2d(int[:,:] x, int[:,:] y):
    cdef int h1,w1,h2,w2,h3,w3,padh,padw
    cdef int i,j,k,l
    h1 = x.shape[0]
    w1 = x.shape[1]
    h2 = y.shape[0]
    w2 = y.shape[1]
    h3 = h1 - (h2-1)
    w3 = w1 - (w2-1)
    padw = (h2-1)/2
    padh = (w2-1)/2
    cdef int[:,:] z = np.zeros((h3,w3),dtype=np.int32)
    for i in range(padh,h1-padh):
        for j in range(padw,w1-padw):
            for k in range()
"""

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef void zeros(arr_type x, int h, int w):
    cdef int i, j
    for i in range(h):
        for j in range(w):
                x[i,j] = 0

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef uint8[:,:,:] cresizeTBC(uint8[:,:,:] im, int h, int w):
    """
    @brief 
    Sample code:
    https://stackoverflow.com/questions/52700878/bicubic-interpolation-python
    
    BiCubic Interpolation explain:
    http://www.ahinson.com/algorithms_general/Sections/InterpolationRegression/InterpolationBicubic.pdf
    @param im = src image
    @param h = dst height
    @param w = dst width
    @retval img = resize 2d array with shape = (h, w)
    """
    cdef int ih, iw, ic, ih_, iw_
    cdef int h_r, w_r
    cdef int i, j, k, q
    cdef int y, _H, H, py, pyy
    cdef int x, _W, W, px, pxx

    ih = int(im.shape[0])
    iw = int(im.shape[1])
    ic = int(im.shape[2])
    ih_ = ih-1
    iw_ = iw-1

    cdef uint8[:,:,:] img = np.empty((h,w,ic),dtype=np.uint8)#array(shape=(h,w,ic), itemsize=sizeof(uint8), format='B')
    cdef int[:,:] F = np.empty((4,4), dtype=np.int32)
    cdef int[:,:] PPY = np.empty((4,1), dtype=np.int32)
    cdef int[:,:] PPX = np.empty((4,1), dtype=np.int32)
    cdef int[:,:] Cr = np.empty((4,4), dtype=np.int32)
    cdef int[:,:] R = np.empty((4,1), dtype=np.int32)
    cdef int[:,:] Cc = np.empty((4,1), dtype=np.int32)
    cdef int[:,:] pix = np.empty((1,1), dtype=np.int32)

    h_r = cCR(ih, h)
    w_r = cCR(iw, w)
   
    PPY[3,0] = vSBIT
    PPX[3,0] = vSBIT
    for j in range(h):
        y = j * h_r
        _H = y >> SBIT
        H = _H << SBIT
        PPY[2,0] = y - H
        PPY[1,0] =  cSR(PPY[2,0]*PPY[2,0])
        PPY[0,0] = cSR(PPY[1,0] * PPY[2,0])
        for k in range(w):
            x = k * w_r
            _W = x >> SBIT
            W = _W << SBIT
            PPX[2,0] = x - W
            PPX[1,0] = sSR(PPX[2,0] * PPX[2,0])
            PPX[0,0]  = sSR(PPX[1,0] * PPX[2,0])
            d0w = clip(_W-1, iw_, 0)
            d1w = clip(_W  , iw_, 0)
            d2w = clip(_W+1, iw_, 0)
            d3w = clip(_W+2, iw_, 0) 
            for i in range(ic):  
                for q in range(4):
                    d0h = clip(_H+q-1, ih_, 0)
                    F[q,0] = im[d0h, d0w, i]      
                    F[q,1] = im[d0h, d1w, i]       
                    F[q,2] = im[d0h, d2w, i]     
                    F[q,3] = im[d0h, d3w, i] 
                
                #Cr = F@XINV
                if (k == 100):
                    print(0,Cr[0,0])
                    cdot(F,XINV,Cr,4,4,4,4,2)
                    print(0,Cr[0,0])
                    #print('px:',px,'\n',PPX,'\n')
                    #print("CR PPX",Cr.shape, PPX.shape, type(Cr), type(PPX), Cr.dtype, PPX.dtype)
                    #R  = Cr@PPX 
                    print(1,R[0,0])
                    cdot(Cr,PPX,R,4,4,4,1,2)
                    print(1,R[0,0])
                    #Cc = (YINV@R + hSBIT) / vSBIT
                    cdot(cYINV,R,Cc,4,4,4,1,2)
                    #pix = Cc@PPY
                    print(2,pix[0,0])
                    cdot(PPY,Cc,pix,1,4,4,1,1)
                    print(2,pix[0,0])
                    img[j,k,i]= clip(pix[0,0],255,0)
                else:
                    cdot(F,XINV,Cr,4,4,4,4,2)
                    #print('px:',px,'\n',PPX,'\n')
                    #print("CR PPX",Cr.shape, PPX.shape, type(Cr), type(PPX), Cr.dtype, PPX.dtype)
                    #R  = Cr@PPX 
                    cdot(Cr,PPX,R,4,4,4,1,2)
                    #Cc = (YINV@R + hSBIT) / vSBIT
                    cdot(cYINV,R,Cc,4,4,4,1,2)
                    #pix = Cc@PPY
                    cdot(PPY,Cc,pix,1,4,4,1,1)
                    img[j,k,i]= clip(pix[0,0],255,0)
                #print((j,k,i),(img[j,k,i],pix))

    return img