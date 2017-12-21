import numpy as np

def _bubblesort(array_in):
	if len(array_in) < 2:
		return array_in
	arrayLen = len(array_in)
	for i in range(arrayLen-1):
		for j in np.arange(i,arrayLen-1):
			if  array_in[j]>=array_in[j+1]:
				temp_ = array_in[j+1]
				array_in[j+1] = array_in[j]
				array_in[j] = temp_
	return array_in
