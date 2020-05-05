from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler, CGIHTTPRequestHandler, BaseHTTPRequestHandler
from urllib.parse import urlparse
from io import BytesIO
import pdb


class TaroHttpHandler(SimpleHTTPRequestHandler):


    def parse_url(self, path):
        query = urlparse(path).query
        path_component = urlparse(path).path
        query_components = {}

        try:
            query_components = dict(qc.split("=") for qc in query.split("&"))
        except ValueError as e:
            pass # Do nothing

        return path_component, query_components

    def do_GET(self):
        path_component, query_components = self.parse_url(self.path)

        if path_component == '/taro/three-cards/':
            self.path = "{}/{}".format(path_component, 'index.html')

        if path_component == '/taro/three-cards/comments/':
            self.path = "{}/{}".format(path_component, 'comments.json')

        if path_component == '/taro/three-cards/values/':
            past = query_components.get('past')
            present = query_components.get('present')
            future = query_components.get('future')
            try:
                assert (past and present and future)
            except AssertionError as e:
                self.send_response(code=400, message='Necessary params: "past", "present", "future".'
                                                     'Received: past={}, present={}, future={}'.format(past, present,
                                                                                                       future))
                self.end_headers()

            try:
                DECK_SIZE = 77
                assert ((int(past) <= DECK_SIZE) and (int(present) <= DECK_SIZE) and (int(future) <= DECK_SIZE))
            except AssertionError as e:
                self.send_response(code=400, message='A card index should be less or equal to 77.'
                                                     'Received: past={}, present={}, future={}'.format(past, present,
                                                                                                       future))
                self.end_headers()

            try:
                assert (query_components.get('past') and query_components.get('present') and query_components.get('future'))
            except AssertionError as e:
                self.send_response(code=400, message='Necessary params: "past", "present", "future".'
                                                     'Received: past={}, present={}, future={}'.format(
                    query_components.get('past'),
                    query_components.get('present'),
                    query_components.get('future')))
                self.end_headers()

            self.path = "{}/{}".format(path_component, 'values.json')

        if path_component == '/taro/three-cards/get-rating/':
            self.path = "{}/{}".format(path_component, 'rating.json')

        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        path_component, _ = self.parse_url(self.path)
        if path_component == '/taro/three-cards/set-rating/':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            self.send_header(keyword="Content-Type", value="application/json")
            self.send_response(200) # Send response is printed.
            self.end_headers()
            response = BytesIO()
            response.write(b'{Rating: 1}')
            response.write(body)
            pdb.set_trace()
            self.wfile.write(response.getvalue())

def run(server_class=HTTPServer, handler_class=TaroHttpHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
