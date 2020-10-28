# Note: C++ 

## Content  

* **[make file](#make_file)**  
* **[file ptr](#file_ptr)**  
* **[unix socket](#unix_socket)**  
* **[win socket](#window_socket)**  
* **[simd](#simd)**  
* **[cpp on c](#cpp_on_c)**  
* **[shared library linker](https://amir.rachum.com/blog/2016/09/17/shared-libraries/)**

## make_file

## introduction of make file

* [make file intro](./makefile.md)
* [[stackoverflow]](https://stackoverflow.com/questions/2481269/how-to-make-a-simple-c-makefile?answertab=votes#tab-top)
* [reference1](http://nuclear.mutantstargoat.com/articles/make/)  
* [reference2](https://www.gnu.org/software/make/manual/make.html#Recursion)  
* [example](#make_file_example)  
* [make flow](#make_flow)  


## make_file_example
- [cppexample](./cpp/Makefile)  
```
cpp/
   |-inc/
   |    |-foo.h
   |    |-bar.h
   |-src/
   |    |-foo.c
   |    |-bar.c
   |    |-main.cc
   |-Makefile
```  

## make_flow  

This example  
* demo to link make file.  
* simple usage of C [make flow](./c/makeflow/readme.md)  


## Note: C  

## file_ptr  

- [write and read binary from struct](./c/fwrite_read.c)  
- [extern variable into global access](./c/fwrite_read.c)  

## unix_socket  

Unix socket for interprocess communication  

* [server](./c/unix_socket/server.c)  
* [client](./c/unix_socket/client.c)  
* [make](./c/unix_socket/Makefile)  

## window_socket  

Window socket for inter device communication with python Popen interface

* [server](./c/window_socket/win_server.c)  
* [client](./c/window_socket/win_client.c)  
* [make](./c/window_socket/Makefile)  
* [python](./c/window_socket/pipe_test.py)  

## simd  

Single instruction multiple data  
Exists in most modern CPU  
MMX -> SSE -> SSE4 -> AVX -> AVX2 -> SSE5 -> 3DNow!
We can also enable SIMD neon by using compiler option!!

* [hello world](./c/simd/simd.c)  

* https://community.arm.com/developer/tools-software/tools/b/tools-software-ides-blog/posts/arm-cortex-a-processors-and-gcc-command-lines

## cpp_on_c  

If we want to import cpp library into c project or 
import c lib into cpp project.
We have to add a thin wrapper layer code as a interface before using the library.

The example demos c project using cpp opencv library.

* [openv cpp on c](./c/cpp_on_c) 

## share library 

If we want to add dynamic link to a binary,

1. export LD_LIBRARY_PATH=<path>:$LD_LIBRARY_PATH
2. Add rpath in build flag -Wl,-rpath=/home/username/foo

## perf  

Allow module to store frame point in compiler flag  

`-fno-omit-frame-pointer`




