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
torproxy = '192.168.0.10'
torport = 9050
sslproxy = '64.235.46.37'				# last hop proxy IP
sslproxyport = 8080						# last hop proxy port number
destination = 'google.com'
destinationport = '80'

sock = socks.socksocket() # Same API as socket.socket in the standard lib
sock.set_proxy(socks.SOCKS5, torproxy, torport)	# tor entrance

sock.connect((sslproxy, sslproxyport))
#sock.send('GET / HTTP/1.1\r\nHost: google.com\r\n\r\n')
sock.send('CONNECT ' + destination + ':' + str(destinationport) + ' HTTP/1.1\r\n\r\n')

print sock.recv(5000)

sock.send('GET / HTTP/1.1\r\nHost: ' + destination + '\r\n\r\n')

print sock.recv(5000)


