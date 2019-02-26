import os
import imp
from utils import import_abs
FILE = "print_app"

def print_main():
	print("Hello world from print_main!")


def importModule(content, filename):
	"""
	https://www.oreilly.com/library/view/python-cookbook/0596001673/ch15s03.html
	"""
	module = imp.new_module(filename)
	exec(content, module.__dict__)
	return module

def main():
	print_main()
	if os.path.exists(FILE + ".py"):
		P = import_abs(FILE)
		P.print_app()

if __name__ == "__main__":
	main()
