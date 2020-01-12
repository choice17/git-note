#include "opencv.hh"
#include "_opencv.h"

#include <iostream>

using namespace std;

CASCADE *new_cas(void)
{
    return new CASCADE();
}

MAT *new_mat(void)
{
    return new MAT();
}

int cas_add(CASCADE *cas, int w, int h)
{
    cout << __func__ << " " << __LINE__ << endl;
    return cas->add(w, h);
}

int mat_sum(MAT *mat, int w, int h)
{
    cout << __func__ << " " << __LINE__ << endl;
    return mat->sum(w, h);

}
