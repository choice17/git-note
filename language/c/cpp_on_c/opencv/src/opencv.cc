#include "opencv.hh"
#include <iostream>

using namespace std;

CASCADE::add(int w, int h)
{
    cout << __func__ << " " << __LINE__ << \
    "return: " << w + h << endl;
    return w + h; 
}

MAT::sum(int w, int h)
{
    cout << __func__ << " " << __LINE__ << \
    "return: " << w + h << endl;
    return w + h; 
}
