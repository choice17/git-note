#include "arr_img.h"


double array_sum(double *arr, int w, int h)
{
    int i, j;
    double sum = 0;
    for (i = 0; i < h; ++i) {
        for (j = 0; j < w; ++j) {
            sum += arr[i * w + j];
        }
    }
    return sum;
}

double chi2(double m, double b, double *x, double *y, double *yerr, int N) {
    int n;
    double result = 0.0, diff;

    for (n = 0; n < N; n++) {
        diff = (y[n] - (m * x[n] + b)) / yerr[n];
        result += diff * diff;
    }

    return result;
}