#ifndef _OPENCV_H_
#define _OPENCV_H_

#ifdef __cplusplus
extern  "C" {
#endif

/* cxx class wrapper */
typedef struct CASCADE CASCADE;
typedef struct MAT MAT;

/* cxx member function wrapper */
CASCADE *new_cas(void);
MAT *new_mat(void);
int cas_add(CASCADE *cas, int w, int h);
int mat_sum(MAT *mat, int w, int h);

#ifdef __cplusplus
}
#endif

#endif /* _OPENCV_H_ */