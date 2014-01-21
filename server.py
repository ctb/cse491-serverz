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

        # Ctrl+C KeyboardInterrupt error handler
        try:
            # Establish connection with client.
            c, (client_host, client_port) = s.accept()
            print 'Got connection from', client_host, client_port
##            print c.recv(1000)
            handle_connection(c)
        except (KeyboardInterrupt):
            print "\r\nEnding server.py ...\r\n"
            exit(0)
            



def handle_connection(conn):

    ## handle request data
    request_data = conn.recv(1000)
    request_type = request_data.splitlines()[0].rsplit(' ')[0] # prints the page requested (1st line, 1st word)
    page_request = request_data.splitlines()[0].rsplit(' ')[1] # prints the page requested (1st line, 2nd word)

    print request_type + ' ' + page_request

    ## initialize html_text
    html_text = str()

    ## set http_response
    ## don't send the http_response just yet, incase page doesn't exist
    http_response =  'HTTP/1.0 200 OK\r\n'
    content_type = 'Content-type: text/html\r\n'


    ## handle different types of HTML requests
    if request_type == "GET":
        ## serve HTML content
        if page_request == '/':
            ## cse.msu.edu:xxxx/
            html_text = '<h1>Hello, world.</h1>' + \
                        'This is MaxwellGBrown\'s Web server.' + \
                        '<ul>' + \
                        '<li><a href="/content">content</a></li>' + \
                        '<li><a href="/file">file</a></li>' + \
                        '<li><a href="/image">image</a></li>' + \
                        '</ul>'
            
        elif page_request == '/content':
            ## cse.msu.edu:xxx/content
            html_text = '<h1>Hello, world.</h1>' + \
                        'This is MaxwellGBrown\'s Web server.' + \
                        '<h2>Content</h2>'
            
        elif page_request == '/file':
            ## cse.msu.edu:xxx/file
            html_text = '<h1>Hello, world.</h1>' + \
                        'This is MaxwellGBrown\'s Web server.' + \
                        '<h2>File</h2>'
            
        elif page_request == '/image':
            ## cse.msu.edu:xxx/image
            html_text = '<h1>Hello, world.</h1>' + \
                        'This is MaxwellGBrown\'s Web server.' + \
                        '<h2>Image</h2>'

    elif request_type == "POST":
        ## POST request handler
        html_text = '<h1>Hello, world.</h1>' + \
                    'MaxwellGBrown\'s POST request HTML.'



    
    ## send http response and content
    conn.send(http_response)
    conn.send(content_type)
    conn.send('\r\n')
    conn.send(html_text)
    conn.close()




## Run main
if __name__ == '__main__':
    main()
