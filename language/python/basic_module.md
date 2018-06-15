# python module  

## content table
* **[subprocess](#subprocess)**
* **[threading_queue](#threading&queue)**
* **[os](#os)**
* **[sys](#sys)**
* **[time&datetime](#time&datetime)**
* **[binascii](#binascii)**
* **[re](#re)**
* **[socket](#socket)**  
* **[urllib](#urllib)**

### subprocess
able to communicate to cmd.exe  
```python  
import subprocess as sp
cmd = 'ffmpeg -re -i url -f mpegts -'
proc = sp.open(cmd,stdout=sp.PIPE)
msg = proc.stdout.readline().strip()
```

### threading_queue
able to do threading operation  
```python
import threading
import queue
import time
class Foo:
	def __init__(self):
		self.thread = {}
		self.lock = threading.Lock()
		self.__create_config()
		self.__daemon()

	def bar(a,q):
		while True:
			self.lock.acquire()
			with self.lock:
				time.sleep(a)
				q.put(a)
				self.lock.release()

	def __create_config():
		self.q = queue.Queue()
		self.thread[0] = threading.Thread(target=self.bar,args=(0.5,self.q))
		self.thread[1] = threading.Thread(target=self.bar,args=(1,self.q))

	def __daemon():
		self.thread[0].setDaemon(True)
		self.thread[1].setDaemon(True)

	def start():
		self.thread[0].start()
		self.thread[1].start()

	def play():
		while True:
			try:
				val = q.get(True)
			except queue.Empty:
				pass
			print(val)

```
### os
```python
import os
curdir = os.getcwd()
dirname = os.path.dirname(curdir)
```
### sys
```python
import sys
sys.path.add(dirname)
sys.name()
```
### time&datetime
```python
import time
ti = time.time()
toc = time.time() - ti

import datetime
today_time = datetime.datetime(2002,5,12,0,0,0)
dt = datetime.timedelta(seconds=100)
det = today_time - dt
det.microseconds
det.hours
det.minutes
(yy,mm,dd,hh,mm,ss,ffff) = det.timetuple()
```
### binascii  
```python
import binascii as bi
b = 'saf342r32'
h = bi.hexify(bytes(b),'utf-8')
uh = bi.unhexify(h)
```

### re  
(regular expression)  
with wild card  
- re.findall  
> [0-9]+  
> ^F.+   
> ^F.+?  
> \S+@\S+
> ()  
> [^ ] 
- re.find  


```python
import re
x = 'My 2 favorite numbers are 19 and 42'
y = re.findall('[0-9]+',x)
print(y)
```
`['2','19','42']`

```python
x = 'From: Using the : character'
y = re.findall('^F.+:',x)
print(y)
````
`['From: Using the :']`
`^F` first match character  
`.+:` greedy as big as possible, one or more char, last character match  

```python
y = re.findall('^F.+?:',x)
print(y)
```
`['From:']` 
`F.+?` first match, one or more, not greedy, last match 

```python
x = 'from stephen.hi@uct.ac.za sat jan 5 000:00:00 2008'
y = re.findall('\S+@\S+',x)
print(y)
```
`['stephen.hi@uct.ac.za']`   
`\S+@\S+`  at least one-non-whitespace char, `@` char match, `+` greedy  


```python
y = re.findall('^From (\S+@\S+)',x))
```
`['stephen.hi@uct.ac.za']`  
`()` highlight the return parition  

```python 
x = 'from stephen.hi@uct.ac.za sat jan 5 000:00:00 2008'
w = x.split()[1].split('@')[1]
<-->
w = re.findall('@([^ ]*)',x)
<-->
w = re.findall('^From .*@([^ ]*)',x)
print(w)
```
`['uct.ac.za']`  
`@([^ ]*)`  `[^ ]` <- match non-blank char, * match many of them  

```python
x = 'we have $10.00 dollars for cookies'  
y = re.findall('\$[0-9.]+',x)
print(y)
```
`['$10.00']`

### socket  
- TCP  
```python
import socket as s

y = s.socket(s.AF_INET, s.SOCK_STREAM)
y.connect(('data.pr4e.org',80))
cmd = 'GET http://data.pr4e.org/romeo.txt HTTPS/1.0\r\n\r\n'.encode()
y.send(cmd)

while True:
	d = y.recv(512)
	if len(d)<1:
		break
	print(d.decode())
y.close()
```

### urllib
```python
import urllib.request, urllib.parse, urllib.error

fhand = urllib.request('http://data.pr4e.org/romeo.txt')
for line in fhand:
	print(line.decode().strip())
```

