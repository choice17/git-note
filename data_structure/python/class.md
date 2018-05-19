# python class inheritance

## class inheritance  
```python 
#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
class FooParent(object):
    def __init__(self):
        self.parent = 'I\'m the parent.'
        print ('Parent')
    
    def bar(self,message):
        print ("%s from Parent" % message)
 
class FooChild(FooParent):
    def __init__(self):
        # super(FooChild,self) 
        super(FooChild,self).__init__()    
        print ('Child')
        
    def bar(self,message):
        super(FooChild, self).bar(message)
        print ('Child bar fuction')
        print (self.parent)
 
if __name__ == '__main__':
    fooChild = FooChild()
    fooChild.bar('HelloWorld')
```

## private  

* python use __ var to declare private
* here Fon override method callbar()
* below shows the static class with private var counter
* here Fon prompt error caller __ counter

```python
class Kon(object):
    __counter = 0

    @staticmethod
    def callbar():        
        bar.calling()        
        Kon.__counter =  Kon.__counter + 1
        print('static class var counter: %d'%Kon.__counter)

class Fon(Kon):
    @staticmethod
    def callbar():
        bar.calling()        
        Fon.__counter =  Fon.__counter + 1
        print('static class var counter: %d'%Fon.__counter)
```


## import module

* make sure there is no cyclic dependency
* here assume the package as below
```
tool/
	|--mod1/
	|    |--__init__.py
	|    |--foo1.py
	|--mod2/
	|    |--__init__.py
	|    |--foo2.py
	|    |--foo3.py
	|--test/
	|	 |--script.py
	|--__init__.py
	|--tool.py
```

* **in simplest way, try to insert path inside every module**

```python
import sys
import os
sys.path.insert(0,os.path.dirname(os.getcwd()))
```

* one more option is to import module inside class/function

```python
#foo2.py
class foo2:
	import mod1.foo1 as foo1
	def __init__(self):
		...
```

