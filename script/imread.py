from PIL import Image
import sys

def imread(file_name):
	img = Image.open(file_name)
	img.show()

if __name__ == '__main__':
	imread(sys.argv[1])