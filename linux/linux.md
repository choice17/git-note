## LINUX

* [ping](#ping)  
* [find](#find)  
* [sed](#sed)  
* [grep](#grep)  
* [netstat](#netstat)  
* [ifconfig](#ifconfig)  
* [vi](#vi)  
* [killall](#killall)  
* [top](#top)  
* [watch](#watch)  
* [cat](#cat)  
* [touch](#touch)  
* [tr](#tr)  

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
