import urllib.request as request
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import socket
import pdb

# BeautifulSoup转换
def soup(str, code = "html.parser"):
	return BeautifulSoup(str, code)

# 爬取页面
def urlOpen(url, charset = "utf-8", header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}):
	req = request.Request(url, header)
	res = request.urlopen(req).read().decode(charset)
	return soup(iUrl)

# 爬取图片
def getImg(imgUrl, path):
	urlretrieve(imgUrl, path)

# 获取IP
def getIp():
	myname = socket.getfqdn(socket.gethostname())
	return socket.gethostbyname(myname)

# 代理IP访问页面
def proxy(url, ip, charset = "utf-8"):
	httpproxy_handler = request.ProxyHandler({"http" : ip, "https" : ip})
	opener = request.build_opener(request.HTTPHandler, httpproxy_handler)
	req = request.Request(url)
	request.install_opener(opener)
	response = opener.open(req)
	return soup(response.read().decode(charset))

# 验证IP有效性
def checkIP(ip):
	try:
		proxy("http://httpbin.org/get", ip)
		return true
	except:
		return false

# 写文件
def writeFile(content, path):
	try:
		with open(path, 'w+') as f:
			f.write(content)
	finally:
		if f:
			f.close()