import demo_pb2

import sys

pb_file = "addr_book.pb"

def writePb(pb_file):
	# init
	address_book = demo_pb2.AddressBook()

	# add
	person = address_book.people.add()

	# setup
	person.id = 123
	person.name = "T C YU"
	person.email = "tcyu@umich.edu"

	# add attr
	phone_number = person.phones.add()
	phone_number.number = "023-2312312"
	phone_number.type = demo_pb2.Person.MOBILE

	# add attr
	phone_number = person.phones.add()
	phone_number.number = "01-12323344"
	phone_number.type = demo_pb2.Person.WORK

	# write
	with open(pb_file, "wb") as f:
	  f.write(address_book.SerializeToString())

def readPb(pb_file):
	address_book = demo_pb2.AddressBook()

	with open(pb_file, "rb") as f:
	  address_book.ParseFromString(f.read())

	# display
	for person in address_book.people:
	  print("Person ID:", person.id)
	  print("  Name:", person.name)
	  if person.HasField('email'):
	    print("  E-mail address:", person.email)

	  for phone_number in person.phones:
	    if phone_number.type == demo_pb2.Person.MOBILE:
	      print("  Mobile phone #:", phone_number.number)
	    elif phone_number.type == demo_pb2.Person.HOME:
	      print("  Home phone #:", phone_number.number)
	    elif phone_number.type == demo_pb2.Person.WORK:
	      print("  Work phone #:", phone_number.number)

def main():
	writePb(pb_file)
	readPb(pb_file)

if __name__ == '__main__':
	main()

