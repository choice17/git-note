# MICS  

## Content
* **[live555_build_for_Window](https://github.com/choice17/live555)**   
* **[XML schema](#xmlschema)**  
* **[jupyter Magic](#juptyermagic)**  
* **[linux cmd](#linuxcmd)**  
* **[pip venv](#pipvenv)**  
* **[conda venv](#condavenv)**  

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

