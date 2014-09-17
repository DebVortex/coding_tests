#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json
from random import randint
from urlparse import urlparse, parse_qs

PORT_NUMBER = 8000
MANIFEST_ID = randint(0, 100000)


class HttpRequestHandler(BaseHTTPRequestHandler, object):

    def __init__(self, *args, **kwargs):
        self.routing = {
            '/': self.index,
            '/get_data': self.get_data,
            '/manifest.appcache': self.manifest
        }
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def _return(self, content, content_type='text/html', status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', self.content_type)
        self.end_headers()
        self.wfile.write(content)

    def _return_static_file(self):
        try:
            with open(self.parsed_path.path[1:]) as static_file:
                self._return(static_file.read(), content_type=self.content_type)
        except IOError:
            with open('templates/404.html') as not_found_template:
                self._return(not_found_template.read(), status_code=404)

    def do_GET(self):
        self.parsed_path = urlparse(self.path)
        self.content_type = self.get_content_type()
        self.handler = self.get_handler()
        self.handler()

    def get_handler(self):
        return self.routing.get(self.parsed_path.path, self._return_static_file)

    def get_content_type(self):
        content_type = 'text/html'
        if 'css' in self.parsed_path.path:
            content_type = 'text/css'
        elif 'js' in self.parsed_path.path:
            content_type = 'application/javascript'
        return content_type

    def index(self):
        with open('templates/index.html') as index_template:
            self._return(index_template.read())

    def get_data(self):
        query = parse_qs(self.parsed_path.query)
        return_value = [1, 2, 3]
        if 'test_data_values' in query:
            return_value = [1, 2, 3, 4, 5]
        json_data = {'test_data_values': return_value}
        self._return(json.dumps(json_data), content_type='application/json')

    def manifest(self):
        with open('static/manifest') as manifest_file:
            manifest_template = manifest_file.read()
            manifest_content = manifest_template.format(MANIFEST_ID)
            self._return(manifest_content, content_type='text/cache-manifest')


if __name__ == '__main__':
    try:
        server = HTTPServer(('', PORT_NUMBER), HttpRequestHandler)
        print('Started httpserver on port {}'.format(PORT_NUMBER))
        server.serve_forever()
    except KeyboardInterrupt:
        print ' received, shutting down the web server'
        server.socket.close()
