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
def handle_submit(para,conn):
    path = para.split('\r\n')[0].split(' ')[1]
    print path
    first_name = path.split('firstname=')[1].split('&lastname=')[0]
    last_name = path.split('firstname=')[1].split('&lastname=')[1]
    print first_name
    print last_name
    conn.send('Hello Mr. %s %s' % (first_name, last_name))

def handle_connection(conn):
        receive = conn.recv(1000)
        print receive       
        command = receive.split('\r\n')[0].split(' ')[0:2]
        method = command[0]
        req = command[1].split('?')[0]
        print req
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n')
        conn.send('\r\n')
        if method == 'POST':
            if req == '/submit':
                handle_submit(para,conn)
            else:
                conn.send('<h1>Hello, world.</h1>')
                conn.sned('')
        elif method == 'GET':
            if req == '/':
                handle_deafult(conn)
            if req == '/content':
                handle_content(conn)
            if req == '/file':
                handle_file(conn)
            if req == '/image':
                handle_image(conn)
            if req == '/submit':
                handle_submit(receive,conn)
        conn.close()

def handle_deafult(conn):
    conn.send("<h1>Hello, world.</h1>")
    conn.send("This is fakestuff's Web server.")
    conn.send("There is a list of 'website' available.<br>")
    conn.send('<a href= /content>Content</a><br>')
    conn.send('<a href= /file>File</a><br>')
    conn.send('<a href= /image>Image</a><br>')
    conn.send("<form action='/submit' method='GET'>")
    conn.send("<input type='text' name='firstname'>")
    conn.send("<input type='text' name='lastname'>")
    conn.send("<input type='submit' value='Submit'></form>")
def handle_content(conn):
    conn.send("This is the content you want to see.")

def handle_file(conn):
    conn.send("This is the file you want to see.")

def handle_image(conn):
    conn.send("This is the image you want to see.")

if __name__ == '__main__':
    main()
