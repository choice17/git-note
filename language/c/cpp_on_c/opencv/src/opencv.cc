#include "opencv.hh"
#include <iostream>

using namespace std;

int CASCADE::add(int w, int h)
{
    cout << __func__ << " " << __LINE__ << \
    "return: " << w + h << endl;
    return w + h; 
}

int MAT::sum(int w, int h)
{
    cout << __func__ << " " << __LINE__ << \
    "return: " << w + h << endl;
    return w + h; 
}
