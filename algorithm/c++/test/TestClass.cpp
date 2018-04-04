#include "TestClass.h"
#include <iostream>

TestClass::TestClass()
{
	std::cout << "Created TestClass\n";
}

TestClass::~TestClass()
{
}

void TestClass::gimme()
{
	std::cout << "Called gimme\n";
}