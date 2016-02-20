"""This module provides HTTP interface to get monitoring data.
"""

import SimpleHTTPServer
import SocketServer
from threading import Thread

# Nasty global variable.
# Hope this is temporarily until I find out how to inject it into
# RequestHandler.
monitoring_info = None


class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """HTTP request handler.
    """

    def do_GET(self):
        """Handles '/monitoring_info' request.
        """
        if self.path != '/monitoring_info':
            self.send_error(404)
            return

        self.send_response(200)

        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write(monitoring_info.to_json())


class Server(object):
    """HTTP server to get monitoring info.
    """
    def __init__(self, port, service_info):
        """
        This constructor has a side effect: it sets global monitoring
        information object. This object is used in HTTP RequestHandler.  This is
        a hack and must be solved. For know, I don't know how.

        Args:
            port (int): HTTP server port.
            service_info (info.ServiceInfo): service information object.
        """
        global monitoring_info
        monitoring_info = service_info

        self.__server = SocketServer.TCPServer(('', port), RequestHandler)

    def start(self):
        """Starts listening for HTTP requests.
        """
        self.__server.serve_forever()

    def start_async(self):
        """Asynchrounously starts HTTP server.
        """
        server_thread = Thread(target=self.start)
        server_thread.start()
