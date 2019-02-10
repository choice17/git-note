from ctypes import *
import math
import random
import cv2
import numpy as np
import os
from datetime import datetime

def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]

class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


#lib = CDLL("/home/pjreddie/documents/darknet/libdarknet.so", RTLD_GLOBAL)
class DARKNETLIB(object):
    def __init__(self):
        s = self
        lib = CDLL("libdarknet.so", RTLD_GLOBAL)
        lib.network_width.argtypes = [c_void_p]
        lib.network_width.restype = c_int
        lib.network_height.argtypes = [c_void_p]
        lib.network_height.restype = c_int

        predict = lib.network_predict
        predict.argtypes = [c_void_p, POINTER(c_float)]
        predict.restype = POINTER(c_float)
        set_gpu = lib.cuda_set_device
        set_gpu.argtypes = [c_int]

        make_image = lib.make_image
        make_image.argtypes = [c_int, c_int, c_int]
        make_image.restype = IMAGE

        get_network_boxes = lib.get_network_boxes
        get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
        get_network_boxes.restype = POINTER(DETECTION)

        make_network_boxes = lib.make_network_boxes
        make_network_boxes.argtypes = [c_void_p]
        make_network_boxes.restype = POINTER(DETECTION)

        free_detections = lib.free_detections
        free_detections.argtypes = [POINTER(DETECTION), c_int]

        free_ptrs = lib.free_ptrs
        free_ptrs.argtypes = [POINTER(c_void_p), c_int]

        network_predict = lib.network_predict
        network_predict.argtypes = [c_void_p, POINTER(c_float)]

        reset_rnn = lib.reset_rnn
        reset_rnn.argtypes = [c_void_p]

        load_net = lib.load_network
        load_net.argtypes = [c_char_p, c_char_p, c_int]
        load_net.restype = c_void_p

        do_nms_obj = lib.do_nms_obj
        do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

        do_nms_sort = lib.do_nms_sort
        do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

        free_image = lib.free_image
        free_image.argtypes = [IMAGE]

        letterbox_image = lib.letterbox_image
        letterbox_image.argtypes = [IMAGE, c_int, c_int]
        letterbox_image.restype = IMAGE

        load_meta = lib.get_metadata
        load_meta.argtypes = [c_char_p]
        load_meta.restype = METADATA

        load_image = lib.load_image_color
        load_image.argtypes = [c_char_p, c_int, c_int]
        load_image.restype = IMAGE

        rgbgr_image = lib.rgbgr_image
        rgbgr_image.argtypes = [IMAGE]

        predict_image = lib.network_predict_image
        predict_image.argtypes = [c_void_p, IMAGE]
        predict_image.restype = POINTER(c_float)

        s.predict_image         = predict_image
        s.rgbgr_image           = rgbgr_image
        s.load_image            = load_image
        s.load_meta             = load_meta
        s.letterbox_image       = letterbox_image
        s.free_image            = free_image
        s.do_nms_sort           = do_nms_sort
        s.load_net              = load_net
        s.reset_rnn             = reset_rnn
        s.network_predict       = network_predict
        s.free_ptrs             = free_ptrs
        s.free_detections       = free_detections
        s.make_network_boxes    = make_network_boxes
        s.get_network_boxes     = get_network_boxes
        s.make_image            = make_image
        s.set_gpu               = set_gpu
        s.predict               = predict
        s.lib                   = lib
        s.do_nms_obj            = do_nms_obj
        s.do_nms_sort           = do_nms_sort

    def classify(self, net, meta, im):
        out = self.predict_image(net, im)
        res = []
        for i in range(meta.classes):
            res.append((meta.names[i], out[i]))
        res = sorted(res, key=lambda x: -x[1])
        return res

    def detect_np(self, net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
        #im_ = load_image(image.encode(), 0, 0)
        im = IMAGE()
        """ darknet format
        image: CHW
        cv2:   HWC
        """
        img = cv2.imread(image)[:,:,::-1].transpose(2,0,1)
        img = img / 255
        c, h, w = img.shape
        im.h, im.w, im.c = c_int(h), c_int(w), c_int(c)

        data = img.flatten()
        C_P = c_float * (im.h * im.w * im.c)
        data = pointer((C_P)(*data))
        im.data = cast(data, POINTER(c_float))
        #im.data = cast(data, c_float_p)

        num = c_int(0)
        pnum = pointer(num)

        self.predict_image(net, im)
        dets = self.get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)

        num = pnum[0]
        if (nms): self.do_nms_obj(dets, num, meta.classes, nms)

        res = []
        for j in range(num):
            for i in range(meta.classes):
                if dets[j].prob[i] > 0:
                    b = dets[j].bbox
                    res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
        res = sorted(res, key=lambda x: -x[1])
        #free_image(im)
        #free_detections(dets, num)
        return res


    def detect(self, net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
        im = self.load_image(image, 0, 0)
        num = c_int(0)
        pnum = pointer(num)
        self.predict_image(net, im)
        dets = self.get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
        num = pnum[0]
        if (nms): self.do_nms_obj(dets, num, meta.classes, nms)

        res = []
        for j in range(num):
            for i in range(meta.classes):
                if dets[j].prob[i] > 0:
                    b = dets[j].bbox
                    res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
        res = sorted(res, key=lambda x: -x[1])
        self.free_image(im)
        self.free_detections(dets, num)
        return res

def load_config():
    lib = DARKNETLIB()
    cfg_file = b"cfg/yolov3-tiny.cfg"
    weights_file = b"weights/yolov3-tiny.weights"
    label_file = b"cfg/coco.data"
    tar_file = "data/dog.jpg"
    for f in [cfg_file, weights_file, label_file, tar_file]:
        assert os.path.exists(f), "%s does not exists" % f
    net = lib.load_net(cfg_file, weights_file, 0)
    meta = lib.load_meta(label_file)
    return lib, net, meta

def detect_IMG(net, meta, image, lib, thresh=.5, hier_thresh=.5, nms=.45 ):
    """ darknet format
    image: CHW
    cv2:   HWC
    """
    im = IMAGE()
    img = image[:,:,::-1].transpose(2,0,1).astype(float) / 255.
    c, h, w = img.shape
    im.h, im.w, im.c = c_int(h), c_int(w), c_int(c)
    data = img.flatten()
    C_P = c_float * (im.h * im.w * im.c)
    data = pointer((C_P)(*data))
    im.data = cast(data, POINTER(c_float))
    #im.data = cast(data, c_float_p)

    num = c_int(0)
    pnum = pointer(num)

    lib.predict_image(net, im)
    dets = lib.get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)

    num = pnum[0]
    if (nms): lib.do_nms_obj(dets, num, meta.classes, nms)

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    return res

def drawbox(results, im):
    res = results
    for r in res:
        rname, _, box = r
        x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        sx, sy, ex, ey = x - (w>>1), y - (h>>1), x + (w>>1), y + (h>>1)
        cv2.rectangle(im, (sx, sy), (ex, ey), (0, 255,0), 3)
        cv2.putText(im, rname.decode(), (sx, ey), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255,0), 2, cv2.LINE_AA)

def main():
    lib, net, meta = load_config()
    cap = cv2.VideoCapture(0)
    if not cap:
        print("not valid camera")
        return
    cv2.namedWindow("T", cv2.WINDOW_NORMAL)

    while (True):
        f, im = cap.read()
        if not f:
            print("no valid frame")
            return
        r = detect_IMG(net, meta, im, lib)
        if r != []:
            print(r, datetime.now())
        drawbox(r, im)
        cv2.imshow("T", im)
        waitKey = cv2.waitKey(10)
        if waitKey == ord('q'):
            return
    
if __name__ == "__main__":
    #net = load_net("cfg/densenet201.cfg", "/home/pjreddie/trained/densenet201.weights", 0)
    #im = load_image("data/wolf.jpg", 0, 0)
    #meta = load_meta("cfg/imagenet1k.data")
    #r = classify(net, meta, im)
    #print r[:10]
    main()
    """
    import os
    lib = DARKNETLIB()
    cfg_file = b"cfg/yolov3-tiny.cfg"
    weights_file = b"weights/yolov3-tiny.weights"
    label_file = b"cfg/coco.data"
    tar_file = "data/dog.jpg"
    for f in [cfg_file, weights_file, label_file, tar_file]:
        assert os.path.exists(f), "%s does not exists" % f
    net = lib.load_net(cfg_file, weights_file, 0)
    meta = lib.load_meta(label_file)
    r = lib.detect_np(net, meta, tar_file)
    #r = detect_np(net, meta, "data/dog.jpg")
    print(r)
    """
    

