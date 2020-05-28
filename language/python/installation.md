## python installation 

## table of content  
* **[window](#window)**  
* **[linux](#linux)**  
* **[virtual env](#virtual_env)**  

### window  

* install anaconda  
**`step`**
1. **[download anaconda](https://repo.continuum.io/archive/)**  
anaconda2.x.x - using python2 as default  
anaconda3.x.x - using python3 as default  
2. run .exe  
3. pip3 
4. install python lib  
5. install python IDE    
`default`  
> spyder3  
> jupyter ipython    
`other`  
> PyCharm  
> VSCode 
6. install git  
7. package management  
> conda list  
> conda remove  
> pip list  
> pip uninstall  

### linux  

1. update pip  
2. install python lib  
3. install python IDE    
`default`  
> spyder3  
> jupyter ipython   
> git   
`other`  
> PyCharm  
> VSCode 
4. pip command  
> sudo pip -> install into global  
> pip -> install globally if not specify  
> pip install --user -> install locally `~/.local/lib/`

### virtual_env  

* [link](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/)  

* show version  
`$ conda -V`  

* update  
`$conda update conda`  

* create env  
```
conda create -n yourenvname python=x.x
=> activate <yourenvname>
conda create -p <prefix> python=x.x
=> activate <prefix>
```  

* activate env  
`source activate yourenvname`  

* install package  
`conda install <>`  

* remove env  
`conda remove -n yourenvname -all`

* import env  
`conda env create -f environment.yml`

* export env  
`conda env export > my_environment.yml`  
