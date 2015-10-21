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
    urls = ['http://www.baidu.com','http://www.sina.com.cn','http://www.163.com','http://www.oschina.net'] * 100
    for url in urls:
        p.spawn(handler_request, url)
    p.join()

if __name__ == "__main__":
    while 1:
        fetch_data()
        gevent.sleep(3)
