import os

FILE = "print_app.py"

def print_main():
	print("Hello world from print_main!")

def main():
	print_main()
	if os.path.exists(FILE):
		import print_app as P
		P.print_app()


if __name__ == "__main__":
	main()
