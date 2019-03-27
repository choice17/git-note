import matplotlib.pylab as plt
import matplotlib.image as Image
#from PIL import Image
import numpy as np


def histeq(img, show=0):
	flat = img.flatten()
	hist = getImgHist(flat)
	if show:
		#plt.hist(flat, bins=50)
		plt.plot(hist)#, bins=255)
		plt.show()
	cdf = getImgCdf(hist)
	if show:
		plt.plot(cdf)
		plt.show()
	cdf = normalCdf(cdf, flat.shape[0])
	if show:
		plt.plot(cdf)
		plt.show()
	eq = cdfEq(cdf, flat, img.shape)
	return eq

def normalCdf(cdf, shape):
	cdf =  np.round(cdf / shape * 255)
	return cdf.astype(np.uint8)

def cdfEq(cdf, flat, shape):
	eq = cdf[flat]
	eq = eq.reshape(shape)
	return eq

def getImgHist(img):
	hist = np.zeros((255),dtype=np.int32)
	for i in img:
		hist[i] += 1
	return hist

def getImgCdf(hist):
	cdf = hist.copy()
	for i in range(1, cdf.shape[0]):
		cdf[i] += cdf[i-1]
	return cdf


def main():
	file = "../../../files/low_constrast.jpg"
	""" PIL
	img = Image.open(file)
	img = np.array(img)
	img = np.dstack((img,img,img))
	print("image shape,", img.shape,img.flatten().shape)
	nimg = histeq(img, 1)
	simg = np.hstack((img, nimg))
	print(img.shape, nimg.shape, simg.shape)
	aimg = Image.fromarray(simg,'RGB')
	aimg.show()
	"""
	# matplotlib image
	img = Image.imread(file)
	#img = np.array(img)
	img = np.dstack((img,img,img))
	print("image shape,", img.shape,img.flatten().shape)
	nimg = histeq(img, 1)
	simg = np.hstack((img, nimg))
	print(img.shape, nimg.shape, simg.shape)
	plt.imshow(simg)
	plt.show()

if __name__ == '__main__':
	main()
