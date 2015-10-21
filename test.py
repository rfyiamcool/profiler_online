#cofing:utf-8
import gevent
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import requests
from profiler_online import run_profiler

run_profiler()

p = Pool(100)

def handler_request(url):
    print len(requests.get(url).content)

def fetch_data():
    def down(url):
        urls = ['http://www.baidu.com','http://www.sina.com.cn','http://www.163.com','http://www.oschina.net'] * 1000
        for url in urls:
            p.spawn(handler_request, url)
            p.join()
while 1:
    gevent.sleep(1)
