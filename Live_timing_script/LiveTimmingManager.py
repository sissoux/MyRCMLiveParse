import json
import requests
import time
import datetime
from pathlib import Path
from PilotClasses import Pilot, Round
import shutil
import secret
import obsws_python as obs
from  Websocket_MyRCM import *
from OBSAutomate import OBS_Auto
import pandas as pd
import generateHTML
from html2image import Html2Image
from ImgGenerator import *
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="A script with a configurable timeout.")

parser.add_argument('-t', type=float, default=0.3, help='Set the timeout value (default: 0.5)')
args = parser.parse_args()
timeout = args.t

def htmlToPng(html_string=None, html_file=None, css_file="Style.css", FilePath=None, size=(1300,1280)):
    try:
        hti = Html2Image(size=size, output_path=Path(FilePath).parent.as_posix(), disable_logging=True, browser="Edge")

        if html_string is not None:
            hti.screenshot(html_str=html_string, css_file=css_file, save_as=Path(FilePath).name)   
    except Exception as e:
        print(f"Failed to convert HTML to PNG: {e}")

LocalOnly = False
generateHTML_PNG = False
UseWebSocket = False

LogInputData = True
LogFileName = Path(f"RaceDataLog-{datetime.datetime.now().strftime("%d%b-%H%M%S")}.txt")

AutomateOBS = True

ReloadDataframe = False
PrevRaceTime = None

if AutomateOBS:
    OBS = OBS_Auto(IP = 'localhost', Port=4455, PassWord=secret.OBSWebSocketPW, verbose=True, debug=False)
    

PublisherServer_IP = "127.0.0.1"
LiveBasePath = Path("C:/RCPARK_Live/Live Course 13/")
RankingServerPath = Path("C:/RCPARK_Live/RankingHTML")
# LiveBasePath = Path("/Volumes/charlesmerlen/Sites/RC")
GdriveBasePath = Path("G:/Mon Drive/Affiches-Graphisme/Course/Course 13 - Oct 2024\YT LIVE")
# GdriveBasePath = Path("/Users/charlesmerlen/Library/CloudStorage/GoogleDrive-rcpark59193@gmail.com/Mon Drive/Affiches-Graphisme/Course/Course 12 - Sept 2024/YT LIVE")
LiveBasePath.mkdir(parents=True, exist_ok=True)
RankingServerPath.mkdir(parents=True, exist_ok=True)

jsonFilePath =      Path(LiveBasePath, "Ranking.json")
htmlFilePath =      Path(LiveBasePath, "Ranking.html")
rankingServerHTMLPath = Path(RankingServerPath, "index.html")
roundFilePath =     Path(LiveBasePath, "Round.txt")
raceTimeFilePath =  Path(LiveBasePath, "temps.txt")
TeamLogoPath =      Path(LiveBasePath, "LogoTeam")
RankingImagePath =  Path(LiveBasePath, "Ranking.png")
RankingImagePath =  Path("Ranking.png")
# rankingServerHTMLPath = Path("index.html")

preGridScreenGen = PreStartScreenGen(LiveBasePath, GdriveBasePath, "ScreenStartLineVide2.png", "Buggy.png", "NewRoundScreen.png")
resultScreenGen = ResultScreenGen(LiveBasePath, GdriveBasePath, "ScreenPodiumVide.png", "Result.png")
gridOverlayGen = GridOverlayScreenGen(LiveBasePath, "StartGridOverlay.png") 

#Copy style files on the correct location to be used by Live and HTML Server
shutil.copyfile("Tableau.css", Path(LiveBasePath, 'Tableau.css'))
shutil.copyfile("style.css", Path(LiveBasePath, 'style.css'))
shutil.copyfile("clock.html", Path(LiveBasePath, 'clock.html'))

shutil.copyfile("detailedRankingStyle.css", Path(RankingServerPath, 'detailedRankingStyle.css'))

index = 0
with open("jsontemplate.txt", 'r', encoding="utf-8") as timefile:
    InputTestFile = timefile.readlines()
response = InputTestFile[0]
Tstart = time.time()

newRound = False
PreviousGroup = None
GeneratedResults = False
ShowedNewRound = False
ShowedResults = True
while (True):

    if Tstart + 0.5 < time.time():
        Tstart = time.time()
        index +=1
        try:
            response = InputTestFile[index]
        except IndexError:
            index = 0

    try:
        if not LocalOnly:
            if UseWebSocket:
                response = get_websocket_response()
            else:
                response = requests.get(f"http://{PublisherServer_IP}/1/StreamingData").text

        js = json.loads(response)
    except ConnectionError:
        print("Cannot reach publisher server")
        continue
    except Exception as e:
        print(e)
        continue

    if LogInputData:
        with open(LogFileName, "+a") as logfile:
            logfile.write(response+"\n")
    # Check if we entered a new round to create new pilot list
    currentGroup = js['EVENT']['METADATA']['SECTION']+js['EVENT']['METADATA']['GROUP']

    if PreviousGroup != currentGroup:
        PreviousGroup = currentGroup
        currentRound = Round(**js['EVENT'])
        if ReloadDataframe:
            currentRound.ReloadDataFramesFromFile(LiveBasePath)
        newRound = True
        ShowedNewRound = False 
        print(f"New round detected: {currentRound.category_pretty}-{currentRound.serie_pretty}")

        preGridScreenGen.generate(currentRound)
        preGridScreenGen.save(currentRound,Path(LiveBasePath, "GridImages"))
        
        gridOverlayGen.generate(currentRound)

    else:
        newRound = False
        currentRound.update(**js['EVENT'])

    if AutomateOBS:
        match currentRound.RaceState:
            case 4|5: #Manche terminée
                if True: #currentRound.RaceEnd:
                    if not GeneratedResults:
                        print("Generating results")
                        GeneratedResults = True
                        resultScreenGen.generate(currentRound)
                        resultScreenGen.save(currentRound,Path(LiveBasePath, "ResultImages"))
                        ShowedResults = False
            case 2|0: #Départ en attente
                if currentRound.RaceEnd ==0:
                    if ShowedNewRound:
                        countdown_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(currentRound.countdown.split(":"))))
                        if "finale" in currentRound.round_pretty.lower():
                            OBS.updateScene(ForceScene=OBS.ManualSceneList["V_Grille" if (5 <= countdown_seconds <= 30) else "V_Vue_Plafond_A_30_45"], ForceDuration=2)
                        else:
                            OBS.updateScene(ForceScene=OBS.ManualSceneList["Comptage"], ForceDuration = 2)

            case 1: #Manche en cours
                GeneratedResults = False
                ShowedNewRound = True #Do not show grid if race is ongoing
            case 0: #Manche terminée
                pass
            case _:
                pass

        if not ShowedResults:
            print("Displaying results")
            ShowedResults = OBS.SetBlockingScene(Scene=OBS.ManualSceneList["Resultats"], Duration = 10)
        if not ShowedNewRound:
            print("Showing grid.")
            ShowedNewRound = OBS.SetBlockingScene(Scene=OBS.ManualSceneList["Serie"], Duration = 10)



        OBS.updateScene()

        
    #add regular dataframeSave
    autoSaveDF=False
    if autoSaveDF:
        for pilot in currentRound.NewLap:
            currentRound.PilotDataFrameDict[pilot].to_csv(Path(LiveBasePath, pilot+".csv"))
        currentRound.NewLap = []

    # Gestion du TEMPS Restant
    RaceTime = currentRound.getRaceTime_pretty()
    if RaceTime != PrevRaceTime:
        PrevRaceTime=RaceTime
        print(f"RaceTime = {RaceTime}")
 
    
    pilotes = []
    
    rankingHtmlBody = generateHTML.getHeaderRanking(RaceTime, showBestLap=False)
    rankingServerHTMLBody = generateHTML.getHeaderDetailedRanking()

    DynamicTableHTMLContent = generateHTML.generateTableHTML(Serie=currentRound.round_pretty, RaceTime=RaceTime, pilots=currentRound.pilotList)

    for pilot in currentRound.pilotList:
        rankingHtmlBody += generateHTML.getPilotRanking(pilot, showBestLap=False)
    
    rankingHtmlBody += '</tbody></table></body>'
    rankingHtmlBody += '</html>'

    try:
        #Save round file
        with open(roundFilePath, 'w',encoding='utf-8') as file:
            file.write(currentRound.round_pretty)
        
        #Save time file
        with open(raceTimeFilePath, 'w',encoding='utf-8') as file:
            file.write(RaceTime)

        #Save HTML file
        with open(htmlFilePath,'w', encoding='utf-8') as file: 
            file.write(rankingHtmlBody)

        if generateHTML_PNG:
            htmlToPng(html_string=rankingHtmlBody, css_file="Style.css", FilePath=RankingImagePath, size=(416,800))

        #Save HTML file
        with open(rankingServerHTMLPath,'w', encoding='utf-8') as file: 
            file.write(rankingServerHTMLBody)

        with open(Path(RankingServerPath,"table_content.json"),'w', encoding='utf-8') as file: 
            json.dump(DynamicTableHTMLContent, file)

        

    except FileNotFoundError:
        print("Problem writing files.\n{e}")
    except PermissionError as e:
        print(f"Permission error while writing files.\n{e}")

    time.sleep(timeout)