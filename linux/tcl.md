## tcsh

unlike bash, tcsh/cshell does not have function.

* [args](#args)
* [alias](#alias)
* [eval](#eval)
* [hybrid](#hybrid)

### args

```tcsh

# number of args
set c=$#argv

# get number of args
set a=$1
set b=$2-

# number var comparison
if ( $c > 0 ) then
  echo hello world! c is $c
else if ( $c == 0 ) then
  echo oh ! c is $c
else
  echo c is negative!
endif

# string var comparison
if ( ${a} == 'proj' ) then
  echo a is proj!
  
# substring comparison
else if ( ${a} =~ *"fe"* ) then
  echo a has fe substring!
endif

# file check
if ( -e ${a}/${b} ) then
  echo file exists!
endif
```

### eval

eval is utils able to execute string command as shell cmd.

```tcsh
set a='echo hi! I am choi && echo "3 + 4" | bc'
eval $a
```

### alias

tcsh alias able to capture argument, which is very useful for proj navigation and script handling

```tcsh

# alias to cshell
alias backws 'cd `backwork.csh`'

# capture alias args
( \!* ) - all args
$a[1] - first argument
$a[2-] - second to last argument

# example
alias goto-dft 'set a=( \!* ); cd `_goto.csh dft $a`; unset a'
alias run-pm 'set a=( \!* ); set b=`_goto.csh tool voltus_power $a[1]`; eval "$b $a[2-]"; unset a; unset b'
alias run-pm-g 'set a=( \!* ); set b=`_goto.csh tool voltus_power $a[1]`; eval "$b -dbg -debugger 'gdb --args %exe% %args' $a[2-]" ; unset a; unset b;'

alias addPath 'set path=(\!^ $path)'

# timeit 
alias timeprog 'set _a=( \!* ); set _b=`date -u +%s.%N` && echo $_a && eval "$_a" && set _c=`date -u +%s.%N` && echo elapsed time : `echo ${_c} - ${_b} | bc` seconds ; unset _a; unset _b; unset _c'

# hybrid with alias, 
alias dftutil 'set a=( \!* ); python3 ~/scripts/dftutils.py $a[1] -p `backwork.csh` $a[2-]; unset a'
```

## hybrid

```tcsh
## alias
alias rundft-rerun 'set a=( \!* ); set dfts=`_goto.csh listdft $a[1]`; make run_dft FLAVOR=opt DFT_COMMAND="$dfts $a[2-] -parallel 300 -newsub -cleanup=pass"; unset a; unset dfts'

## goto.csh
    set summary=${anls_path}/output/dftout/lnx86_64_opt/summary_${key}.end
    set dfts=`python -c 'import sys; print (" ".join(open(sys.argv[1],"r").readlines()[6:-1])).replace("\n","")' $summary`
    echo $dfts
```
