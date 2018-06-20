import re
import urllib.request
import urllib.error
import urllib.parse
import json
from mysql import MySQL
import sys
import pymysql

def getLists(url):
    header={    #请求头部
	   'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	   'Referer': 'https://music.163.com/search/'
	}
    #post请求表单数据
    data={
    	'params':'oOT52xB1xHd5z7jrDscArZKPRkHvp3GsCJ6Bd6pp1/5SR1za1EdQ2MLBK60s9oYLw+gf579TSvTayuokrXerKTJxuAE18WYLQ0HGplQoN1BVp/GrJAgthI/4TBqhulpAo+FYSkR/O08pSqv3gkaEkZGM9o6zpffgNdDN/CdqYtE6XkW7nXPGhX4E77q1POgCHduo1/1lmBaFxsluyWViQGzsOaIW3hRVx8tLOrXTMhljq7mRpMO0v6maiI8PS8jTs6NSLzESeAzDQwGRf1i0V8P21qO4b1GWYus6ekK62EFN+Nx+z3tnjZCNHWJi5g/SStzni7cxRwxLH3+neSaER99iTPbgICGHQlbXr9JFcAY=',
    	'encSecKey':'c037b9e1af0c9980e3584055e2b2289001da0b9de7b9f8e272d8d6a8f29d6ada179da272b5625b343c1f74cec4a93cc76601c7f37b997146d456ab4822fcd605394b83e4de653cf0a9861e9e6fa398aaa60455477f04835fad53f6fb535045a36bd6e548cd71caaefea983f31be1a68d5e2aa2cab86513a3f40eda5c85e276ec'
    }
    postdata=urllib.parse.urlencode(data).encode('utf8')  #进行编码
    request=urllib.request.Request(url,headers=header,data=postdata)
    reponse=urllib.request.urlopen(request).read().decode('utf8')
    songlist = json.loads(reponse)['result']['songs'];
    mysqlObj = MySQL()
    for song in songlist:
    	mysqlObj.insert('songlist', 'sid, name, author', '%s,"%s","%s"'%(song['id'], song['name'], song['ar'][0]['name']))
    	print(song['id'])


getLists('https://music.163.com/weapi/cloudsearch/get/web?csrf_token=')

def getSongLists():
    mysqlOby = MySQL()
    return mysqlOby.findAll('songlist', 'id > 0', 'sid, name')

def getCommtents(hot_song_id, hot_song_name):
    url='http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(hot_song_id) + '?csrf_token='   #歌评url
    header={    #请求头部
	   'User-Agent':'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
	}
    #post请求表单数据
    data={
    	'params':'zC7fzWBKxxsm6TZ3PiRjd056g9iGHtbtc8vjTpBXshKIboaPnUyAXKze+KNi9QiEz/IieyRnZfNztp7yvTFyBXOlVQP/JdYNZw2+GRQDg7grOR2ZjroqoOU2z0TNhy+qDHKSV8ZXOnxUF93w3DA51ADDQHB0IngL+v6N8KthdVZeZBe0d3EsUFS8ZJltNRUJ',
    	'encSecKey':'4801507e42c326dfc6b50539395a4fe417594f7cf122cf3d061d1447372ba3aa804541a8ae3b3811c081eb0f2b71827850af59af411a10a1795f7a16a5189d163bc9f67b3d1907f5e6fac652f7ef66e5a1f12d6949be851fcf4f39a0c2379580a040dc53b306d5c807bf313cc0e8f39bf7d35de691c497cda1d436b808549acc'
    }
    postdata=urllib.parse.urlencode(data).encode('utf8')  #进行编码
    request=urllib.request.Request(url,headers=header,data=postdata)
    reponse=urllib.request.urlopen(request).read().decode('utf8')
    json_dict=json.loads(reponse)   #获取json
    hot_commit=json_dict['hotComments']  #获取json中的热门评论

    mysqlObj = MySQL()
    for item in hot_commit:
    	mysqlObj.insert('commentlist', 'sid, nickname, content, likedCount', '%s,"%s","%s","%s"'%(hot_song_id, pymysql.escape_string(item['user']['nickname']), pymysql.escape_string(item['content']), item['likedCount']))

songLists = getSongLists();

num=0
while num < len(songLists):    #保存所有热歌榜中的热评
    print('正在抓取第%d首歌曲热评...'%(num+1))
    getCommtents(songLists[num]['sid'], songLists[num]['name'])
    print('第%d首歌曲热评抓取成功'%(num+1))
    num+=1