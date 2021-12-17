from http.server import BaseHTTPRequestHandler, HTTPServer
import time, json, re, random
from urllib.parse import unquote

def kiwiParseReference(ref):
    m = re.search(r'\{ref(.+)@(.+)\}', ref)
    if m is None: return None
    return (m.group(1), m.group(2))

def kiwiSave():
    with open('kiwidb.db', 'w') as f:
        json.dump(loaded, f)

config = None
with open('kiwidb.config.json') as f:
    config = json.load(f)

loaded = {}
with open('kiwidb.db') as f:
    loaded = json.load(f)

class KiwiServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server_version = "KiwiDB/1.0"

        path = unquote(self.path[1:])
        if path.startswith('@'):
            if path[1:] in loaded:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(loaded[path[1:]]).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
            return
        ref = kiwiParseReference(path)
        if ref is None:
            self.send_response(400)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return
        
        if ref[1] in loaded and ref[0] in loaded[ref[1]]:
            data = loaded[ref[1]][ref[0]]
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
    
    def do_DELETE(self):
        self.server_version = "KiwiDB/1.0"
        
        path = unquote(self.path[1:])
        ref = kiwiParseReference(path)
        if ref is None:
            self.send_response(400)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return
        
        if ref[1] in loaded and ref[0] in loaded[ref[1]]:
            del loaded[ref[1]][ref[0]]
            kiwiSave()
            self.send_response(204)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
    
    def do_PUT(self):
        self.server_version = "KiwiDB/1.0"
        
        path = unquote(self.path[1:])
        ref = kiwiParseReference(path)
        if path.startswith('@'):
            if path[1:] not in loaded:
                loaded[path[1:]] = {}
            
            rand = ''.join(random.choice('0123456789abcdef') for n in range(32))
            ref = (rand, path[1:])
        if ref is None:
            self.send_response(400)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return
        
        if ref[1] in loaded and ref[0] in loaded[ref[1]]:
            self.send_response(409)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
        else:
            length = int(self.headers.get('content-length'))
            data = self.rfile.read(length)

            loaded[ref[1]][ref[0]] = json.loads(data)
            kiwiSave()
            self.send_response(201)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Location", config['redirect'] + "{ref" + ref[0] + path + "}")
            self.end_headers()
    
    def do_PATCH(self):
        self.server_version = "KiwiDB/1.0"
        
        path = unquote(self.path[1:])
        ref = kiwiParseReference(path)
        if ref is None:
            self.send_response(400)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return
        
        if ref[1] in loaded and ref[0] in loaded[ref[1]]:
            length = int(self.headers.get('content-length'))
            data = self.rfile.read(length)

            incoming = json.loads(data)
            outgoing = { **loaded[ref[1]][ref[0]], **incoming }
            loaded[ref[1]][ref[0]] = outgoing

            kiwiSave()
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

if __name__ == "__main__":        
    webServer = HTTPServer((config['host'], config['port']), KiwiServer)
    print(f">> KiwiDB HTTP server started at http://localhost:{config['port']}/")

    try:
        webServer.serve_forever()
    except Exception as e:
        print(e)
        print(">> KiwiDB stopping")

    webServer.server_close()
    kiwiSave()
    print(">> KiwiDB stopped")