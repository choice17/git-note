# python basic command  

* **[operator](#operator)**
* **[None](#None)**
* **[int](#int)**  
* **[string](#string)** 
* **[float](#float)**  
* **[bool](#bool)**
* **[list](#list)** 
* **[tuple](#tuple)**  
* **[dict](#dict)**
* **[if](#if)**
* **[for](#for)**  
* **[while](#while)**
* **[try](#try)** 
* **[misc](#misc)**
* **[def](#def)**
* **[class](../../data_structure/python/class.md)**
* **[function decorator](#funcdeco)**  


### operator  
here python supports several operators:  
```python
+ - // / % * ** () {} & | and or not is 
a = 1 + 2
# a = 3
b = 1 + .6
# b = 1.6
c = a-b
# c = 1.4
d = c*a
# d = 4.2
e = 2**a
# e = 8
f = e//2
# f = 4
f = 3.2//2
# f = 1
g = 24%20
# g = 4
```
### None
which a good tool to declare a variable    
```python
a = None
a is None
# ans = True
a = 1 
a is not None
# ans = True
```
### int
```python
a = 3
a = int(3.2)
a = int('3')
# ans = 3
```
### string
```python
a = ''
a = 'hello world'
a = "hello world"
''.join('i am here')
'i am here'.find('here')
# ans = 5 
'hi ' + 'i am here'
# ans = 'hi i am here'
'HI I am Here'.strip().lower()
# ans = 'hi i am here'
a = b'i am here'
# bytes ascii b'i am here'
b = a.decode('utf-8')
# ans = 'i am here'
```
### float  
### list  
```python
a = [1,2,3]
a.append(4)
# ans = [1,2,3,4]
a + [5,6]
# ans = [1,2,3,4,5,6]
a.pop()
# ans = 1, a->[2,3,4,5,6]
len(a)
# ans = 5
b = [[1,2,3],[1,2,3]] #array
[ i for i in a]
# ans = [2,3,4,5,6]
c = ['i','am','here']
d = [(1,2,3),(1,2,4),(5)]
d[0]
# ans = (1,2,3)
e = [{'a':3,'b':4,5:100},{'e':1000,'f':'red','d':[1,2,3]}]
e[2]['e']
# ans = 1000
```
### tuple 
which has similar behavior to list  
```python  
a = (1,2)
b = ([1,23],[2,3])  
```
### dict
which is powerful but has a unique id inside it  
```python
a = {'a': 'b','c':12,'d':[1,2,3],'e':(1,2),'f':{} }
a.keys()
# ['a','b','c','d','e','f']
a.values()
# dict value ['b','c',12,[1,2,3],(1,2),{}]
```
### for  
```python
for i in range(5):
	print(i)
# ans = 0 1 2 3 4 
[i for i in range(5)]
# ans = [0 1 2 3 4]
```
### while  
```python 
i = 0
while True:
	time.sleep(1)
	print(i)
    i = i + 1
    if i==5:
        break
# ans= 0 1 2 3 4 
```
### try
```python
try:
	print(noA)
except NameError as e:
	print(e)
	raise ValueError("Not yet assign noA!") from e

# ans = NameError referenced to variable not declared  
try:
	print(noA)
except NameError as e:
	print(e)
finally:
	noA = 3
	print(noA)
#  ans = NameError referenced to variable not declared  
#  ans = 3
```
### misc
```python
# comment here
def foo():
	'''
	docstr
	which is to describe a func, module
	'''
	"""
	or double quote
	""" 
	pass
```
### def
```python
def func(a,b:int,c=10,d:list):
	print(a,b,c,d)
	return(a,b,c)
e = func('a',3,d=[1,2,3])
# ans = 'a',3,10,[1,2,3]
a,b,c,d = e
```
```python
def foo(a,b=None,c=4,*args,**kwargs):
	print(a,b)
	for i in args:
		print('position args: 'i)
	for k,v in kwargs.items():
		print('optional args %s (*kwargs'): %s' % (k,v)
foo(1,2,3,5,6,a=3,b=6)
#ans:
(1,2)
position args: 5 
position args: 6
'option args a (*kwargs): 3'
'option args b (*kwargs): 6'
```
### funcdeco  

**Basic**  
```python  
class FOO(object):
    def route(self, name):

        def wrapper(fn):
            print("registered FOO ", name)
        
            def ret_fn(*args):
                print("hello world from FOO TOP")
                ret =  fn(*args)
                print("hello world from FOO BOTTOM")
                return ret
            return ret_fn

        return wrapper

app = FOO()

@app.route("/get")
def sayhi(*args):
    print("say something: %s!", args)
```

At the function registeration, it will print

```bash
registered FOO  /get
```

```python
sayhi("say hi here")
```

And to call sayhi function would output  

```bash
hello world from FOO TOP
say something: %s! ('hi',)
hello world from FOO BOTTOM
```

**Advanced**  

Let's Look at more advance usage

```python
class BAR(FOO):

    def route(self, name):

        def wrapper(fn):
            print("registered from BAR ", name)
            a = super(BAR, self).route(name)(fn)
            def ret_fn(*args):
                print("hello world from BAR TOP")             
                ret = a(*args)
                print("hello world from BAR BOTTOM")
                return ret
            return ret_fn

        return wrapper

app = BAR()

@app.route("/get")
def sayhi(*args):
    print("say something: %s!", args)
    
```

Here BAR is super class from FOO, and super the decorator route.
It outputs followings at the function registration.

```python
registered from BAR  /get
registered FOO  /get
```

Let's see the output of `sayhi("hi")`  

```bash
hello world from BAR TOP
hello world from FOO TOP
say something: %s! ('hi',)
hello world from FOO BOTTOM
hello world from BAR BOTTOM
```
Hence, using function decoration helps to raise abstract level of code and simplify usage! cheers!  

Here lets take a look into log time class
```python
class LOGGER(object):
    
    __slots__ = ('log')
    def __init__(self):
        self.log ={}

    def logTime(self, name):

        def ret_fn(fn):
            key = "%s_%s"%(name,fn.__name__)
            self.log[key] = 0
            def wrapper(*args, **kwargs):
                ti = T.time()
                ret = fn(*args, **kwargs)
                self.log[key] = T.time() - ti            
                return ret

            return wrapper

        return ret_fn	

log = LOGGER()

class BAR(FOO):
///////////////////////
    @log.logTime("BAR")
    def play(self):
        T.sleep(1)
        print("i am playing!")
```
```python
app = BAR()
app.play()
print(log.log)
```
```bash
{'BAR_play': 0.9998998641967773}
```
