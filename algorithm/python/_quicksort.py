import numpy as np
import sys
#import __funture__
sys.setrecursionlimit(1000)

def _quicksort(array_in):

	if len(array_in) <2:
		return array_in
	pivot = array_in[0]
	smaller = [i for i in array_in[1:] if i <= pivot]
	bigger = [i for i in array_in[1:] if i >= pivot]
	
	return [quicksort(smaller) + [pivot] + quicksort(bigger),quicksort.counter]

