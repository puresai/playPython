import urllib.request as urllib
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import socket
import pdb

# 爬取页面
def urlOpen(url, header, ip = '', charset = 'utf-8'):
	if(ip == ''):
		ip = getIp()
	proxies = {'http' : ip}
	proxy_support = urllib.ProxyHandler(proxies)
	opener = urllib.build_opener(proxy_support)
	urllib.install_opener(opener)
	req = urllib.Request(url, headers=header)
	print(1)
	pdb.set_trace()
	iUrl = urllib.urlopen(req).read().decode(charset)

	return BeautifulSoup(iUrl, "html.parser")

# 爬取图片
def getImg(imgUrl, path):
	urllib.urlretrieve(imgUrl, path)

# 获取IP
def getIp():
	myname = socket.getfqdn(socket.gethostname())
	return socket.gethostbyname(myname)