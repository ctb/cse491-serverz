import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
##    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
##    expected_return = 'HTTP/1.0 200 OK\r\n' + \
##                      'Content-type: text/html\r\n' + \
##                      '\r\n' + \
##                      '<h1>Hello, world.</h1>' + \
##                      'This is MaxwellGBrown\'s Web server.' + \

    ## Do a handle_connection for all 4 pages                
    for page in ['/','/content','/file','/image']:
        conn = FakeConnection("GET "+page+" HTTP/1.0\r\n\r\n")

        ## standardized info per page
        expected_return = 'HTTP/1.0 200 OK\r\n' + \
                          'Content-type: text/html\r\n' + \
                          '\r\n' + \
                          '<h1>Hello, world.</h1>' + \
                          'This is MaxwellGBrown\'s Web server.'

        #Add content to check for per page
        if page == '/':
            expected_return = expected_return + \
                              '<ul>' + \
                              '<li><a href="/content">content</a></li>' + \
                              '<li><a href="/file">file</a></li>' + \
                              '<li><a href="/image">image</a></li>' + \
                              '</ul>'
        elif page == '/content':
            expected_return = expected_return + \
                              '<h2>Content</h2>'

        elif page == '/file':
            expected_return = expected_return + \
                              '<h2>File</h2>'

        elif page == '/image':
            expected_return = expected_return + \
                              '<h2>Image</h2>'
                              
                          
    
        server.handle_connection(conn)

        assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_POST():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                          'Content-type: text/html\r\n' + \
                          '\r\n' + \
                          '<h1>Hello, world.</h1>' + \
                          'MaxwellGBrown\'s POST request HTML.'
    
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    
