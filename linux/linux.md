## LINUX

* [ping](#ping)  
* [find](#find)  
* [sed](#sed)  
* [grep](#grep)  
* [netstat](#netstat)  
* [ifconfig](#ifconfig)  
* [rename](#rename)  
* [vi](#vi)  
* [killall](#killall)  
* [top](#top)  
* [watch](#watch)  
* [cat](#cat)  
* [touch](#touch)  
* [tr](#tr)  
* [clang](#clang)  

## ping  

Ping can check network connection  

```
$ ping <ip>
```

## find  

find can search for files using wildcard  

```
$ find . -name "*.h"  
```  

find and exec clang-format
```
$ find . -name "*.[ch]" -exec clang-format-3.9 -i {} \;
```

## sed  

```
$ sed -i "s/<pattern_to_find>/<patter_to_replace>/g" <wildcard>
```

## rename  

usage of rename is similar to sed  

```
$ rename -f "s/<orig_pattern>/<to_pattern>/g" <file_pattern>
e.g. /* tmp.log tmp_a.log => tak.log tak_a.log */
$ rename -f "s/tmp/tak/g" *.c
```

## grep  

Search for all local directory recursively with line number 

```
$ grep -E "<pattern>" -rn . -A 5
```

`A` display with next 5 lines  

## killall  

killall can send signal to linux program by program name  


`-2`  SIGINT interrupt signal.  
`-9`  SIGKILL program cannot ignore the kill signal.  

```
killall -2 <program>  
```

## ifconfig  

To show pc mac, tcpip addr

```
$ ifconfig
```

## top

with watch in 2 sec loop

```
$ watch -d2 top
```

## cat   

cat is like echo, but to echo all the content of a file  

## touch  

touch create a empty content file  

## clang  

```
$ clang-format-3.9 before.c > after.c
Edit
Format One File with In-place Option
Run clang-format on filename.c and directly overwrite filename.c with formatted output. (-i option stands for in-place)
```
```
$ clang-format-3.9 -i filename.c
Edit
Format All Files in a Directory
Run clang-format in your target directory on all .h and .c files.
```
```
$ find . -name "*.[ch]" -exec clang-format-3.9 -i {} \;
Or, you want to process .c and .h files separately.
```
```
$ find . -name "*.h" -exec clang-format-3.9 -i {} \;
$ find . -name "*.c" -exec clang-format-3.9 -i {} \;
Edit
Format All Files in a Directory with Sanity Check
In short, formatting is very reliable.
But if you really want to check program behavior is not changed after formatting, you can run the following steps.

Before formatting, build all object files, strip debug information from them, and rename to *.o.orig.
```

```
$ make all
$ find . -name "*.o" -exec arm-augentix-linux-gnueabi-strip --strip-debug {} \;
$ find . -name "*.o" -exec mv {} {}.orig \;
$ find . -name "*.o.orig" 
Run clang-format in your target directory on all .h and .c files.

$ find . -name "*.h" -exec clang-format-3.9 -i {} \;
$ find . -name "*.c" -exec clang-format-3.9 -i {} \;
After formatting, build all object files, strip debug information from them, and compare to *.o.orig.

$ make all
$ find . -name "*.o" -exec arm-augentix-linux-gnueabi-strip --strip-debug {} \;
$ find . -name "*.o" -exec diff {} {}.orig \;
If any object code differ from original one, you can further check the cause by disassemble them.
Take mpi_dev.o for example, the new object code differs from original one because it contains build date and time in the object code.

$ diff mpi_dev.o mpi_dev.o.orig
Binary files mpi_dev.o and mpi_dev.o.orig differ
$ arm-augentix-linux-gnueabi-objdump -D mpi_dev.o > mpi_osd.o.asm
$ arm-augentix-linux-gnueabi-objdump -D mpi_dev.o.orig > mpi_osd.o.orig.asm
$ meld mpi_osd.o.asm mpi_osd.o.orig.asm
```
