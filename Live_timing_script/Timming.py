#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 21:29:40 2024

@author: charlesmerlen
"""

import json
import requests
import time
import random
from pathlib import Path
from PilotClasses import Pilot, Round
import re
import shutil
import secret
import obsws_python as obs
from OBSAutomate import OBS_Auto
import pandas as pd
import generateHTML



LocalOnly = True
AutomateOBS = False
enableSevenSegDisplay = False
StatisticDisplayPeriod = 15 * 60 #s

ReloadDataframe = True

if AutomateOBS:
    OBS = OBS_Auto(IP = 'localhost', Port=4455, PassWord=secret.OBSWebSocketPW, verbose=True, debug=True)
    

PublisherServer_IP = "192.168.0.176"
LiveBasePath = Path("C:/RCPARK_Live/Live Endurance/")
LiveBasePath.mkdir(parents=True, exist_ok=True)

jsonFilePath =      Path(LiveBasePath, "Ranking.json")
htmlFilePath =      Path(LiveBasePath, "Ranking.html")
htmlTableFilePath = Path(LiveBasePath, "Table.html")
roundFilePath =     Path(LiveBasePath, "Round.txt")
raceTimeFilePath =  Path(LiveBasePath, "temps.txt")
TeamLogoPath =      Path(LiveBasePath, "LogoTeam")

shutil.copyfile("Tableau.css", Path(LiveBasePath, 'Tableau.css'))

if enableSevenSegDisplay:
    from displayDriver import Display
    disp = Display(numberOfLines=3, Port="/dev/ttyS0")

response = '{   "EVENT": {       "CONFIG": {           "MODE": "LapAndTime",           "NROFBESTLAPS": 0       },       "DATA": [           {               "ABSOLUTTIME": "04:21.095",               "BESTTIME": "19.212",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "BRCA",               "COLOR": 2,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "0.000",               "DELAYTIMEPREVIOUS": "0.000",               "FORECAST": "15 05:03.003",               "INDEX": 1,               "LAPINFO": "",               "LAPS": 13,               "LAPTIME": "20.030",               "MEDIUMTIME": "20.084",               "PILOT": "Boda Clément",               "PILOTNUMBER": 0,               "PROGRESS": 0,               "SPEED": "27,14",               "STANDARDDEVIATION": "1.077",               "TEMPERATUR": "20 °C",               "TRANSPONDER": "9666194",               "TREND": 1,               "VEHICLE": 1,               "VOLTAGE": "5,7 V"           },           {               "ABSOLUTTIME": "04:17.567",               "BESTTIME": "19.351",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "880",               "COLOR": 7,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-1",               "DELAYTIMEPREVIOUS": "-1",               "FORECAST": "14 05:01.595",               "INDEX": 2,               "LAPINFO": "",               "LAPS": 12,               "LAPTIME": "25.779",               "MEDIUMTIME": "21.463",               "PILOT": "Vandenberghe Davidddddddddddddddddd",               "PILOTNUMBER": 0,               "PROGRESS": 6,               "SPEED": "21,09",               "STANDARDDEVIATION": "2.115",               "TEMPERATUR": "12 °C",               "TRANSPONDER": "2857229",               "TREND": -1,               "VEHICLE": 2,               "VOLTAGE": "5,7 V"           },           {               "ABSOLUTTIME": "03:57.002",               "BESTTIME": "19.640",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "",               "COLOR": 1,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-2",               "DELAYTIMEPREVIOUS": "-1",               "FORECAST": "14 05:03.731",               "INDEX": 3,               "LAPINFO": "",               "LAPS": 11,               "LAPTIME": "24.766",               "MEDIUMTIME": "21.545",               "PILOT": "Tony RC",               "PILOTNUMBER": 0,               "PROGRESS": 90,               "SPEED": "21,95",               "STANDARDDEVIATION": "2.369",               "TEMPERATUR": "20 °C",               "TRANSPONDER": "2398220",               "TREND": -1,               "VEHICLE": 4,               "VOLTAGE": "6,9 V"           },           {               "ABSOLUTTIME": "04:06.838",               "BESTTIME": "20.852",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "",               "COLOR": 7,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-2",               "DELAYTIMEPREVIOUS": "+9.836",               "FORECAST": "14 05:14.092",               "INDEX": 4,               "LAPINFO": "",               "LAPS": 11,               "LAPTIME": "21.173",               "MEDIUMTIME": "22.439",               "PILOT": "Clarhaut Vincnnnnnnnnnnnnnnnnnent",               "PILOTNUMBER": 0,               "PROGRESS": 51,               "SPEED": "25,67",               "STANDARDDEVIATION": "1.954",               "TEMPERATUR": "11 °C",               "TRANSPONDER": "8926221",               "TREND": 1,               "VEHICLE": 3,               "VOLTAGE": "7,1 V"           },           {               "ABSOLUTTIME": "04:08.981",               "BESTTIME": "22.157",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "1176",               "COLOR": 7,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-3",               "DELAYTIMEPREVIOUS": "-1",               "FORECAST": "13 05:24.275",               "INDEX": 5,               "LAPINFO": "",               "LAPS": 10,               "LAPTIME": "23.243",               "MEDIUMTIME": "24.898",               "PILOT": "domis fabien",               "PILOTNUMBER": 0,               "PROGRESS": 20,               "SPEED": "23,39",               "STANDARDDEVIATION": "2.735",               "TEMPERATUR": "15 °C",               "TRANSPONDER": "3567179",               "TREND": 1,               "VEHICLE": 6,               "VOLTAGE": "5,8 V"           },           {               "ABSOLUTTIME": "03:45.304",               "BESTTIME": "25.920",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "Rc park",               "COLOR": 1,               "COUNTRY": "BEL",               "DELAYTIMEFIRST": "-5",               "DELAYTIMEPREVIOUS": "-2",               "FORECAST": "10 05:08.071",               "INDEX": 6,               "LAPINFO": "",               "LAPS": 8,               "LAPTIME": "27.370",               "MEDIUMTIME": "28.163",               "PILOT": "BILLE eddy",               "PILOTNUMBER": 0,               "PROGRESS": 100,               "SPEED": "19,86",               "STANDARDDEVIATION": "2.555",               "TEMPERATUR": "6 °C",               "TRANSPONDER": "3830740",               "TREND": -1,               "VEHICLE": 5,               "VOLTAGE": "6,0 V"           }       ],       "KEY": "B18D6AD15E176B658F02",       "METADATA": {           "COUNTDOWN": "00:00:00",           "CURRENTTIME": "01:04:14",           "DIVERGENCE": "00:00:00",           "GROUP": "101 :: Qualification :: Série 1 - Heat 1",           "NAME": "TONY RC MEETING",           "RACETIME": "06:00:00",           "REMAININGTIME": "04:25:46",           "SECTION": "RC PARK 1/10 TT 4X2 OPEN  [101]"       },       "TIMESTAMP": "1345831324",       "VERSION": "1.0"   }}'

newRound = False
PreviousGroup = None

while (True):

    if AutomateOBS:
        OBS.updateScene()

    try:
        if not LocalOnly:
            response = requests.get(f"http://{PublisherServer_IP}/1/StreamingData").text
        js = json.loads(response)
    except ConnectionError:
        print("Cannot reach publisher server")
        continue

    # Check if we entered a new round to create new pilot list
    currentGroup = js['EVENT']['METADATA']['SECTION']+js['EVENT']['METADATA']['GROUP']

    if PreviousGroup != currentGroup:
        PreviousGroup = currentGroup
        currentRound = Round(**js['EVENT'])
        if ReloadDataframe:
            currentRound.ReloadDataFramesFromFile(LiveBasePath)
        newRound = True
        try:
            shutil.copyfile(Path(LiveBasePath,currentRound.picPath), Path(LiveBasePath, 'seriePic.JPG'))
            shutil.copyfile(Path(LiveBasePath,currentRound.bannerPath), Path(LiveBasePath, 'banner.JPG'))
        except:
            print("Cannot find the requested picture. Serie picture not updated.")
    else:
        newRound = False
        currentRound.update(**js['EVENT'])

    #add regular dataframeSave
    autoSaveDF=True
    if autoSaveDF:
        for pilot in currentRound.NewLap:
            currentRound.PilotDataFrameDict[pilot].to_csv(Path(LiveBasePath, pilot+".csv"))
        currentRound.NewLap = []

    # Gestion du TEMPS Restant
    RaceTime = currentRound.getRaceTime_pretty()

    ''' GESTION DU FICHIER Tableau.html '''
    
    pilotes = []
    
    texte = ""

    htmlbody = generateHTML.getHeader(RaceTime)
    tabhtmlbody = generateHTML.getHeaderTable(RaceTime)

    for pilot in currentRound.pilotList:
        htmlbody += generateHTML.getPilot(pilot, TeamLogoPath)
        tabhtmlbody += generateHTML.getPilotTable(pilot, TeamLogoPath)

        pilotes.append({
            "Pos":pilot.position,
            "Car":pilot.vehicle,
            "PrenomNom":pilot.pilot
            })

    if enableSevenSegDisplay and len(currentRound.pilotList)>=disp.numberOfLines: 
        disp.setLines([f"{pilot.vehicle:02d}-{pilot.besttime_s:05.2f}-{pilot.laps:02d}" for pilot in currentRound.pilotList[:disp.numberOfLines]])
        disp.updateDisplay()
    
    htmlbody += '</tbody></table></body>'
    htmlbody += '</html>'

    try:
        #Save round file
        with open(roundFilePath, 'w',encoding='utf-8') as file:
            file.write(currentRound.round_pretty)
        
        #Save time file
        with open(raceTimeFilePath, 'w',encoding='utf-8') as file:
            file.write(RaceTime)

        #Save HTML file
        with open(htmlFilePath,'w', encoding='utf-8') as file: 
            file.write(htmlbody)
        #Save HTML file
        with open(htmlTableFilePath,'w', encoding='utf-8') as file: 
            file.write(tabhtmlbody)
        
        #save pilots file
        with open(jsonFilePath,'w', encoding='utf-8') as file: 
            json.dump(pilotes,file)
        
        #Save Json as text file
        fichier_texte = Path(jsonFilePath).with_suffix(".txt")
        with open(fichier_texte, 'w',encoding='utf-8') as file:
                file.write(texte)

    except FileNotFoundError:
        print("Problem writing files.\n{e}")
    except PermissionError as e:
        print(f"Permission error while writing files.\n{e}")

    time.sleep(0.5)