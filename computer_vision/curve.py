import cv2
import numpy as np
import matplotlib.pylab as plt

ADD = 50
#fit_x = np.array([0, 5, 40, 95, 150, 200, 240, 255])
#fit_y = np.array([0, 6, 43, 150 , 152, 200, 240, 255])
fit_x = np.array([0, 5, 40, 95, 150, 200, 240, 255])
fit_y = np.array([0, 6, 43, 130 , 152, 200, 240, 250])
curve = np.polyfit(fit_x, fit_y, 7)
print(curve)
class Curve(object):
	def __init__(self,curve=None):
		if curve is not None:
			self._coef = curve
			self._len = len(curve)

	def set(self, curve):
		self._coef = curve
		self._len = len(curve)

	def get(self, img):
		t_img = img.astype(np.int32)
		o_img = np.zeros(img.shape)
		for i in range(self._len):
			o_img += (t_img ** i) * self._coef[self._len-i-1]
			print("(%.4f) * x(%.4f) ^ (%d) "%( self._coef[self._len-i-1], t_img[17,17], i))
		return o_img.astype(np.uint8)  
	def getP(self, img):
		p = np.poly1d(self._coef)
		o_img = p(img.astype(np.int32))
		#print(np.max(o_img[:]), np.min(o_img[:]))
		return o_img.astype(np.uint8)

C = Curve(curve)
p = np.poly1d(curve)
xp = np.linspace(0, 255, 100)
y = np.linspace(0, 255, 100)
_ = plt.plot(xp, y, '.', xp, p(xp), '-')
plt.xlim(0,255)
plt.ylim(0,255)
plt.show()

import glob
imgs = ['../files/mono.jpg']
i =0 
for img_ in imgs:
	print("processing %s"%img_)
	im = cv2.imread(img_)
	#im = im.astype(np.int32)
	#im[:,:,2] = np.where(im[:,:,2] + ADD  > 255, 255,  im[:,:,2] + ADD)
	#im = im.astype(np.uint8)
	#im[:,:,2] = C.get(im[:,:,2])
	im[:,:,2] = C.getP(im[:,:,2])
	#im = C.getP(im)
	cv2.imwrite("{0}.jpg".format(i), im)
	i += 1