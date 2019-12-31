# MICS  

## Content
* **[live555_build_for_Window](https://github.com/choice17/live555)**   
* **[XML schema](#xmlschema)**  
* **[jupyter Magic](#juptyermagic)**  
* **[linux cmd](#linuxcmd)**  
* **[pip venv](#pipvenv)**  
* **[conda venv](#condavenv)**  
* **[mount nfs](#mountnfs)**  

## xmlschema

*  [xml schema validator](https://www.liquid-technologies.com/online-xsd-validator)  
*  [xml schema](http://www.utilities-online.info/xsdvalidation/#.XGOBIVUzaUl)  

## jupytermagic  

* [reference](https://ipython.org/ipython-doc/3/interactive/reference.html)  

## linuxcmd  

**rename**  file name
`$ rename -v "s/<origin>/<replace>/g" *<file>`  

**sed** rename file content inplace
`$ sed -i "s/<origin>/<replace>/g" *<file>`  

**time**   
**forloop**  
`time -p bash -c "for (( i=0; i<10; i++ )); do command1; command2; done;"`  
`time (for i in {1..10}; do sleep 1 ; done)`  

## pipvenv  

```python
$ python -m venv build_env
$ cd build_env
$ cd Script\activate.bat
```

## condavenv

```python
$ conda create --name <myenv> python=<3.4> --no-default-packages
```

## mountnfs

```
Mount nfs

connect nfs
https://www.hanewin.net/nfs-e.htm
Goto "NFS" page and setup as in the picture below.

mount port 1058
server port 2049
udp thread 4
30000 bytes transfer size
udp /tcp
nfs server ver 2/3
async
allow unix emulate hard link

export page -> edit export files

Add
<NFS path> -name:usbnfs -maproot:0 -umask:000  -public
ex.
D:/ethnfs -name:ethfs -maproot:0 -umask:000  -public -name ethnfs

restart server
```

