# this script can't directly redirect to vue dev server html, it can only proxy ./dist files when you use 'python -m http.server' to serve them

# author: gemini 2.5 flash
import http.server
import http.client
import socketserver
import urllib.parse
import sys

# Configuration
PROXY_PORT = 3000 #the gateway port
TARGET_HOST = '127.0.0.1'
TARGET_PORT = 8000 #one of the service port
TARGET_URL = "http://{}:{}".format(TARGET_HOST, TARGET_PORT) # Changed from f-string

def get_http_content(url):
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]
        conn = http.client.HTTPSConnection(url.split('/')[0])
    else:
        conn = http.client.HTTPConnection(url.split('/')[0])

    path = '/' + '/'.join(url.split('/')[1:])

    try:
        conn.request("GET", path)
        response = conn.getresponse()
        if response.status == 200:
            return response.read().decode('utf-8')
        else:
            return "Error: " + response.status + " " + response.reason
    except Exception as e:
        return "Error: " + str(e)
    finally:
        conn.close()

class CustomProxyHandler(http.server.SimpleHTTPRequestHandler):
    # This dictionary maps the client's request headers to the headers
    # that should be forwarded to the target server.
    # It removes headers that might cause issues or are not relevant for forwarding.
    _exclude_request_headers = {
        'host', 'connection', 'proxy-connection', 'keep-alive',
        'proxy-authenticate', 'proxy-authorization', 'te', 'trailers',
        'transfer-encoding', 'upgrade'
    }

    def _send_json_response(self, status_code, data):
        """Helper to send a JSON response."""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(data.encode('utf-8'))

    def do_GET(self):
        self._handle_request('GET')

    def do_POST(self):
        self._handle_request('POST')

    def do_PUT(self):
        self._handle_request('PUT')

    def do_DELETE(self):
        self._handle_request('DELETE')

    def do_HEAD(self):
        self._handle_request('HEAD')

    def _handle_request(self, method):
        # 1. Handle custom /hi route
        if self.path == '/hi':
            print("Incoming request path: {} (handled by custom route)".format(self.path)) # Changed from f-string
            self._send_json_response(200, '{"message": "Hello from Python proxy route!"}')
            return

        print("Incoming request path: {} (proxying to {})".format(self.path, TARGET_URL)) # Changed from f-string

        # 2. Extract path and query for the target request
        parsed_url = urllib.parse.urlparse(self.path)
        target_path = parsed_url.path
        if parsed_url.query:
            target_path += '?' + parsed_url.query

        # 3. Prepare headers for the target request
        forward_headers = {}
        for header, value in self.headers.items():
            if header.lower() not in self._exclude_request_headers:
                forward_headers[header] = value

        # Ensure Host header is set correctly for the target server
        # This is crucial for proper routing on the target server if it's virtual-host based
        forward_headers['Host'] = "{}:{}".format(TARGET_HOST, TARGET_PORT) # Changed from f-string
        # print("Forwarding headers: {}".format(forward_headers)) # Uncomment for debugging - Changed from f-string

        try:
            # 4. Make the request to the target server
            conn = http.client.HTTPConnection(TARGET_HOST, TARGET_PORT, timeout=5) # 5-second timeout

            # Read request body for POST/PUT/PATCH
            request_body = None
            if method in ['POST', 'PUT', 'PATCH']:
                content_length = int(self.headers.get('Content-Length', 0))
                request_body = self.rfile.read(content_length)

            conn.request(method, target_path, body=request_body, headers=forward_headers)
            target_response = conn.getresponse()

            # 5. Read target response body
            response_body = target_response.read()

            # 6. Modify response if HTML
            content_type = target_response.getheader('Content-Type', '')
            modified_body = response_body
            is_html_and_modified = False # Flag to track if HTML was modified

            if 'text/html' in content_type:
                try:
                    html_content = response_body.decode('utf-8')
                    # here you should based on old url, to modify the new html code
                    # if you need to get http response, you use get_http_content() function
                    if '</head>' in html_content:
                        modified_html = html_content.replace(
                            '</head>',
                            '<meta name="author" content="yingshaoxo"></head>'
                        )
                        modified_body = modified_html.encode('utf-8')
                        is_html_and_modified = True # Set flag if modification occurred
                        print("HTML response modified.")
                except UnicodeDecodeError:
                    print("Could not decode HTML, skipping modification.")
                    pass # Keep original body if decode fails

            # 7. Forward target response to client
            self.send_response(target_response.status)

            # Copy all headers from target_response
            headers_to_send = {}
            for header, value in target_response.getheaders():
                headers_to_send[header.lower()] = value # Store lowercased for consistent lookup

            # ONLY remove Content-Length and Transfer-Encoding if body was actually modified AND it was HTML
            if is_html_and_modified:
                if 'content-length' in headers_to_send:
                    del headers_to_send['content-length']
                if 'transfer-encoding' in headers_to_send:
                    del headers_to_send['transfer-encoding']

            # Write headers to client
            for header_name, header_value in headers_to_send.items():
                self.send_header(header_name, header_value)
            self.end_headers()

            # For HEAD requests, do not send a body
            if method != 'HEAD':
                self.wfile.write(modified_body)

        except http.client.HTTPException as e:
            print("HTTP client error: {}".format(e)) # Changed from f-string
            self.send_error(502, "Proxy Error: HTTP client error", str(e))
        except ConnectionRefusedError:
            print("Connection refused to {}:{}. Is target server running?".format(TARGET_HOST, TARGET_PORT)) # Changed from f-string
            self.send_error(502, "Proxy Error: Target server refused connection")
        except TimeoutError:
            print("Proxy timeout when connecting to {}:{}.".format(TARGET_HOST, TARGET_PORT)) # Changed from f-string
            self.send_error(504, "Proxy Error: Gateway Timeout")
        except Exception as e:
            print("Unexpected proxy error: {}".format(e), file=sys.stderr) # Changed from f-string
            self.send_error(500, "Internal Proxy Error", str(e))
        finally:
            if 'conn' in locals():
                conn.close() # Ensure connection is closed

if __name__ == '__main__':
    # Create the HTTP server
    httpd = socketserver.TCPServer(("", PROXY_PORT), CustomProxyHandler) # Removed 'with' statement
    try:
        print("Serving proxy on http://localhost:{}".format(PROXY_PORT)) # Changed from f-string
        print("Target server: {}".format(TARGET_URL)) # Changed from f-string
        print("Press Ctrl+C to stop.")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down proxy server.")
    finally:
        # Explicitly shut down the server in the finally block
        httpd.shutdown()
        httpd.server_close()
