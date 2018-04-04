#include <iostream>
#include <string>
#include "TestClass.h"
using namespace std;

int main()
{
	TestClass s;
	s.gimme();
	string yourName;

	cout << "Enter your name: ";
	cin  >> yourName;
	cout << "Hello " + yourName << endl;

	return 0;
}