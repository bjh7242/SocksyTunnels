#!/usr/bin/env python

# proxy list
# https://www.sslproxies.org

import argparse
import socket
import socks
import sys


def create_listener(listenip, listenport, socksconn):
    """
    args:     listenip - interface to listen on
              listenport - port to listen on
              socksconn - socks.socksocket object with an established connection
    """
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((listenip, listenport))
        s.listen(1)            # listen with 1 queued connection
    except socket.error as msg:
        s.close()
        s = None
        print msg
        sys.exit()

    while True:
        response = ""
        try:
            conn, addr = s.accept()
            print "Connection from address: " + str(addr)
            req = conn.recv(1024)
            if not req:
                break
            print req
            socksconn.send(req)		# send the data through the socks connection
            while True:
                data = socksconn.recv(1024)
                if not data:
                    break
                conn.send(data)

        except KeyboardInterrupt:
            print "CTRL-C received. Quitting."
            break
    sys.exit()
    

def create_tunnel(args):
    socksproxy = args.socks_proxy
    socksport = int(args.socks_port)
    sslproxy = args.ssl_proxy
    sslproxyport = int(args.ssl_proxy_port)
    destination = args.destination_ip
    destinationport = int(args.destination_port)
    listenport = int(args.listen_port)
    listenip = args.listen_ip
    
    sock = socks.socksocket() 
    sock.set_proxy(socks.SOCKS5, socksproxy, socksport)    # tor entrance
    
    sock.connect((sslproxy, sslproxyport))    # connect to the proxy after exiting tor
    # send CONNECT request to the proxy
    sock.send('CONNECT ' + destination + ':' + str(destinationport) + ' HTTP/1.1\r\n\r\n')
    
    print sock.recv(1024)
    create_listener(listenip, listenport, sock)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--socks-proxy', '-s', help='IP of the SOCKS proxy (first hop)', required=True)
    parser.add_argument('--socks-port', '-x', help='Port of the SOCKS proxy (first hop)', required=True)
    parser.add_argument('--ssl-proxy', '-o', help='IP of the last hop (exit proxy)', required=True)
    parser.add_argument('--ssl-proxy-port', '-r', help='Port of the ssl proxy', required=True)
    parser.add_argument('--destination-ip', '-d', help='IP of the ultimate destination of the tunnel', required=True)
    parser.add_argument('--destination-port', '-p', help='Port of the destination of the tunnel', required=True)
    parser.add_argument('--listen-port', '-l', help='Port to listen on on the computer you are running this on. This will be forwarded to the destination port', required=True)
    parser.add_argument('--listen-ip', '-n', help='Interface to listen on (default=0.0.0.0)', default='0.0.0.0', required=False)
    args = parser.parse_args()
    create_tunnel(args)


