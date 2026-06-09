import http.server
import socketserver
import sys
import urllib.request
import urllib.parse

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/tts'):
            try:
                # Parse query parameters
                parsed_url = urllib.parse.urlparse(self.path)
                params = urllib.parse.parse_qs(parsed_url.query)
                text = params.get('text', [''])[0].strip()
                lang = params.get('lang', ['en-US'])[0]
                
                # Extract base language code (e.g., "en-US" -> "en")
                base_lang = lang.split('-')[0].split('_')[0]
                
                if not text:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Missing text parameter")
                    return
                
                # Split text into chunks of max 150 characters for the Google TTS API
                chunks = []
                current_chunk = ""
                for char in text:
                    current_chunk += char
                    if len(current_chunk) >= 150 and char in "。！？；，、,.!? \n":
                        chunks.append(current_chunk.strip())
                        current_chunk = ""
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # Fallback if splitting yielded empty list but text exists
                if not chunks:
                    chunks = [text]
                
                # Ensure no single chunk is too long for the API (max 200 characters)
                final_chunks = []
                for chunk in chunks:
                    if len(chunk) > 200:
                        for i in range(0, len(chunk), 200):
                            final_chunks.append(chunk[i:i+200])
                    else:
                        final_chunks.append(chunk)
                
                merged_mp3 = b""
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                
                for chunk in final_chunks:
                    if not chunk:
                        continue
                    url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={base_lang}&client=tw-ob&q={urllib.parse.quote(chunk)}"
                    req = urllib.request.Request(url, headers=headers)
                    try:
                        with urllib.request.urlopen(req) as response:
                            merged_mp3 += response.read()
                    except Exception as tts_err:
                        print(f"Error fetching TTS chunk: {tts_err}")
                
                if merged_mp3:
                    self.send_response(200)
                    self.send_header('Content-Type', 'audio/mpeg')
                    self.send_header('Content-Disposition', 'attachment; filename="speech.mp3"')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    self.end_headers()
                    self.wfile.write(merged_mp3)
                else:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b"Failed to generate TTS audio")
            except Exception as e:
                print(f"TTS API Error: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
            return
            
        # Call the parent do_GET for static files
        super().do_GET()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        # Prevent caching for testing
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

# Map file extensions explicitly to fix Windows registry MIME type issues
MyHTTPRequestHandler.extensions_map.update({
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.wasm': 'application/wasm',
    '.html': 'text/html',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.ico': 'image/x-icon',
})

if __name__ == '__main__':
    # Allow port to be configurable
    port = PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        
    # Allow address reuse to prevent "address already in use" errors on restarts
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), MyHTTPRequestHandler) as httpd:
        print(f"Serving at port {port} with custom MIME types and no-cache headers...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server.")
            sys.exit(0)
