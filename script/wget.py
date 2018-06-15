import urllib.request as ur
import sys
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
