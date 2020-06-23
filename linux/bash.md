## bash command

* [reference](https://www.shellscript.sh/)
* [variable](#variable)
* [args](#args)
* [while](#while_loop)  
* [if](#for_loop_string)  
* [for](#for_loop_string)  
* [str compare](#string_compare)  
* [test/pattern command](test_pattern)  
* [case](#case)  

## variable  

Bash does not need type declaration, they are all stored as string
```
file="file.txt"
var=1
var=2.4
```

## args  

Bash takes args 
```bash
file=$1
var=$2
```
## while_loop  

```bash
// while [[ cond ]] ; do // command ; done
file=$1
size=$2
end=10
start=0
while [[ $i -lt $end ]]
do
    // do your command here
    echo here is the value "$i"
    i=$(( i+1 ))
done
```

## for_loop_string  

// if [ cond ] then // command ; fi
// for [ cond ] ; do // command ; done

```bash
file=$1
mode=$2
name="fox is running"
if [ "$mode" == "walk" ]
then
    name="fox is walking"
fi

for n in $name
do
    grep $n -rn $file
done
```

## string_compare  

```bash
VAR1="Linuxize"
VAR2="Linuxize"

if [ "$VAR1" = "$VAR2" ]; then
    echo "Strings are equal."
else
    echo "Strings are not equal."
fi
```

## test_pattern

```
Use the = operator with the test [ command.
Use the == operator with the [[ command for pattern matching.
"[" is an alias symbol link to test program in linux, i.e. if ["$a" = 3] => test$a = 3] is not a valid symtax.
similar to "[["
```

```bash
#!/bin/bash

VAR1="Linuxize"
VAR2="Linuxize"
# case 0 test
if [ "$VAR1" = "$VAR2" ]; then
    echo "Strings are equal."
else
    echo "Strings are not equal."
fi
# case 1 pattern matching
if [[ "$VAR1" == "$VAR2" ]]; then
    echo "Strings are equal."
else
    echo "Strings are not equal."
fi
```

## case 

```bash

          case  $variable-name  in
                pattern1|pattern2|pattern3)       
     		    command1
                    ...
                    ....
                    commandN
                    ;;
                pattern4|pattern5|pattern6)
     		    command1
                    ...
                    ....
                    commandN
                    ;;            
                pattern7|pattern8|patternN)       
     		    command1
                    ...
                    ....
                    commandN
                    ;;
                *)              
          esac
```

