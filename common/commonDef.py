# 爬取页面
def urlOpen(url, charset = 'utf-8'):
	from urllib.request import urlopen 
	from bs4 import BeautifulSoup
	iUrl = urlopen(url).read().decode(charset)
	return BeautifulSoup(iUrl, "html.parser")

# 爬取图片
def getImg(imgUrl, path):
	from urllib.request import urlretrieve
	urlretrieve(imgUrl, path)