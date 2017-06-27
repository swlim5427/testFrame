# coding=utf-8
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import io
import urllib
from commonFunc import *
import json


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    #----------处理post请求
    def do_POST(self):

        datas = self.rfile.read(int(self.headers['content-length']))
        datas = urllib.unquote(datas).decode("utf-8",'ignore')
        self.action(datas)

    # ----------处理get请求
    def do_GET(self):

        url = urllib.unquote(self.path)

        if url == "/favicon.ico":
            self.responseError()

        mpath,margs=urllib.splitquery(url)
        self.action(margs)

    # ----------处理post请求
    def action(self,datas):
        try:
            datas = self.getParam(datas)
            param = json.loads(datas)

            enc = "UTF-8"
            datas = datas.encode(enc)

            f = io.BytesIO()
            f.write(datas)
            f.seek(0)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            test_frame_distribute.testFrameDistribute(param)
        except:
            self.responseError()

    # ----------提取参数
    def getParam(self,params):
        try:
            if len(params)==0:
                return
            else:
                param = params.split('=')[1]
                return param
        except:
            self.responseError()

    def responseError(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return

class CustomHTTPServer(HTTPServer):
    def __init__(self, host, port):
        HTTPServer.__init__(self, (host, port), CustomHTTPRequestHandler)

def main():
    server = CustomHTTPServer('172.21.10.227', 9989)
    server.serve_forever()

if __name__ == '__main__':
    main()