import json
import requests
import time
from pathlib import Path
import shutil
from PilotClasses import Round
import generateHTML
import argparse
import http.server
import socketserver
import os
import threading

# Set up argument parser
parser = argparse.ArgumentParser(description="A script with a configurable timeout and HTTP server.")
parser.add_argument('-t', type=float, default=0.5, help='Set the timeout value (default: 0.5)')
parser.add_argument('-p', type=int, default=8080, help='Set the port for the HTTP server (default: 8080)')
args = parser.parse_args()
timeout = args.t
port = args.p

LocalOnly = True
PublisherServer_IP = "192.168.0.6"

# Define the RankingServer directory using Pathlib and ensure it exists
RankingServerPath = Path.cwd() / "RankingServer"
RankingServerPath.mkdir(parents=True, exist_ok=True)

# Copy CSS file to the RankingServer folder
shutil.copyfile("detailedRankingStyle.css", RankingServerPath / 'detailedRankingStyle.css')
# shutil.copyfile("lightRankingStyle.css", RankingServerPath / 'lightRankingStyle.css')

index = 0
with open("jsontemplate.txt", 'r', encoding="utf-8") as timefile:
    InputTestFile = timefile.readlines()
response = InputTestFile[0]
Tstart = time.time()

PreviousGroup = ""
newRound = False

# Initialize currentRound with None
currentRound = None

# In-memory variables to hold the latest generated table content (JSON)
latest_table_content = {}
latest_light_table_content = {}

# Function to handle the data fetching and HTML generation
def update_data():
    global index, response, Tstart, PreviousGroup, newRound, latest_table_content, latest_light_table_content, currentRound

    if Tstart + 5 < time.time():
        Tstart = time.time()
        index += 1
        try:
            response = InputTestFile[index]
        except IndexError:
            index = 0

    try:
        if not LocalOnly:
            response = requests.get(f"http://{PublisherServer_IP}/1/StreamingData").text

        js = json.loads(response)
    except requests.ConnectionError:
        print("Cannot reach publisher server")
        return
    except Exception as e:
        print(f"Error parsing response: {e}")
        return

    # Check if we entered a new round to create a new pilot list
    currentGroup = js['EVENT']['METADATA']['SECTION'] + js['EVENT']['METADATA']['GROUP']
    
    if PreviousGroup != currentGroup:
        PreviousGroup = currentGroup
        currentRound = Round(**js['EVENT'])
        newRound = True
    else:
        newRound = False
        if currentRound is not None:
            currentRound.update(**js['EVENT'])
        else:
            print("currentRound is None, skipping update.")
            return

    # Gestion du TEMPS Restant
    RaceTime = currentRound.getRaceTime_pretty() if currentRound else "N/A"
    print(f"RaceTime = {RaceTime}")

    # Generate detailed and light ranking HTML pages
    rankingServerHTMLBody = generateHTML.getHeaderDetailedRanking()
    latest_table_content = generateHTML.generateTableHTML(
        Serie=currentRound.round_pretty, RaceTime=RaceTime, pilots=currentRound.pilotList)
    
    lightRankingHTMLBody = generateHTML.getHeaderLightRanking()
    latest_light_table_content = generateHTML.generateLightTableHTML(
        Serie=currentRound.round_pretty, RaceTime=RaceTime, pilots=currentRound.pilotList)

    try:
        # Save detailed HTML file (index.html)
        index_html_path = RankingServerPath / "index.html"
        with index_html_path.open('w', encoding='utf-8') as file:
            file.write(rankingServerHTMLBody)

        # Save light ranking HTML file (light.html)
        light_html_path = RankingServerPath / "light.html"
        with light_html_path.open('w', encoding='utf-8') as file:
            file.write(lightRankingHTMLBody)

    except FileNotFoundError as e:
        print(f"Problem writing files: {e}")
    except PermissionError as e:
        print(f"Permission error while writing files: {e}")

# HTTP Server Class
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/updateTable':  # Serve detailed table content
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Serve the latest detailed table content from memory
            if latest_table_content:
                self.wfile.write(json.dumps(latest_table_content).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({"error": "No data available"}).encode('utf-8'))
        
        elif self.path == '/updateLightTable':  # Serve light table content
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Serve the latest light table content from memory
            if latest_light_table_content:
                self.wfile.write(json.dumps(latest_light_table_content).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({"error": "No data available"}).encode('utf-8'))
        
        else:
            # Serve static files (HTML, CSS)
            super().do_GET()

# Function to run the HTTP server
def run_server():
    # Set the working directory to RankingServerPath
    os.chdir(RankingServerPath)
    PORT = port
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Serving HTTP on port {PORT} from {RankingServerPath}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server is shutting down.")
            httpd.shutdown()

# Main loop to handle data fetching and HTML generation
if __name__ == "__main__":
    # Run the HTTP server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Main loop to update data and generate files
    while True:
        update_data()
        time.sleep(timeout)
