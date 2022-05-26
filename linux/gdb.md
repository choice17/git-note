### gdb  

gdb is a linux debug tool

source code

https://www.gnu.org/software/gdb/download/

### method

If user want to enable gdb, one must compile object file with -g flag with -O0 without optimization.

* by attach program

```bash
$> binary.elf &
$> gdb -p binary.elf-pid
$> : gdb - console
```

* by start up

```bash
$> gdb --args binary.elf args1 args2 ...
$> : gdb - console
```

* detach the debug program

```bash
$> : gdb - console
$> : detach
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
```

* disassemble the instruction set

```
set  disassemble-next-line on
show disassemble-next-line
```

## disable optimization for function

```cpp
/* function.cpp */
int __attribute__((optimize("O0"))) foo(int b)
{
  int a = b * b;
  return a;
}
```
