import BaseHTTPServer
import datetime
import sys
import os

SERVER = '0.0.0.0'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 2333
LOG_PATH = 'reqlog.txt'


class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if '.png' in self.path:
            print self.path
            fname = '1.png'
        elif '.jpg' in self.path:
            fname = '1.jpg'
        elif '.gif' in self.path:
            fname = '1.gif'
        elif '.html' in self.path:
            fname = 'index.html'
        elif 'clear' in self.path:
            os.remove(LOG_PATH)
            self.send_response(200)
            self.end_headers()
            self.wfile.write('ok')
            return
        else:
            self.send_response(200)
            self.end_headers()
            try:
                self.wfile.write(open(LOG_PATH, 'r').read())
            except IOError:
                print '[*]Create logfile: ' + LOG_PATH
            return

        message_parts = ['<br>===== [%s] %s =====' % (self.path, datetime.datetime.today())]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s: %s' % (name, value.strip()))
        message = '<br>'.join(message_parts) + '<br>'

        with open(LOG_PATH, 'a') as f:
            f.write(message)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(open(fname, 'rb').read())


print '[*]Starting server at %s:%d' % (SERVER, PORT)
server = BaseHTTPServer.HTTPServer((SERVER, PORT), WebRequestHandler)
server.serve_forever()
