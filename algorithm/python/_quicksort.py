import numpy as np
import sys
import random
import time
#import __funture__
sys.setrecursionlimit(1000)


def _quicksort(array_in):

	if len(array_in) <2:
		return array_in

	smaller = []
	equal = []
	bigger = []
	pivot = random.choice(array_in)
	
	for i in array_in:
		if i < pivot:
			smaller.append(i)
		elif i == pivot:
			equal.append(i)
		else: 
			bigger.append(i)

	#smaller = [i for i in array_in if i < pivot]
	#bigger = [i for i in array_in if i > pivot]
	
	return _quicksort(smaller) + equal + _quicksort(bigger) 

if __name__ == "__main__":
	print("demo of using _quicksort...")
	print("list a = [1,23,4,5,63,98,23,12,5,3,6]")
	a = np.random.rand(10000)
	c = time.time()
	_quicksort(a)
	print("time used for _quicksort is {}".format(time.time()-c))


