from wsgiref.simple_server import make_server
from http import cookies

# Every WSGI application must have an application object - a callable
# object that accepts two arguments. For that purpose, we're going to
# use a function (note that you're not limited to a function, you can
# use a class for example). The first argument passed to the function
# is a dictionary containing CGI-style envrironment variables and the
# second variable is the callable object (see PEP 333).
def hello_world_app(environ, start_response):
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'text/plain')] # HTTP Headers
    start_response(status, headers)

    # The returned object is going to be printed
    return [b"Hello Worlddd"]

#httpd = make_server('', 8000, hello_world_app)
#print("Serving on port 8000...")

# Serve until process is killed
#httpd.serve_forever()

#httpd.handle_request()


class Request:

    def __init__(self):
        self.cookie = cookies.SimpleCookie()

    def getCookie(self, key):
        return self.cookie[key]

    def setCookie(self, key, value):
        self.cookie[key] = value

    def setPathInfo(self, pathInfo):
        self.pathInfo = pathInfo

    def setPostData(self, data):
        self.postData = data


    def createFromUwsgiEnv(environ):

        request = Request()
        request.setPathInfo(environ['PATH_INFO'])
        request.setRequestMethod(environ['REQUEST_METHOD'])
        request.setQueryString(environ['QUERY_STRING'])

        if environ['REQUEST_METHOD'] == 'POST':
            length = int(environ['CONTENT_LENGTH'])
            raw = environ['wsgi.input'].read(length)
            raw = str(raw, encoding='utf8')
            data = urllib.parse.parse_qs(raw, encoding='utf-8')
            request.setPostData(data)


class Response:

    def __init__(self):
        self.cookie = cookies.SimpleCookie()

    def setCookie(self, key, value):
        self.cookie[key] = value

    def getCookie(self, key):
        return self.cookie[key]

    def getCookies(self):
        return self.cookie

    def redirect(self, url):
        self.redirect = url

