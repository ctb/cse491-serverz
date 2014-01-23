#!/usr/bin/env python
import random
import socket
import time

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.
    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        c, (client_host, client_port) = s.accept()
        
        print 'Got connection from', client_host, client_port
        #Establish connection with client.
       # url = host + ':' +str(port)
        handle_connection(c)

def handle_connection(conn):
        command = conn.recv(1000).split('\r\n')[0].split(' ')[0:2]
        method = command[0]
        req = command[1]
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n')
        conn.send('\r\n')
        if method == 'POST':
           conn.send('<h1>Hello, world.</h1>')
        elif method == 'GET':
           if req == '/':
               conn.send("<h1>Hello, world.</h1>")
               conn.send("This is fakestuff's Web server.")
               conn.send("There is a list of 'website' available.<br>")
               conn.send('<a href= /content>Content</a><br>')
               conn.send('<a href= /file>File</a><br>')
               conn.send('<a href= /image>Image</a><br>')
           if req == '/content':
               conn.send("This is the content you want to see.")
           if req == '/file':
               conn.send("There will be some files in future.")
           if req == '/image':
               conn.send("Only most smart guy could see the image. LOL")  
        conn.close()

if __name__ == '__main__':
    main()
