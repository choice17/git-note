# python module  

## content table  
* **[subprocess](#subprocess)**  
* **[threading_queue](#threading&queue)**  
* **[os](#os)**  
* **[sys](#sys)**  
* **[time&datetime](#time&datetime)**  
* **[binascii](#binascii)**  
* **[struct](#struct)**  
* **[re](#re)**  
* **[socket](#socket)**  
* **[urllib](#urllib)**  
* **[beautifulSoup](#beautifulSoup)**  
* **[xmlparser](#xmlparser)**  
* **[jsonparser](#jsonparser)**  
* **[argparser](#argparser)**  
* **[configparser](#configparser)**  
* **[pyinstaller](#pyinstaller)**  
* **[cpython](#cpython)**

### subprocess
able to communicate to cmd.exe  
```python  
import subprocess as sp
cmd = 'ffmpeg -re -i url -f mpegts -'
proc = sp.Popen(cmd,stdout=sp.PIPE)
msg = proc.stdout.readline().strip()
```
when calling Popen, with option `buff=100000` allows generally large buffer for stdout  
then you can read it with your choice  
for example, we can easily read a image pixel value with 
`cmd = 'ffmpeg -i rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov -map v:0 -an -f image2pipe  -vcodec rawvideo -s:v 480x320 -pix_fmt rgb24 - `
```python 
''' inside thread '''
proc = sp.Popen(cmd,stdout=sp.PIPE, buffsize=100000)
raw_msg = proc.stdout.read(480*320*3)
queue1.put(raw_msg)
''' the other thread, queue with False disable blocking '''
raw_msg = queue1.get(False)
image = np.fromstring(raw_msg).reshape(480,320,3)

```
alternatively it can use `Popen` with communicate to allow write completion of file
```ptyhon
cmd = 'dir'
proc = sp.Popen(cmd,stdout=sp.PIPE)
file = proc.stdout.communicate()
with line in file.readlines():
	print(line.decode().split()[0])
> c:\program\file1
> c:\program\file2
> ...
```
simple use call function without any
```python
sp.Call('echo hi')
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

### struct 
struct is a module manipulate binary and hex parsing for writing file  
major function is `S.pack(format_str, number)` and `S.unpack(format_str, b'str')`
> 'H': unsigned short int, 'h': signed short  
> 'B': unsigned binary, 'b': signed binary  
> 'L': unsigned int, 'l': signed int   
> '>': big endian, '<': little endian   
`\xff\x00` means 2 bytes in little endian such that 00 ff => 65535 
```python
import struct as S
number1 = 65535
c = S.pack('H', number1)
print(c)
> b'\xff\xff'
S.unpack('H', c)
> (65535,)
c = S.pack('L', number1)
> b'\xff\xff\x00\x00'
S.unpack('L', c)
> (65535,)
```

there is more than struct allowing binary and hex conversion  
```python  
bin(65535)
> '0b111111111111111111' => '1111 1111 1111 1111'
bin(0o12)
> '0b1010'
bin(0x0f)
> '0b1111'
hex(65535)
> '0xff' 
hex(0o10)
> '0x8'
hex(0b1111)
> '0xf'
```

python3 also support str.format to parse binary/hex value  
```python
'{:04x}'.format(16)
> '0010'
'{:04d}'.format(345)
> '0345'
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
- python lib to do basic network command on socket  
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
- python lib to utilize url urllib.request  
```python
import urllib.request

fhand = urllib.request('http://data.pr4e.org/romeo.txt')
for line in fhand:
	print(line.decode().strip())
```

```python
import urllib.request as ur
def download_url(url_,target=None):
	
	file = url_[-url_[::-1].find('/'):]
	if target is not None:
		file = target
	print('save to %s'%file)
	ur.urlretrieve(url_,file,cbk)	
def cbk(a,b,c):  
    '''''return 
    @a:downloaded%
    @b:datasize 
    @c:remotesize 
    '''      
    process = round(min(100, (a * b) / c * 100),1)
    _str = "\u2588"*int(process/5)+ "% 3.1f%% of %d bytes" % (process, c)
    print (_str ,end= '\r' )
    
if __name__ == '__main__':	
	target = sys.argv[2] if len(sys.argv) == 3 else None
	download_url(sys.argv[1],target)
	```

### beautifulSoup  
python lib to parse html  
```python
import urllib.request as UR, urllib.parse as UP, urllib.error as UE
from bs4 import BeautifulSoup as B
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html = UR.urlopen(url, context=ctx).read()
soup = B(html, 'html.parser')
tags = soup('a')
for tag in tags:    
    print ('URL:',tag.get('href', None))
```
`soup('a')` search tag with name 'a', which usually binds with href here   

### xmlparser  
parse xml
> http://py4e-data.dr-chuck.net/comments_42.xml
> <comments>
>   <comment>
>    <name>Matthias</name>
>    <count>97</count>
>   </comment>
>  <comment> 
>	...
> <comments>  

```python  
import urllib.request as UR, urllib.parse as UP, urllib.error as UE
from bs4 import BeautifulSoup as B
import ssl
import xml.etree.ElementTree as ET

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#url = 'http://py4e-data.dr-chuck.net/comments_42.xml'
url = input('Enter URL: ')
html = UR.urlopen(url, context=ctx).read()
soup = B(html, 'html.parser')

print('Do it with beautifulSoup================')
tags = soup('comment')
_sum  = 0
for tag in tags:
    name = tag.find('name').contents[0]    
    count =  int(tag.find('count').contents[0])
    _sum += count
    print ('name: %s, count: %d'%(name,count))
print('final sum: %d'%_sum)
print('Do it with xmlparser================')

_xml = ET.fromstring(html)
_comments = _xml.find('comments')
_sum = 0
for comment in _comments:
    name  = comment.find('name').text
    count = int(comment.find('count').text)
    _sum += count
    print ('name: %s, count: %d'%(name,count))
print('final sum: %d'%_sum)
```

or sum up counts by call `counts = _xml.findall('.//count')`    

### jsonparser 
python lib to parse json  
```python 
import urllib.request as UR, urllib.parse as UP, urllib.error as UE
import json
import ssl


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#url = 'http://py4e-data.dr-chuck.net/comments_42.json'
url = input('Enter URL: ')
html = UR.urlopen(url, context=ctx).read()

info = json.loads(html)
_sum  = 0
for item in info['comments']:

    name = item['name']
    count =  item['count']
    _sum += count
    print ('name: %s, count: %d'%(name,count))
print('final sum: %d'%_sum)
```
`json.loads` return python dictionary as the format of json  

## argparser  
argparser allows parsing sys input  
```python
'''parser.py'''
import argparser as arg

def parser_func():
	parser = arg.ArgumentParser()
	parser.add_argument('-v','--verbose',type=int,default=0,help_in='0: open, 1:close')
	return arg.parse_args()

if __name__ == '__main__':
	print(parser_func().verbose)
```
```bash
python parser.py 
>> 0
python parser.py -v 1
>> 1
python parser.py -h 
>> show help ...
```
to access action item in parser  
```python
def change_action(parser,dest_in, help_in):
	for action in parser._actions():
		if dest_in == action.dest_in:
			action.help_in = help_in
```
allow repeating the parser for different application -> def userspace  
```python
import argparser
class UserNamespace(object):
    pass
user_namespace = UserNamespace()
app_parser = argparser.ArgumentParser(add_help=False)
app_parser.add_argument('-app','--app',help='')
app_parser.add_argument('-h','--help',action='store_true',help='')
args,_ = app_parser.parse_known_args(namespace=user_namespace)
if args.args.help:
	print('help')
service_parser = argparser.ArgumentParser()
service_parser.add_argument('-s','--service',help='service command')
args,_ = app_parser.parse_known_args(namespace=user_namespace)
```



## configparser  
configparser allows parsing config.ini file  
```python 
'''in config file'''
[DEFAULT]
fun1=foo
fun2=bar

[SETUP]
fun1=handsome
```
```python
'''main script'''
import configparser as C
config = configparser.Configparser()
config.read('config.ini')
config.sections()
['DEFAULT','SETUP']
config['DEFAULT']['fun1']
>> foo
config['SETUP']['fun1']
>> handsome
```

## pyinstaller  
pyinstaller help to create window application .exe file from .py  
one line installation script:  
`pip install pyinstaller`
one line execute py to exe  
`pyinstaller <-F> app.py `

** more options  
1. create spec file  
```python
pyi-makespec -F app.py
```
2. edit the spec file or checkout <path-to-pyinstaller\hook\> to know the availability of library access   
```python   
1. import sys  
2. sys.setrecursionlimit(10000) # <== to avoid overhead the limit  
3. binaries=['opencv_ffmpeg.dll'] # <== may need if ur using opencv-python 
4. excludes=['PyQt4','PyQt5'] # <== may induce error, but its fine for simple application
```
3. to compress the exe file, to take away abundant library manully in dist file (if not using -F option)  
4. go to <path-to-pyinstaller-lib\hook\hook-numpy.core.py>, comment the mkl-section to avoid install mkl into your exe, it may affect performace though.  

**NOTE**  
Per user case, we may want to provide template application code for user to define some simple function

For example  
[app.py](./pyinstaller/app.py)  
[print_app.py](./pyinstaller/print_app.py)  

`$ pyinstaller app.py -F` does not includes print_app.py  
BUT in RUNTIME, it can check print_app.py and import code from it.  


5. Create separate env for clean build pyinstaller

* create conda virtual env
```
$ conda create -n build_env python=3.5.5 --no-default-packages
```

* create conda env and set prefix to custom location
```
$ conda create -p $USER/local/env/py36 python=3.6.10 --no-default-packages
```

6. install packages
```
$ activate build_env
$ pip install pyinstaller==3.3.1
$ pip install msgpack
$ pip install pypiwin32
$ pip install opencv-python==3.4.1.15  
$ conda install av -c conda-forge
$ conda install -c conda-forge numpy openblas 
```

7. checking non-python static library   
a. move opencv_ffmpeg341_64.dll to building env (it locates at installed opencv folder)

8. Note. 

python pip package manager can always use under conda space. i.e. pip install -> conda_env/local/site-package

## cpython  

[link to cpython](./cpython/readme.md)




