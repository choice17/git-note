/* SIMD header file
** https://blog.csdn.net/nancygreen/article/details/8880810
** gcc -Q --help=target | grep enabled => detect avaiable SIMD set
** https://www.officedaytime.com/simd512e/simd.html operation set
** WORD - 16bit DWORD - 32bit QWORD - 64bit
** EIGEN matrix lib AVX
** gcc -march=native -O2 -mavx -mno-avx -mno-sse4 ... etc
*/

#include <stdio.h>
#include <immintrin.h>  // portable to all x86 compilers
#include <stdint.h>



int32_t sum_array(const int32_t a[], const int n)
{
    __m128i vsum = _mm_set1_epi32(0);       // initialise vector of four partial 32 bit sums
    int32_t sum;
    int i;

    for (i = 0; i < n; i += 4)
    {
        __m128i v = _mm_load_si128(&a[i]);  // load vector of 4 x 32 bit values
        vsum = _mm_add_epi32(vsum, v);      // accumulate to 32 bit partial sum vector
    }
    // horizontal add of four 32 bit partial sums and return result
    vsum = _mm_add_epi32(vsum, _mm_srli_si128(vsum, 8));
    vsum = _mm_add_epi32(vsum, _mm_srli_si128(vsum, 4));
    sum = _mm_cvtsi128_si32(vsum);
    return sum;
}

int main()
{
    __m128 vector1 = _mm_set_ps(4.0, 3.0, 2.0, 1.0); // high element first, opposite of C array order.  Use _mm_setr_ps if you want "little endian" element order in the source.
    __m128 vector2 = _mm_set_ps(7.0, 8.0, 9.0, 0.0);

    __m128 sum = _mm_add_ps(vector1, vector2); // result = vector1 + vector 2

    vector1 = _mm_shuffle_ps(vector1, vector1, _MM_SHUFFLE(0,1,2,3));
    // vector1 is now (1, 2, 3, 4) (above shuffle reversed it)
    printf("%f %f %f %f \n", vector1[0], vector1[1], vector1[2], vector1[3]);


    int32_t a[16] = {0,23,41,42,-23,23,35,67,39,256,64,3456,-3456,2,4,53};
    int res = sum_array(a, 16);

    return 0;
}