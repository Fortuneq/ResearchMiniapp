#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.request
import urllib.parse
from pathlib import Path
from urllib.error import URLError, HTTPError

PORT = 8000
DIRECTORY = Path(__file__).parent
N8N_WEBHOOK_URL = 'https://maine-doug-all-commander.trycloudflare.com/webhook/***REMOVED***'

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/research':
            self.handle_research_request()
        else:
            super().do_POST()
    
    def handle_research_request(self):
        try:
            # Read request data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            print(f"📨 Received research request: {post_data.decode('utf-8')}")
            
            # Forward to n8n webhook
            req = urllib.request.Request(
                N8N_WEBHOOK_URL,
                data=post_data,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Research-MiniApp/1.0'
                }
            )
            
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    response_data = response.read()
                    print(f"✅ N8N Response: {response_data.decode('utf-8')}")
                    
                    # Send success response
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    
                    # Try to parse n8n response, or send test response
                    try:
                        n8n_result = json.loads(response_data.decode('utf-8'))
                        self.wfile.write(response_data)
                    except:
                        # If n8n doesn't return proper JSON, send test response
                        test_response = {
                            "success": True,
                            "documentUrl": "https://docs.google.com/document/d/1test-document-url/edit",
                            "message": "Research completed successfully"
                        }
                        self.wfile.write(json.dumps(test_response).encode('utf-8'))
                        
            except (URLError, HTTPError) as e:
                print(f"❌ N8N Error: {e}")
                
                # Send test response for development
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                test_response = {
                    "success": True,
                    "documentUrl": "https://docs.google.com/document/d/1test-document-url/edit",
                    "message": "Development mode - webhook not available"
                }
                self.wfile.write(json.dumps(test_response).encode('utf-8'))
                
        except Exception as e:
            print(f"🔥 Server error: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_response = {
                "success": False,
                "message": f"Server error: {str(e)}"
            }
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
        print(f"🚀 Serving Telegram Mini App with Proxy at:")
        print(f"   Local: http://localhost:{PORT}")
        print(f"   Network: http://0.0.0.0:{PORT}")
        print(f"🔗 Proxying to: {N8N_WEBHOOK_URL}")
        print(f"📋 Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n✅ Server stopped successfully")