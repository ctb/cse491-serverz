#!/usr/bin/env python
import random
import socket
import time

s = socket.socket()         # Create a socket object
host = socket.getfqdn() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

http_response =  'HTTP/1.0 200 OK \r\n'
content_type = 'Content-Type:text/html \r\n'
html_text = '<h1>Hello World</h1> this is MaxwellGBrown\'s Web server.'

print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)                 # Now wait for client connection.

print 'Entering infinite loop; hit CTRL-C to exit'
while True:
    # Establish connection with client.    
    c, (client_host, client_port) = s.accept()
    print c.recv(1000)
    print 'Got connection from', client_host, client_port
    c.send(http_response)
    c.send(content_type)
    c.send('\r\n')
    c.send(html_text)
# @You could move this string into a veriable during initialization
#  and just send the text string
    c.close()
