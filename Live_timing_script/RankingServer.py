import http.server
import socketserver
import json
from pathlib import Path

# Define the folder to serve index.html and other static assets
web_dir = Path("C:/RCPARK_Live/RankingHTML")
json_file_path = web_dir / "table_content.json"

# Ensure the JSON file exists
if not json_file_path.is_file():
    raise FileNotFoundError(f"JSON file {json_file_path} does not exist")

# Change the working directory to the specified folder
import os
os.chdir(web_dir)

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/updateTable':  # Serve updated table content from the JSON file
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Read the JSON file containing thead and tbody data
            with open(json_file_path, 'r', encoding='utf-8') as f:
                table_data = json.load(f)

            # Send the JSON content as the response
            self.wfile.write(json.dumps(table_data).encode('utf-8'))
        else:
            # Serve other files normally
            super().do_GET()

# Set up the server
PORT = 8080

with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
    print(f"Serving HTTP on port {PORT} from {web_dir}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server is shutting down.")
        httpd.shutdown()
