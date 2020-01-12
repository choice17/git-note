#ifndef OPENCV_HH_
#define OPENCV_HH_

class CASCADE {
public:
    int w;
    int h;
    CASCADE(){};
    ~CASCADE(){};
    int add(int w, int h);
};

class MAT {
public:
    int w;
    int h;
    int c;
    void *data;
    MAT(){};
    ~MAT(){};
    int sum(int w, int h);
};

#endif