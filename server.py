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

  first_line_of_request_split = request.split('\r\n')[0].split(' ')

  # Path is the second element in the first line of the request
  # separated by whitespace. (Between GET and HTTP/1.1). GET/POST is first.
  http_method = first_line_of_request_split[0]
	
  try:
    path = first_line_of_request_split[1]
  except:
    path = "/404"

  if http_method == 'POST':
      conn.send('HTTP/1.0 200 OK\r\n' + \
                    'Content-type: text/html\r\n' + \
                    '\r\n' + \
                    'Post? Post! Zomg!')
  else:
      if path == '/':
          handle_index(conn)
      elif path == '/content':
          handle_content(conn)
      elif path == '/file':
          handle_filepath(conn)
      elif path == '/image':
          handle_image(conn)
      elif path == '/submit':
          handle_submit(conn)
      else:
          notfound(conn)
      conn.close()

def handle_index(conn):
  ''' Handle a connection given path / '''
  conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            "<form action='/submit' method='GET'>\n" + \
            "<p>first name: <input type='text' name='firstname'></p>\n" + \
            "<p>last name: <input type='text' name='lastname'></p>\n" + \
            "<input type='submit' value='Submit'>\n\n" + \
            "</form>")

def handle_submit(conn):
  ''' Handle a connection given path /submit '''
  conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            "hi\n")

def handle_content(conn):
  ''' Handle a connection given path /content '''
  conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            '<h1>Cam is great</h1>' + \
            'This is some content.')

def handle_filepath(conn):
  ''' Handle a connection given path /file '''
  conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            '<h1>They don\'t think it be like it is, but it do.</h1>' + \
            'This some file.')

def handle_image(conn):
  ''' Handle a connection given path /image '''
  conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            '<h1>Wow. Such page. Very HTTP response</h1>' + \
            'This is some image.')

def notfound(conn):
  conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            'Oopsies, this isn\'t the page you want. :(')

if __name__ == '__main__':
   main()
