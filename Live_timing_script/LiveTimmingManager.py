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

LocalOnly = True
generateHTML_PNG = True
UseWebSocket = False

LogInputData = False
LogFileName = Path(f"RaceDataLog-{datetime.datetime.now().strftime("%d%b-%H%M%S")}.txt")

AutomateOBS = False

ReloadDataframe = False

if AutomateOBS:
    OBS = OBS_Auto(IP = 'localhost', Port=4455, PassWord=secret.OBSWebSocketPW, verbose=False, debug=False)
    

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
while (True):

    if Tstart + 5 < time.time():
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
        generateMainPreRaceGridImage(currentRound, outputPath=Path(LiveBasePath, "NewRoundScreen.png"), backgroundImagePath=Path(GdriveBasePath,"ScreenStartLineVide2.png"), buggyImagePath=Path(GdriveBasePath,"Buggy.png"))
        shutil.copyfile(Path(LiveBasePath, "NewRoundScreen.png"), Path(LiveBasePath, "GeneratedImages", f"{currentRound.category_pretty}-{currentRound.serie_pretty}-NewRoundScreen.png"))
        generateMainResultImage(currentRound, backgroundImagePath=Path(GdriveBasePath,"ScreenPodiumVide.png"), outputPath=Path("Result.png"))                      
        generateStartGridOverlay(currentRound, outputPath=Path(LiveBasePath, "StartGridOverlay.png"))
        # try:
        #     if currentRound.picPath is not None:
        #         shutil.copyfile(Path(LiveBasePath,currentRound.picPath), Path(LiveBasePath, 'seriePic.JPG'))
        #     if currentRound.bannerPath is not None:
        #         shutil.copyfile(Path(LiveBasePath,currentRound.bannerPath), Path(LiveBasePath, 'banner.JPG'))
        # except:
        #     print("Cannot find the requested picture. Serie picture not updated.")
    else:
        newRound = False
        currentRound.update(**js['EVENT'])

        if AutomateOBS:
            if not ShowedNewRound:
                ShowedNewRound = OBS.updateScene(ForceScene=OBS.ManualSceneList["Serie_T_"], ForceDuration = 10, Block = True)
            match currentRound.RaceState:
                case 4|5: #Manche terminée
                    if True: #currentRound.RaceEnd:
                        if not GeneratedResults:
                            GeneratedResults = True
                            generateMainResultImage(currentRound, backgroundImagePath=Path(GdriveBasePath,"ScreenStartLine-CMN.png"), buggyImagePath=Path(GdriveBasePath,"Buggy.png"), outputPath=Path(LiveBasePath, "MainRanking.png"))
                        print("Round is over, Displaying results")
                        OBS.updateScene(ForceScene=OBS.ManualSceneList["Resultats"], ForceDuration = 15)
                case 2|0: #Départ en attente
                    print("Waiting race to start. Showing grid.")
                    countdown_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(currentRound.countdown.split(":"))))
                    if "finale" in currentRound.round_pretty.lower():
                        OBS.updateScene(ForceScene=OBS.ManualSceneList["V_Grille" if (5 <= countdown_seconds <= 30) else "V_Vue_Plafond_A_30_45"], ForceDuration=15)
                    else:
                        OBS.updateScene()
                case 1: #Manche en cours
                    GeneratedResults = False
                    OBS.updateScene()
                case _:
                    if True: #currentRound.RaceEnd:
                        if not GeneratedResults:
                            GeneratedResults = True
                            generateMainRankingImage(currentRound, backgroundImagePath=Path(GdriveBasePath,"ScreenStartLine-CMN.png"), buggyImagePath=Path(GdriveBasePath,"Buggy.png"), outputPath=Path(LiveBasePath, "MainRanking.png"))
                        print("Round is over, Displaying results")
                        OBS.updateScene(ForceScene=OBS.ManualSceneList["Resultats"], ForceDuration = 15)

    #add regular dataframeSave
    autoSaveDF=False
    if autoSaveDF:
        for pilot in currentRound.NewLap:
            currentRound.PilotDataFrameDict[pilot].to_csv(Path(LiveBasePath, pilot+".csv"))
        currentRound.NewLap = []

    # Gestion du TEMPS Restant
    RaceTime = currentRound.getRaceTime_pretty()
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