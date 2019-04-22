import numpy as np

def _bubblesort(array_in):
	if len(array_in) < 2:
		return array_in
	arrayLen = len(array_in)
	for i in range(arrayLen-1):
		for j in np.arange(arrayLen-1):
			if  array_in[j]>=array_in[j+1]:
				temp_ = array_in[j+1]
				array_in[j+1] = array_in[j]
				array_in[j] = temp_
	return array_in

def main():
	_min = -9999
	_max = 9999
	_len = 10
	li = np.random.randint(_min, _max, (_len))
	print(li)
	_bubblesort(li)
	print(li)


if __name__ == '__main__':
	main()