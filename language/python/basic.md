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
* **[class](../../data_structure/python/class.md)

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
```
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

