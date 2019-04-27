import bs4 as bs 
import sys 
import schedule 
import time  
from lxml import html 

from barcodelookup.models import Asin

from PyQt5.QtWebEngineWidgets import QWebEnginePage

class Page(QWebEnginePage): 

	def __init__(self, url): 
		from PyQt5.QtWidgets import QApplication 
		from PyQt5.QtWebEngineWidgets import QWebEnginePage 
		from PyQt5.QtCore import QUrl

		self.app = QApplication(sys.argv) 
		QWebEnginePage.__init__(self) 
		self.html = '' 
		self.loadFinished.connect(self._on_load_finished) 
		self.load(QUrl(url)) 
		self.app.exec_() 

	def _on_load_finished(self): 
		self.html = self.toHtml(self.Callable) 
		print('Load finished') 

	def Callable(self, html_str): 
		self.html = html_str 
		self.app.quit() 

def exact_url(url): 
	index = url.find("B0") 
	index = index + 10
	current_url = "" 
	current_url = url[:index] 
	return current_url 
	


def check(url): 
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'} 
	
	# adding headers to show that you are 
	# a browser who is sending GET request
	import requests
	from time import sleep
	from lxml import html
	page = requests.get(url, headers = headers)  
	for i in range(20): 
		# because continuous checks in  
		# milliseconds or few seconds 
		# blocks your request 
		sleep(3)  
		
		# parsing the html content 
		doc = html.fromstring(page.content) 
		
		# checking availaility 
		XPATH_AVAILABILITY = '//div[@id ="availability"]//text()'
		RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY) 
		AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
		return AVAILABILITY 





from time import sleep


url_base = "https://www.amazon.in/dp/{}"
while True:
	asins = Asin.objects.filter(checked=False)
	for asin in asins:
		url = url_base.format(asin.asin)
		exacturl = exact_url(url) # main url to extract data 
		page = Page(exacturl) 
		soup = bs.BeautifulSoup(page.html, 'html.parser') 
		js_test = soup.find('span', id ='priceblock_ourprice') 
		if js_test is None: 
			js_test = soup.find('span', id ='priceblock_dealprice')		 
		str1 = "" 
		for line in js_test.stripped_strings : 
			str1 = line 


		price = int(float(str1.replace(", ", "")))
		ans = check(url)
		availability = False
		if ans.find("In stock") != -1:
			availability = True

		asin.price = price
		asin.is_available = availability
		asin.checked = True
		asin.save()
		print("Price = "+str(price)+" availability= "+ ans)
	sleep(5)