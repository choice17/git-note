### gdb  

gdb is a linux debug tool

source code

https://www.gnu.org/software/gdb/download/

### content

* [method](#method)
* [gdb console](#gdb-console)
* [disable optimization](#disable-optimization)
* [avoid multithreading run](#avoid-multithreading-run)
* [gdbinit](#gdbinit)
* [add_debug_symbol](#add_debug_symbol)

### method

If user want to enable gdb, one must compile object file with -g flag with -O0 without optimization.

* by start up

```bash
>$ gdb --args binary.elf args1 args2 ...
>(gdb)$ - console
```

* attach program within gdb console

```bash
>(gdb)$ attach <pid>
```

* by attach program

```bash
>$ binary.elf &
>$ gdb -p <binary.elf pid>
>(gdb)$ - console
```

* detach from the debug program

```bash
>(gdb)$ - console
>(gdb)$ detach
```

### gdb console

* basic 

```
b <file>:<line no> ## break on the line number
b <function name> ## break on the function entry
i <break point> ## info of break point number
p <variable> ## print variable value
r ## restart program
c ## continue to next break point
n ## step into next line
l ## list current lines
info threads ## show threads information
t <thread no> ## jump to thread id
bt <stack number> ## show stack trace
j <stack number> ## jump to specific stack
p ((class/struct ptr *)<stack-address>)->(member variable) ## print specific stack member/member function by using stack address
shell ## jump to shell console ($ fg to return to gdb)
```

* disassemble the instruction set

```
set  disassemble-next-line on
show disassemble-next-line
```

## disable optimization

* for single function  

```cpp
/* function.cpp */
int __attribute__((optimize("O0"))) foo(int b)
{
  int a = b * b;
  return a;
}
```

* for a specific code segment  

```cpp
#pragma GCC optimize("O0")
...
#pragma GCC reset_options
```

## avoid multithreading run

* lock thread step

set scheduler-locking step  
set scheduler-locking on  

* fork
set follow-fork-mode  
parent  
child  

## gdbinit

gdb init is a automation tool. It allows gdb to run a program and print gdb command result to log file.
User can set conditional break point and print stack, back trace to log file without manual monitoring.

```bash
# to execute
$ g++ -o test test.cc -g -O0
$ gdb ./test -x .gdbinit 
$ gdb [-p pid] -x .gdbinit
```

```bash
# .gdbinit 
set pagination off
set logging file gdb.txt
set logging on

br foo if a == 300
# ^^ when breaking at function fun_convert, execute `commands` till next `end`
commands
    bt 3
    print " from foo \n"
    continue
end

br test.cc:15 if c == 25
# ^^ when breaking at line 451 of file.c, execute from `commands` till next `end`
commands
    bt 3
    print " from bar \n"
    continue
end

run
01q
```

```cpp
/* test.cc */
#include <iostream>

 int foo(int a)
{
    static int cnt = 0;
    return a + (++cnt);
}

int bar(int c)
{
 static int b = -1000;
  return ++b + c * 2;
}

int main()
{
    int i = 1000;
    int sum = 0;
   while(i-->0)
   {
       sum+=foo(i*2);
       sum+=bar(i/2);
   }
   std::cout << " result is " << sum << "\n";
   return 0;

}
```

## add_debug_symbol

we can add symbol using below method inside gdb console
```bash
> add-symbol-file filename address

# address can be retrieved using below command
> readelf -WS path/to/file.elf | grep .text | awk '{ print "0x"$5 }'
```

below is the automated function to retrieve symbol for gdb after adding the function to ~/.gdbinit
```bash
define add-symbol-file-auto
  # Parse .text address to temp file
  shell echo set \$text_address=$(readelf -WS $arg0 | grep .text | awk '{ print "0x"$5 }') >/tmp/temp_gdb_text_address.txt

  # Source .text address
  source /tmp/temp_gdb_text_address.txt

  #  Clean tempfile
  shell rm -f /tmp/temp_gdb_text_address.txt

  # Load symbol table
  add-symbol-file $arg0 $text_address
end
```
