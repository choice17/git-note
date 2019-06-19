# Note: C++ 

## Content  

* **[make file](#make_file)**  
* **[file ptr](#file_ptr)**  
* **[unix socket](#unix_socket)**  
* **[simd](#simd)**  

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

## simd  

Single instruction multiple data  
Exists in most modern CPU  
MMX -> SSE -> SSE4 -> AVX -> AVX2 -> SSE5 -> 3DNow!

* [hello world](./c/simd/simd.c)  

