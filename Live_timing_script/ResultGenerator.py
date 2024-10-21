import pandas as pd
import os
from ImgGenerator import ResultScreenGen
from pathlib import Path

class FakeRound:
    def __init__(self, category_pretty, serie_pretty, pilotList):
        self.pilotList = [FakePilot(pilot=x["Pilot"], besttime_s=x["Best Time"]) for x in pilotList]
        self.category_pretty = category_pretty
        self.serie_pretty = serie_pretty

class FakePilot:
    def __init__(self, pilot, besttime_s):
        self.besttime_s = besttime_s
        self.pilot = pilot
        self.LastName = " ".join(self.pilot.split(" ")[:-1])
        self.FirstName = self.pilot.split(" ")[-1]

# Function to extract the best time from the runs
def extract_best_time(runs):
    best_time = None
    for run in runs:
        try:
            dat = run.split("\t")[4]
            if dat != '0:00.000':
                time = float(dat.split(":")[-1])
                if best_time is None:
                    best_time=time
                else:
                    best_time=time if time<best_time or best_time is None else best_time
        except:
            print("Error parsing bestTime")
    return best_time

def ParseRankingFile(FileName):
    # Read the file (replace 'yourfile.csv' with the actual file path)
    with open(FileName, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Initialize variables
    pilots = []
    runs = []
    current_pilot = {}
    collecting_runs = False
    counter = 100
    # Parse the file
    for line in lines[:-1]:
        line = line.strip()
        counter+=1
        
        if line.startswith("Rank") or line.startswith("Run\tCounted") or counter <3:
            continue  # Skip headers
        
        if line.startswith("Final Runs:"):
            collecting_runs = True
            current_pilot['Runs'] = []
            continue
        
        if line.startswith("Qualifying result:"):
            counter=0
            collecting_runs = False
            # Extract best time from runs
            best_time = extract_best_time(current_pilot['Runs'])
            current_pilot['Best Time'] = best_time
            pilots.append(current_pilot)
            current_pilot = {}
            continue
        try:
            if collecting_runs and line:
                current_pilot['Runs'].append(line)
            else:
                # Collect main table data
                if line and not line.startswith("Final Runs"):
                    fields = line.split('\t')
                    current_pilot = {
                        'Pilot': fields[3].strip(),
                        'Rank': fields[0].strip(),
                        'License Nr.': fields[4].strip(),
                        'Country': fields[8].strip(),
                        'Model': fields[9].strip(),
                        'Points': fields[5].strip()
                    }
        except Exception as e:
            print(f"Error on line: {line}")
    # Convert to DataFrame
    return pilots
    
# Define the folder containing the CSV files
folder_path = 'RankingDataIn'

# Dictionary to hold filenames and corresponding DataFrames
file_dataframes = {}
LiveBasePath = Path("C:/RCPARK_Live/Live Course 13/")
GdriveBasePath = Path("G:/Mon Drive/Affiches-Graphisme/Course/Course 13 - Oct 2024\YT LIVE")

generator = ResultScreenGen(LiveBasePath, GdriveBasePath, "ScreenPodiumVide.png", "Result.png")
# Loop through all CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        # Parse the CSV file and get the DataFrame
        pilots = ParseRankingFile(file_path)
        Round = FakeRound(filename.split("_")[0],filename.split("_")[1][:-4], pilots)
        print(f"Generating image for {Round.category_pretty}:")
        generator.generate(Round)
        generator.save(Round,Path(LiveBasePath, "FinalesResultImages"))
print("Done.")