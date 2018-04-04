## typedef is to alias data type with another name

### alias to int 

```
typedef int km_per_hour ;
typedef int points ;

km_per_hour current_speed ;  //"km_per_hour" is synonymous with "int" here,
points high_score ;          //and thus, the compiler treats our new variables as integers.


void congratulate(points your_score) {
    if (your_score > high_score)
```

### alias to structure

```
struct MyStruct {
    int data1;
    char data2;
};
```

can be written as 

```
typedef struct MyStruct {
    int data1;
    char data2;
} newtype;
```

`newtype a;` instead of call `struct MyStruct a;`

### alias to pointer

```
typedef int *intptr;

intptr cliff, allen;        // both cliff and allen are int* type

intptr cliff2, *allen2; 	// it is int** type here
```

### alias to function pointers

without using typedef 
```
int do_math(float arg1, int arg2) {
    return arg2;
}

int call_a_func(int (*call_this)(float, int)) {
    int output = call_this(5.5, 7);
    return output;
}

int final_result = call_a_func(&do_math);
```

use typedef 
```
typedef int (*MathFunc)(float, int);

int do_math(float arg1, int arg2) {
    return arg2;
}

int call_a_func(MathFunc call_this) {
    int output = call_this(5.5, 7);
    return output;
}

int final_result = call_a_func(&do_math);
```

other example: 
```
void (*signal(int sig, void (*func)(int)))(int);
```
while use typedef make it more clear
```
typedef void (*sighandler_t)(int);
sighandler_t signal(int sig, sighandler_t func);
```

### alias with list/array
```
typedef char arrType[6];    // type name: arrType
                            // new type: char[6]

arrType arr={1,2,3,4,5,6};  // same as: char arr[6]={1,2,3,4,5,6}

arrType *pArr;              // same as: char (*pArr)[6];
```

