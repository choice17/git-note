# python module  

## content table
* **[subprocess](#subprocess)**
* **[threading_queue](#threading&queue)**
* **[os](#os)**
* **[sys](#sys)**
* **[time&datetime](#time&datetime)**
* **[binascii](#binascii)**

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