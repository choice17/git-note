import os
import imp

def import_abs(filename):
	filename += ".py"
	module = imp.new_module(filename)
	exec(open(filename,"r").read(), module.__dict__)
	return module