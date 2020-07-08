import posixpath
import urllib
from http import HTTPStatus
from jinja2 import Environment, BaseLoader
import os

try:
    from http.server import SimpleHTTPRequestHandler
except ImportError:
    from SimpleHTTPServer import SimpleHTTPRequestHandler

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):

        if self.path=='/ping':
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "application/json")
            msg = '{"status": "ok"}'
            self.send_header("Content-Length", len(msg))
            self.end_headers()
            self.wfile.write(msg.encode())
            return

        if self.web_auth:
            # ensure connection is authorized, this seems to apply to list_directory() as well
            self.auth_connection()

        strip_path = self.do_strip_base_url(self.path)
        self.logger.info("LOG: {},{}".format(strip_path,self.path))
        if not strip_path:
            self.send_error(404, "Path {} not found".format(self.path))

        if strip_path=='start':
            with open("index.html", 'r') as f:
                content = f.read()
                rtemplate = Environment(loader=BaseLoader).from_string(content)
                data = rtemplate.render(env=os.environ)
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-Length", len(data))
                self.end_headers()
                self.wfile.write(data.encode())
                return

        if self.only_upgrade:
            self.send_error(405, "Method Not Allowed")
        else:
            SimpleHTTPRequestHandler.do_GET(self)

    def do_strip_base_url(self, path):

        base_url = os.environ.get('BASE_URL','')
        if path==base_url:
            return '/'

        if self.path.startswith(base_url+'/'):
            return self.path[len(base_url)+1:]
        
            
    def list_directory(self, path):
        if self.file_only:
            self.send_error(404, "No such file")
        else:
            return SimpleHTTPRequestHandler.list_directory(self, path)


    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        path = self.do_strip_base_url(path)
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path
