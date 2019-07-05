## WEBCRAWLING

* **[financial-website](#financialwebsite)**  
* **[crawling-intro](#crawlingintro)**  
* **[robots.txt](#robots.txt)**  

## financialwebsite  

* [yahoo](https://finance.yahoo.com/quote/)[]
* [wantgoo](https://www.wantgoo.com/global)

## crawlingintro  

!The following content is based on/refer to the intro website!  

* [intro](https://medium.com/velotio-perspectives/web-scraping-introduction-best-practices-caveats-9cbf4acc8d0f)

h2. pythonlib

h3. Requests 
```python
import requests
r = requests.get("https://velotio.com") #Fetch HTML Page
```
h3. BeautifulSoup  
```python
from bs4 import BeautifulSoup
import requests
r = requests.get("https://velotio.com") #Fetch HTML Page
soup = BeautifulSoup(r.text, "html.parser") #Parse HTML Page
print "Webpage Title:" + soup.title.string
print "Fetch All Links:" soup.find_all('a')
```
h3. scrapy
```python
$cat > myspider.py <<EOF
import scrapy
class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']
    def parse(self, response):
        for title in response.css('h2.entry-title'):
            yield {'title': title.css('a ::text').extract_first()}
EOF
 scrapy runspider myspider.py
```

h2. CHALLENGES 

* warehousing  
** AWS [link-to-setup-AWS-crawling](https://medium.com/@raoshashank/free-cloud-based-data-scraping-using-aws-e111a950e6b5)  
** structured data (relational database service)  
** DynamoDB (non-relational database)  
* Pattern Changes  
** test regularly  
* Anti-Scraping Technologies  
** Proxy services with rotating IP Addresses help in this regard
** Scrapy provides several rotation proxy services

h2. Scraping Guidelines/ Best Practices

* Take care of robots.txt file (instruct search engine robots)  
* Do not hit the servers too frequently, add sleep time  
* User Agent Rotation and Spoofing  
** For Scrapy, set USER_AGENT property in settings.py. Format as: ‘myspidername: myemailaddress’
* Scrape during off-peak hours   

## robots.txt  

** [intro-for-robots.txt](https://moz.com/learn/seo/robotstxt)  

It is specified for search engine robots

* User-agent   
* Disallow 
* Allow   
* Crawl-delay  
* Sitemap 
