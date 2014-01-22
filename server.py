# @comment   I Reviewed this, it works it both Firefox and Chrome. Good work!

#!/usr/bin/env python
import random
import socket
import time

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port, '\n'
        handle_connection(c)

def handle_connection(conn):
    request = conn.recv(1000)

    # Path is the second element in the first line of the request
    # separated by whitespace. (Between GET and HTTP/1.1)
    path = request.split('\r\n')[0].split(' ')[1]

    if path == '/':
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  '<h1>Links to other pages</h1>' + \
                  '<a href = /content>Content</a><br>' + \
                  '<a href = /file>File</a><br>' + \
                  '<a href = /image>Image</a>')
    elif path == '/content':
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  '<h1>Cam is great</h1>' + \
                  'This is some content.')
    elif path == '/file':
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  '<h1>They don\'t think it be like it is, but it do.</h1>' + \
                  'This some file.')
    elif path == '/image':
        conn.send('HTTP/1.0 200 OK\r\n' + \
                  'Content-type: text/html\r\n' + \
                  '\r\n' + \
                  '<h1>Wow. Such page. Very HTTP response</h1>' + \
                  'This is some image.')
    conn.close()

if __name__ == '__main__':
   main()
