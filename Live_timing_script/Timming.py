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

from displayDriver import Display

serverIP = "192.168.0.176"
LiveBasePath = Path("C:/RCPARK_Live/Live Course 9/")
LiveBasePath.mkdir(parents=True, exist_ok=True)

jsonFilePath =      Path(LiveBasePath, "Ranking.json")
htmlFilePath =      Path(LiveBasePath, "Ranking.html")
roundFilePath =     Path(LiveBasePath, "Round.txt")
raceTimeFilePath =  Path(LiveBasePath, "temps.txt")

LocalOnly = True

enableSevenSegDisplay = True
if enableSevenSegDisplay:
    disp = Display(numberOfLines=3, Port="COM5")

response = '{   "EVENT": {       "CONFIG": {           "MODE": "LapAndTime",           "NROFBESTLAPS": 0       },       "DATA": [           {               "ABSOLUTTIME": "04:21.095",               "BESTTIME": "19.212",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "BRCA",               "COLOR": 2,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "0.000",               "DELAYTIMEPREVIOUS": "0.000",               "FORECAST": "15 05:03.003",               "INDEX": 1,               "LAPINFO": "",               "LAPS": 13,               "LAPTIME": "20.030",               "MEDIUMTIME": "20.084",               "PILOT": "Boda Clément",               "PILOTNUMBER": 0,               "PROGRESS": 0,               "SPEED": "27,14",               "STANDARDDEVIATION": "1.077",               "TEMPERATUR": "20 °C",               "TRANSPONDER": "9666194",               "TREND": 1,               "VEHICLE": 1,               "VOLTAGE": "5,7 V"           },           {               "ABSOLUTTIME": "04:17.567",               "BESTTIME": "19.351",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "880",               "COLOR": 7,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-1",               "DELAYTIMEPREVIOUS": "-1",               "FORECAST": "14 05:01.595",               "INDEX": 2,               "LAPINFO": "",               "LAPS": 12,               "LAPTIME": "25.779",               "MEDIUMTIME": "21.463",               "PILOT": "Vandenberghe Davidddddddddddddddddd",               "PILOTNUMBER": 0,               "PROGRESS": 6,               "SPEED": "21,09",               "STANDARDDEVIATION": "2.115",               "TEMPERATUR": "12 °C",               "TRANSPONDER": "2857229",               "TREND": -1,               "VEHICLE": 2,               "VOLTAGE": "5,7 V"           },           {               "ABSOLUTTIME": "03:57.002",               "BESTTIME": "19.640",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "",               "COLOR": 1,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-2",               "DELAYTIMEPREVIOUS": "-1",               "FORECAST": "14 05:03.731",               "INDEX": 3,               "LAPINFO": "",               "LAPS": 11,               "LAPTIME": "24.766",               "MEDIUMTIME": "21.545",               "PILOT": "Tony RC",               "PILOTNUMBER": 0,               "PROGRESS": 90,               "SPEED": "21,95",               "STANDARDDEVIATION": "2.369",               "TEMPERATUR": "20 °C",               "TRANSPONDER": "2398220",               "TREND": -1,               "VEHICLE": 4,               "VOLTAGE": "6,9 V"           },           {               "ABSOLUTTIME": "04:06.838",               "BESTTIME": "20.852",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "",               "COLOR": 7,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-2",               "DELAYTIMEPREVIOUS": "+9.836",               "FORECAST": "14 05:14.092",               "INDEX": 4,               "LAPINFO": "",               "LAPS": 11,               "LAPTIME": "21.173",               "MEDIUMTIME": "22.439",               "PILOT": "Clarhaut Vincnnnnnnnnnnnnnnnnnent",               "PILOTNUMBER": 0,               "PROGRESS": 51,               "SPEED": "25,67",               "STANDARDDEVIATION": "1.954",               "TEMPERATUR": "11 °C",               "TRANSPONDER": "8926221",               "TREND": 1,               "VEHICLE": 3,               "VOLTAGE": "7,1 V"           },           {               "ABSOLUTTIME": "04:08.981",               "BESTTIME": "22.157",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "1176",               "COLOR": 7,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-3",               "DELAYTIMEPREVIOUS": "-1",               "FORECAST": "13 05:24.275",               "INDEX": 5,               "LAPINFO": "",               "LAPS": 10,               "LAPTIME": "23.243",               "MEDIUMTIME": "24.898",               "PILOT": "domis fabien",               "PILOTNUMBER": 0,               "PROGRESS": 20,               "SPEED": "23,39",               "STANDARDDEVIATION": "2.735",               "TEMPERATUR": "15 °C",               "TRANSPONDER": "3567179",               "TREND": 1,               "VEHICLE": 6,               "VOLTAGE": "5,8 V"           },           {               "ABSOLUTTIME": "03:45.304",               "BESTTIME": "25.920",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "Rc park",               "COLOR": 1,               "COUNTRY": "BEL",               "DELAYTIMEFIRST": "-5",               "DELAYTIMEPREVIOUS": "-2",               "FORECAST": "10 05:08.071",               "INDEX": 6,               "LAPINFO": "",               "LAPS": 8,               "LAPTIME": "27.370",               "MEDIUMTIME": "28.163",               "PILOT": "BILLE eddy",               "PILOTNUMBER": 0,               "PROGRESS": 100,               "SPEED": "19,86",               "STANDARDDEVIATION": "2.555",               "TEMPERATUR": "6 °C",               "TRANSPONDER": "3830740",               "TREND": -1,               "VEHICLE": 5,               "VOLTAGE": "6,0 V"           }       ],       "KEY": "B18D6AD15E176B658F02",       "METADATA": {           "COUNTDOWN": "00:00:00",           "CURRENTTIME": "00:04:14",           "DIVERGENCE": "00:00:00",           "GROUP": "101 :: Qualification :: Série 1 - Heat 1",           "NAME": "TONY RC MEETING",           "RACETIME": "00:05:00",           "REMAININGTIME": "00:00:46",           "SECTION": "RC PARK 1/10 TT 4X2 OPEN  [101]"       },       "TIMESTAMP": "1345831324",       "VERSION": "1.0"   }}'

newRound = True

PreviousGroup = None

while (True):
    try:
        if not LocalOnly:
            response = requests.get(f"http://{serverIP}/1/StreamingData").text
        js = json.loads(response)
    except ConnectionError:
        print("Cannot reach publisher server")
        continue

    # Check if we entered a new round to create new pilot list
    currentGroup = js['EVENT']['METADATA']['SECTION']+js['EVENT']['METADATA']['GROUP']

    if PreviousGroup != currentGroup:
        PreviousGroup = currentGroup
        currentRound = Round(**js['EVENT'])
    else:
        currentRound.update(**js['EVENT'])

    print(currentRound.getRaceTime_pretty())

    for pilot in currentRound.pilotList:
        print(f"Pilot {pilot.pilot} is in {pilot.index} position with {pilot.laps} laps in {pilot.absoluttime}s.")

    if enableSevenSegDisplay: 
        disp.setLines(["01-17.58-10", "03-17.16-10", "08-20.58-09"])
        disp.updateDisplay()

    # Gestion du TEMPS Restant

    RaceTime = currentRound.getRaceTime_pretty()
        
    print(RaceTime)

    ''' GESTION DU FICHIER Tableau.html '''
    print(f"Nbre Pilote {currentRound.numberOfPilots}")
    
    pilotes = []
    
    texte = ""

    htmlbody = '<!DOCTYPE html><html>'
    htmlbody += '<head><title>Page Title</title><meta http-equiv="refresh" content="1">'
    htmlbody += '<head>'
    htmlbody += '<meta charset="UTF-8">'
    # htmlbody +=  "<script>function autoRefresh() {window.location = window.location.href;}setInterval('autoRefresh()', 300);</script>"
    htmlbody += '<link href="style.css" rel="stylesheet">'
    htmlbody += '</head>'

    entete = '<body><table><thead>'
    entete += '<tr><td colspan="5" id="timming" style="height: 60px;font-size: 50px;font-family: Montserrat;">'+RaceTime+'</td></tr>'
    entete += '<tr><th></th><th></th><th>Driver</th><th>Lap</th><th>Best</th></tr>'
    entete += '</thead><tbody>'
    htmlbody += entete

    for pilot in currentRound.pilotList:
        print(f"Pilot {pilot.pilot} is in {pilot.position}")
        htmlpilot = f"<tr><td>{pilot.position}</td><td>{pilot.vehicle}</td><td>{pilot.pilot.upper()}</td><td>{pilot.laps}</td><td>{pilot.besttime_s:0.3f}</td></tr>"
        htmlbody += htmlpilot

        pilotes.append({
            "Pos":pilot.position,
            "Car":pilot.vehicle,
            "PrenomNom":pilot.pilot
            })
        
    #     # texte += ""+str(js['EVENT']['DATA'][i]['INDEX']) + ". -" + str(js['EVENT']['DATA'][i]['VEHICLE'])+ "- L"+str(js['EVENT']['DATA'][i]['LAPS'])+" "+js['EVENT']['DATA'][i]['PILOT'].title()+ "\n"
        texte += f"{pilot.position}. -{pilot.vehicle}- L{pilot.laps}\n"

    
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

    time.sleep(1)