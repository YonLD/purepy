import sys
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from http.server import SimpleHTTPRequestHandler, HTTPServer
from examples.bootstrap_cover.index import BootstrapCover
from examples.bootstrap_features.index import BootstrapFeatures
from examples.bootstrap_pricing.index import BootstrapPricing
from examples.event_counter.index import EventCounter
from pure.html import ul, li, a, div, h1

def ExamplesView():
    return (
        div(
            h1('Purepy Examples'),
            ul(
                li(
                    a('Bootstrap Cover').href('/bootstrap-cover')
                ),
                li(
                    a('Bootstrap Features').href('/bootstrap-features')
                ),
                li(
                    a('Bootstrap Pricing').href('/bootstrap-pricing')
                ),
                li(
                    a('Event Counter').href('/event-counter')
                )
            )
        )
    )

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            result = str(ExamplesView())
        elif self.path == '/bootstrap-cover':
            result = str(BootstrapCover())
        elif self.path == '/bootstrap-features':
            result = str(BootstrapFeatures())
        elif self.path == '/bootstrap-pricing':
            result = str(BootstrapPricing())
        elif self.path == '/event-counter':
            result = str(EventCounter())
        else:
            super().do_GET()
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(result.encode())

def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server on port {}...'.format(port))
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
