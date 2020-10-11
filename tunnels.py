#!/usr/bin/env python

# proxy list
# https://www.sslproxies.org

import argparse
import socket
import socks
import sys
import time

def recv_timeout(the_socket, timeout):
    the_socket.setblocking(0)
    total_data = []
    data = '' 
    begin = time.time()

    while 1:
        #if you got some data, then break after wait sec
        if total_data and time.time() - begin > timeout:
            break
        #if you got no data at all, wait a little longer
        elif time.time()-begin>timeout*2:
            break

        try:
            data=the_socket.recv(8192)
            if data:
                total_data.append(data)
                begin=time.time()
            else:
                time.sleep(0.1)
        except:
            pass

    return ''.join(total_data)


def create_listener(listenip, listenport, socksconn, timeout):
    """
    args:     listenip - interface to listen on
              listenport - port to listen on
              socksconn - socks.socksocket object with an established connection
    """
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((listenip, listenport))
        s.listen(10)            # listen with 10 queued connections
    except socket.error as msg:
        s.close()
        s = None
        print(msg)
        sys.exit()

    try:
        conn, addr = s.accept()
        print("Connection from address: " + str(addr))
        while True:
            req = recv_timeout(conn, timeout)	# receive data from the client
            socksconn.send(req)		# send the data through the socks connection to the destination
            data = recv_timeout(socksconn, timeout)
            conn.send(data)

    except KeyboardInterrupt:
        print("CTRL-C received. Quitting.")
        conn.close()
        s.close()
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
    timeout = args.timeout
    
    sock = socks.socksocket() 
    sock.set_proxy(socks.SOCKS5, socksproxy, socksport)    # tor entrance
    
    sock.connect((sslproxy, sslproxyport))    # connect to the proxy after exiting tor
    # send CONNECT request to the proxy
    sock.send('CONNECT ' + destination + ':' + str(destinationport) + ' HTTP/1.1\r\n\r\n')
    
    print(sock.recv(1024))
    create_listener(listenip, listenport, sock, timeout)
    

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
    parser.add_argument('--timeout', '-t', help='Timeout value for sockets to listen for receiving data', default=.01)
    args = parser.parse_args()
    create_tunnel(args)


