#!/usr/bin/env python
# pip install -U requests[socks]
# pip install urllib3[socks]


# proxy list
# https://www.sslproxies.org

#from requests import Request, Session
import urllib3
from urllib3.contrib.socks import SOCKSProxyManager


""" my header 
to Proxy IP:PORT through socks proxy

CONNECT https://google.com

"""

#sslproxy = '206.189.47.247:3128'
sslproxy = '192.168.0.10'
sslproxyport = '3128'
destination = 'google.com:443'

pool = urllib3.HTTPConnectionPool(sslproxy, sslproxyport)
# pool.request('CONNECT ' + destination, '/') 	# does not pass off handling response when it only gets the status code with no other headers...
#resp = pool.request('CONNECT ' + destination, sslproxy) 
#resp = pool.request('CONNECT ', sslproxy+ ':' +sslproxyport) 
#resp = pool.request('CONNECT ' + sslproxy + ':' + sslproxyport, '/')
#resp = pool.request('CONNECT ' + sslproxy + ':' + sslproxyport, '/')
#import pdb; pdb.set_trace()
resp = pool.request('CONNECT ' + destination , '/')

print resp.status

#resp = pool.request('GET', '/', sslproxy)

#pool.SOCKSProxyManager('socks5://192.168.0.10:9050/')
#resp = proxy.request('CONNECT ' + destination, sslproxy)



#proxy = SOCKSProxyManager('socks5://192.168.0.10:9050/')
#resp = proxy.request('CONNECT ' + destination, sslproxy)

print resp.data

#s = Session()
#r = Request('CONNECT https://mail.gentoocloud.com', 'http://80.211.4.187:8080')
#
#prepped = r.prepare()
#
#resp = s.send(prepped,
#    proxies=proxy,
#)

#r = requests.connect("https://google.com", proxies=proxy)


#print resp.content


