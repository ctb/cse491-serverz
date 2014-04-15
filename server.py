#!/usr/bin/env python
import argparse
from app import make_app
import imageapp
import os
import quixote
from quixote.demo.altdemo import create_publisher
import random
import socket
from StringIO import StringIO
from sys import stderr
import time
from urlparse import urlparse
from wsgiref.validate import validator
import threading

def handle_connection(server_port, conn, port, app):
    print 'handling a connection'
    request = conn.recv(1)
    
    if not request:
        print 'Error, remote client closed connection without sending anything'
        return

    count = 0
    env = {}
    while request[-4:] != '\r\n\r\n':
         request += conn.recv(1)

    request, data = request.split('\r\n',1)
    headers = {}
    for line in data.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        headers[k.lower()] = v

    path = urlparse(request.split(' ', 3)[1])
    env['REQUEST_METHOD'] = 'GET'
    env['PATH_INFO'] = path[2]
    env['QUERY_STRING'] = path[4]
    env['CONTENT_TYPE'] = 'text/html'
    env['CONTENT_LENGTH'] = str(0)
    env['SCRIPT_NAME'] = ''
    env['SERVER_NAME'] = socket.getfqdn()
    env['SERVER_PORT'] = str(server_port)
    env['wsgi.version'] = (1, 0)
    env['wsgi.errors'] = stderr
    env['wsgi.multithread'] = False
    env['wsgi.multiprocess'] = False
    env['wsgi.run_once'] = False
    env['wsgi.url_scheme'] = 'http'
    env['HTTP_COOKIE'] = headers['cookie'] if 'cookie' in headers.keys() else ''

    body = ''
    if request.startswith('POST '):
        env['REQUEST_METHOD'] = 'POST'
        env['CONTENT_LENGTH'] = headers['content-length']
        env['CONTENT_TYPE'] = headers['content-type']
        while len(body) < int(headers['content-length']):
            body += conn.recv(1)

    def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

    env['wsgi.input'] = StringIO(body)
    result = app(env, start_response)
    for data in result:
        conn.send(data)
    conn.close()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action="store",
                              default=0,
                              dest='arg_port',
                              help="The port to use (optional)",
                              required=False,
                              type=int)

    results = parser.parse_args()
    return results.arg_port

def main():
    port = get_args()

    imageapp.setup()
    p = imageapp.create_publisher()
    wsgi_app = quixote.get_wsgi_app()
    s = socket.socket()
    host = socket.getfqdn()
    if port == 0:
        port = random.randint(8000, 9999)
    s.bind((host, port))
    
    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)
    s.listen(5)
    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        print 'Waiting for a connection'
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port

        # see: https://docs.python.org/2/library/threading.html#thread-objects
        t = threading.Thread(target=handle_connection,
                             args=(port, c, client_port, wsgi_app))
        t.start()

if __name__ == '__main__':
    main()

