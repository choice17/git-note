import os
import imp

FILE = "print_app.py"

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
	if os.path.exists(FILE):
		fobj = open(FILE,'r').read()
		P = importModule(fobj, FILE)
		"""
		import <module> as <P>
		"""
		code = """
a = P.print_app()
b = P.print_bar()
print('print a:(%s) and b:(%s) from main' %(a, b))
"""
		exec(code)
		"""
		import <module> directly from .py
		""" 
		exec(fobj)
		code = """
a = print_app()
b = print_bar()
print('print a:(%s) and b:(%s) from main' %(a, b))
"""
		exec(code)
if __name__ == "__main__":
	main()
