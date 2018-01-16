from common import commonDef as cf
import pdb
import os


iptxt = os.path.abspath('ip.txt')
page = cf.urlOpen("http://www.xicidaili.com/wn/")
trs = page.find("a", attrs = {"id": "ip_list"}).findAll("tr")
i = 0
for tr in trs:
	i = i + 1
	if i > 1:
		tds = tr.findAll("td")
		ip = tds[1]
		port = tds[2]
		if cf.checkIP(("%s:%s")%(ip, port)):
			cf.writeFile(("%s:%s,")%(ip, port), iptxt)