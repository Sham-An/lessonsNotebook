from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
import re
#Возвращает адрес http://icanhazip.com/
######################FIND PROXIES#########################################
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:299]:   #299 proxies max
        proxy = ":".join([i.xpath('.//td[1]/text()')
        [0],i.xpath('.//td[2]/text()')[0]])
        proxies.add(proxy)
    return proxies



######################write to file in format   IP:PORT######################
try:
    proxies = get_proxies()
    f=open('proxy_list.txt','w')
    for proxy in proxies:
        f.write(proxy+'\n')
    f.close()
    print ("DONE")
except:
    print ("MAJOR ERROR")