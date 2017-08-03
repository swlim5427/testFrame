# coding=utf-8
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import io
import urllib
from commonfunc import *
import json


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        datas = self.rfile.read(int(self.headers['content-length']))
        datas = urllib.unquote(datas).decode("utf-8", 'ignore')
        self.action(datas)

    def do_GET(self):

        url = urllib.unquote(self.path)

        if url == "/favicon.ico":
            self.response_error()

        mpath, margs = urllib.splitquery(url)
        self.action(margs)

    def action(self, datas):
        try:
            datas = self.get_param(datas)
            param = json.loads(datas)

            enc = "UTF-8"
            datas = datas.encode(enc)

            f = io.BytesIO()
            f.write(datas)
            f.seek(0)

            t = public_methods.create_threading(param)
            t.start()

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()


        except Exception as e:
            print e
            self.response_error()

    def get_param(self, params):

        try:
            if len(params) == 0:
                return
            else:
                if "+" in params:
                    p = params.replace("+", "")
                    param = p.split('=')[1]
                else:
                    param = params.split('=')[1]
                return param

        except Exception as e:
            print e
            self.response_error()

    def response_error(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return


class CustomHTTPServer(HTTPServer):
    def __init__(self, host, port):
        HTTPServer.__init__(self, (host, port), CustomHTTPRequestHandler)

if __name__ == '__main__':

    public_methods.init_table()
    server = CustomHTTPServer('172.21.5.148', 9989)
    print "service start"

    server.serve_forever()
