#!/usr/bin/env python
import random
import socket
import time

def main(socketmodule=None):
    if socketmodule is None:
        socketmodule = socket
        
    s = socketmodule.socket()         # Create a socket object
    host = socketmodule.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)

def handle_connection(c):
    request = c.recv(1000)

    if not request:
        print 'error, remote client closed connection without sending anything'
        return

    if request.startswith('POST'):
        c.send('HTTP/1.0 200 OK\r\n\r\nhello, world\n')
        c.close()
        return
    else:                               # a GET, assume
        c.send('HTTP/1.0 200 OK\r\n')
        c.send('Content-type: text/html\r\n')
        c.send('\r\n')
        c.send('<h1>Hello, world.</h1>')
        c.send('This is ctb\'s Web server.')
        c.close()

if __name__ == '__main__':
    main()
    
