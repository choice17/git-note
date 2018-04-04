function sort_array = _quicksort(array_in)
	[m,n] = size(array_in);
	assert(m==1 || n==1,'only support 1D array');
	if n==1
		array_in = array_in';
	end
	lenArray = length(array_in);
	
	if lenArray<3
		return array_in;
	end
	
	pivot = 1;
	
	less = array_in(array_in<array_in(pivot));
	more = array_in(array_in>array_in(pivot));
	middle = array_in(array_in==array_in(pivot));
	
	sort_array = [_quicksort(less) middle _quicksort(more)];
end
	