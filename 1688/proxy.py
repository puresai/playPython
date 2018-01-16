from common import commonDef as cf
import pdb
import time
from bs4 import BeautifulSoup

ip = "163.125.22.240"
port = "9999"
page = cf.proxy("https://s.1688.com/company/company_search.htm?keywords=%CA%D6%BB%FA&button_click=top&earseDirect=false&n=y&sortType=pop&pageSize=30&offset=3&beginPage=1", ("%s:%s")%(ip,port), "gbk")
# page = cf.proxy("http://api.xicidaili.com/free2016.txt", ("%s:%s")%(ip,port))
# page = cf.urlOpen("http://www.13sai.com")
print(page)
# contactsA = page.findAll('a', attrs = {"class", "sm-offerResult-areaaddress"})
# for href in contactsA:
# 	if href['href']:
# 		print(href['href'])
		# contactPage = cf.proxy(href['href'], ip, "gbk")
		# print(contactInfo)
		# time.sleep(2)