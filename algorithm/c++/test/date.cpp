#include <iostream>
#include "date.h"

	Date::Date(int m, int y) //constructor with parameters
	{
		setMonth(m);
		setYear(y);
	}
	//set functions
	void Date::setMonth(int m) //set month, if input not 1-12, will set to 1
	{
		if (m >= 1 && m <= 12)
			month = m;
		else
			month = 1;
	}
	void Date::setYear(int y) //set year 
	{
		year = y;
	}
	//get functions
	int Date::getMonth() //get month
	{
		return month;
	}
	int Date::getYear() //get year
	{
		return year;
	}
	//member functions
	void Date::displayDate() //display date in mm/yyyy format
	{
		std::cout << month << "/" << year;
	}