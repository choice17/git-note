from keras.applications import MobileNet as Model

if __name__ == '__main__':
	model = Model(weights="imagenet")