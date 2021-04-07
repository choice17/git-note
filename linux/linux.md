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
* [mount](#mount)
* [sysctl](#sysctl)  
* [dos2unix](#dos2unix)  
* [tar](#tar)  
* [sh loop](#sh)
* [clean-console](#clean)  
* [objdump](#objdump)  
* [readelf](#readelf)  
* [nm](#nm)  
* [module](#module)  
* [strip](#strip)  
* [wc](#wc)  

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

find with regex with sed type
```
$ find . -regextype sed -regex "./[0-9]\{5\}.txt"

// find local file with absolute path
$ find . -regextype sed -regex ".*/train/[0-9]\{5\}\.txt" -exec readlink -f  {} \;

// search by absolute path directly for /path/{:012d}.jpg
$ find /<path> -type f -regextype sed -regex '\/.*[0-9]\{12\}.jpg'
```

See regex example https://regex101.com/r/bN0fU0/4,
same regex but added slash for exscape char.  

find with multiple cmd
```
$ find <dir> -name "*.mp4" -exec sh -c 'f=$(basename {}); python3 script.py -src <dir>/"$f" <dir>/"$f" pattern/"$f" -dst <dir>/"$f" -args xxx' \;
```

## sed  

Replace pattern
```
$ sed -i "s/<pattern_to_find>/<patter_to_replace>/g" <wildcard>
```

Append line
```
$ sed -i "<line no>a<string>" <file wildcard>
```

Replace line
```
$ sed -i "<line no>c<string>" <file wildcard>
```

Without inplace the file and output to console
```
$ sed "<line no>c<string>" <file wildcard> | head -20
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

Redefine new ethernet hw addr

```
ifconfig eth0 down
ifconfig eth0 hw ether AA:BB:CC:CC:00:11
ifconfig eth0 192.168.0.10 netmask 255.255.192.0
ifconfig eth0 up
```

## top

with watch in 2 sec loop

```
$ watch -d2 top
```

or 

```
$ top -d 2
```

PS. use key 0/1 to show cpu core loading

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

## mount 

```
## manual_mount_nfs

NFS_IP=192.168.10.147
NFS_NAME=ethnfs
NFS_DIR=/mnt/nfs/ethnfs

ping -c 1 -w 2 $NFS_IP
$ mount -o port=2049,nolock,proto=tcp -t nfs $NFS_IP:/$NFS_NAME $NFS_DIR
 or
$ mount -o port=2049,nolock,proto=tcp -t nfs 192.168.10.147:/ethnfs /mnt/nfs/ethnfs
```

## tr

tr is something like sed 

```
IFACE=eth0

ETHADDR=$(cat /sys/class/net/$IFACE/address)

# Default MAC address set by U-Boot
ETHADDR_DEFAULT=02:00:00:00:00:00

set_random_ethaddr() {
        ETHADDR=$(tr -dc A-F0-9 < /dev/urandom | head -c 6 | \
                  sed -r 's/(..)/\1:/g;s/:$//;s/^/12:34:56:/')
        echo "Randomize MAC address: $ETHADDR"
        /sbin/ifdown $IFACE
        ifconfig $IFACE hw ether $ETHADDR
        /sbin/ifup $IFACE
}


case "$1" in
        start)
                # set MAC address to 12:34:56:XX:XX:XX
                # if default MAC address is applied
                if [ $ETHADDR = $ETHADDR_DEFAULT ]; then
                        set_random_ethaddr
                fi
        ;;
        stop)
        ;;
        restart|reload)
                "$0" stop
                "$0" start
                ;;
        *)
                echo "Usage: $0 {start|stop|restart}"
                exit 1
        ;;
esac
```

## sysctl  

system ctrl module allows to broaden the bandwidth of network

starting network
```
/sbin/sysctl -w net.core.rmem_default=524288
/sbin/sysctl -w net.core.wmem_default=524288
/sbin/sysctl -w net.core.rmem_max=624288
/sbin/sysctl -w net.core.wmem_max=724288
printf "Starting network: "
/sbin/ifup -a
```

stoping network
```
printf "Stopping network: "
/sbin/ifdown -a
[ $? = 0 ] && echo "OK" || echo "FAIL"
/sbin/sysctl -w net.core.rmem_default=163840
/sbin/sysctl -w net.core.wmem_default=163840
/sbin/sysctl -w net.core.rmem_max=163840
/sbin/sysctl -w net.core.wmem_max=163840
```   

## dos2unix  

doc2unix is a binary function to convert WINDOW EOL file to UNIX format  

usage:  
```
$ doc2unix <regex-file>
```

## tar  

```
Packaging only
$ tar cvf <FileName>.tar <DirName>

Unpack
$ tar xvf <FileName>.tar
```

```
compress to gzip
$ tar zcvf <FileName>.tar.gz <DirName>

extract from gzip
$ tar zxvf <FileName>.tar.gz
```

## sh

```
for i in `ls ./*.txt`; do
    @echo dos2unix $i;
    dos2unix $i;
done
```  

## clean  

```
$ clear && printf '\e[3J'
```

## objdump  

similar to readelf  

check cross-compiler for binary file  
```
objdump -s --section .comment <elf>
```

## readelf  

read elf related header dynamic so 

```
readelf -d library.so
```

```
-a (all)
-h file header
-e all headers (similar to -h -l -s)
-d show dynamic sections
```

## nm  

list all symbol in the objects  

```
nm <object>
```

## module  

module load specific modules which define specific linux environ variables
we can specify multiple module files for project switching

```
/* $HOME/.modulefiles/project-0 */
family("jls")

help([[
  Module description
]])

-- Buildroot --
setenv("BR_DIR", "/tools/buildroot/dl")

-- Cross toolchain Root Dir --
CROSS_TOOL = "/tools/arm-linux-gnueabihf"
setenv("CROSS_TOOL", CROSS_TOOL)
setenv("ARCH", "arm")
setenv("CROSS_COMPILE", "arm-linux-gnueabihf-")
prepend_path("PATH", XTOOL_PATH .. "/bin")

-- Project --
setenv("REPO_LINK", "http://github.com/choice17/repo/project0")
```

## strip  

remove all unused symbol note and debug message

for share library  
`${CROSS_COMPILE}strip --strip-debug --remove-section=.note --remove-section=.comment *.so`

for binary  
`${CROSS_COMPILE}strip <binary>`

## wc  

to count number of lines of a text  

`wc -l <text file>`  

or count number of lines for pipe output  

```bash 
  cat <file> | wc -l
  ls *.h | wc -l
  find . -name "*.h" | wc -i
```
