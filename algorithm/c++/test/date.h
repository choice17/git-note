#ifndef DATE_H
#define DATE_H

class Date
{
	public:
	
	//constructor with default values if not provided
	Date(int = 1, int = 2000); 
	
	//set functions
	void setMonth(int); //set month
	void setYear(int); //set year 
	
	//get functions
	int getMonth(); //get month
	int getYear(); //get year
	
	//member functions
	void displayDate();//display date in mm/dd/yyyy format
	
	private:
	
	int month;
	int year; 
};

#endif 