#!/usr/bin/env python
# pip install -U requests[socks]
# pip install urllib3[socks]


# proxy list
# https://www.sslproxies.org

#from requests import Request, Session
#import urllib3
#from urllib3.contrib.socks import SOCKSProxyManager

import socks
#import socket


""" my header 
to Proxy IP:PORT through socks proxy

CONNECT https://google.com

"""

#sslproxy = '206.189.47.247:3128'
sslproxy = '192.168.0.10'
sslproxyport = '3128'
destination = 'google.com:443'

sock = socks.socksocket() # Same API as socket.socket in the standard lib
sock.set_proxy(socks.SOCKS5, "192.168.0.10", 9050)	# tor entrance

sock.connect(('google.com', 80))
sock.send('CONNECT HTTP/1.1')

print sock.recv(5000)


