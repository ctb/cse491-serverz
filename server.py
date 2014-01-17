#!/usr/bin/env python
import random
import socket
import time

def handle_get(conn, path):
    if path == '/':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html>\n\t<body>\n\t\t')
        conn.send('<h1>Hello, world.</h1>\n\t\t')
        conn.send("This is brtaylor92's Web server.\n\t")
    elif path == '/content':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html>\n\t<body>\n\t\t')
        conn.send('<h1>Content Page</h1>\n\t\t')
        conn.send('Content goes here, once there is any :)\n\t')
        conn.close()
    elif path == '/file':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html>\n\t<body>\n\t\t')
        conn.send('<h1>File Page</h1>\n\t\t')
        conn.send('Files go here, once there are any :)\n\t')
    elif path == '/image':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html>\n\t<body>\n\t\t')
        conn.send('<h1>Image Page</h1>\n\t\t')
        conn.send('Images go here, once there are any :)\n\t')
    else:
        # Page we don't have...
        conn.send('HTTP/1.0 404 Not Found\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html>\n\t<body>\n\t\t')
        conn.send('<h1>Oops! Something went wrong...</h1>\n\t\t')
        conn.send('We couldn\'t find that page\n\t')
    # And we're done
    conn.send('</body>\n</html>')

def handle_post(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html>\n\t<body>\n\t\t')
    conn.send('<h1>Hello World!</h1>\n\t\t')
    conn.send('This is a POST page.\n\t')
    conn.send('</body>\n</html>')

def handle_connection(conn):
    req = conn.recv(1000)
    check = req.split('\r\n')[0]
    if check == 'GET':
        try:
            path = req.split('\r\n')[0].split(' ')[1]
            handle_get(conn, path)
        except IndexError:
            handle_get(conn, '/404')
    elif check == 'POST':
        handle_post(conn)
    # Done here
    conn.close()

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
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)
        

# boilerplate
if __name__ == "__main__":
    main()