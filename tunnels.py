#!/usr/bin/env python

# proxy list
# https://www.sslproxies.org

import socks
import argparse


""" my header 
to Proxy IP:PORT through socks proxy

CONNECT https://google.com

"""

def create_tunnel(args):
    socksproxy = args.socks_proxy
    socksport = int(args.socks_port)
    sslproxy = args.ssl_proxy
    sslproxyport = int(args.ssl_proxy_port)
    destination = args.destination_ip
    destinationport = int(args.destination_port)
    
    sock = socks.socksocket() # Same API as socket.socket in the standard lib
    sock.set_proxy(socks.SOCKS5, socksproxy, socksport)	# tor entrance
    
    sock.connect((sslproxy, sslproxyport))
    #sock.send('GET / HTTP/1.1\r\nHost: google.com\r\n\r\n')
    sock.send('CONNECT ' + destination + ':' + str(destinationport) + ' HTTP/1.1\r\n\r\n')
    
    print sock.recv(5000)
    
    sock.send('GET / HTTP/1.1\r\nHost: ' + destination + '\r\n\r\n')
    
    print sock.recv(5000)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--socks-proxy', '-s', help='IP of the SOCKS proxy (first hop)', required=True)
    parser.add_argument('--socks-port', '-x', help='Port of the SOCKS proxy (first hop)', required=True)
    parser.add_argument('--ssl-proxy', '-l', help='IP of the last hop (exit proxy)', required=True)
    parser.add_argument('--ssl-proxy-port', '-r', help='Port of the ssl proxy', required=True)
    parser.add_argument('--destination-ip', '-d', help='IP of the ultimate destination of the tunnel', required=True)
    parser.add_argument('--destination-port', '-p', help='Port of the destination of the tunnel', required=True)
    args = parser.parse_args()
    create_tunnel(args)
