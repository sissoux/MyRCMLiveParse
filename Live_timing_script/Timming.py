#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 21:29:40 2024

@author: charlesmerlen
"""

import shutil
import os
# import Reference as r
import json
import requests
import time
import random
from pathlib import Path

LiveBasePath = Path("C:/RCPARK_Live/Live Course 9/")
LiveBasePath.mkdir(parents=True, exist_ok=True)

jsonFilePath =  Path(LiveBasePath, "Ranking.json")
htmlFilePath =  Path(LiveBasePath, "Ranking.html")
roundFilePath =  Path(LiveBasePath, "Round.txt")
raceTimeFilePath =  Path(LiveBasePath, "temps.txt")

LocalOnly = True

response = '{   "EVENT": {       "CONFIG": {           "MODE": "LapAndTime",           "NROFBESTLAPS": 0       },       "DATA": [           {               "ABSOLUTTIME": "04:21.095",               "BESTTIME": "19.212",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "BRCA",               "COLOR": 2,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "0.000",               "DELAYTIMEPREVIOUS": "0.000",               "FORECAST": "15 05:03.003",               "INDEX": 1,               "LAPINFO": "",               "LAPS": 13,               "LAPTIME": "20.030",               "MEDIUMTIME": "20.084",               "PILOT": "Boda Clément",               "PILOTNUMBER": 0,               "PROGRESS": 0,               "SPEED": "27,14",               "STANDARDDEVIATION": "1.077",               "TEMPERATUR": "20 °C",               "TRANSPONDER": "9666194",               "TREND": 1,               "VEHICLE": 1,               "VOLTAGE": "5,7 V"           },           {               "ABSOLUTTIME": "04:17.567",               "BESTTIME": "19.351",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "880",               "COLOR": 7,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-1",               "DELAYTIMEPREVIOUS": "-1",               "FORECAST": "14 05:01.595",               "INDEX": 2,               "LAPINFO": "",               "LAPS": 12,               "LAPTIME": "25.779",               "MEDIUMTIME": "21.463",               "PILOT": "Vandenberghe Davidddddddddddddddddd",               "PILOTNUMBER": 0,               "PROGRESS": 6,               "SPEED": "21,09",               "STANDARDDEVIATION": "2.115",               "TEMPERATUR": "12 °C",               "TRANSPONDER": "2857229",               "TREND": -1,               "VEHICLE": 2,               "VOLTAGE": "5,7 V"           },           {               "ABSOLUTTIME": "03:57.002",               "BESTTIME": "19.640",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "",               "COLOR": 1,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-2",               "DELAYTIMEPREVIOUS": "-1",               "FORECAST": "14 05:03.731",               "INDEX": 3,               "LAPINFO": "",               "LAPS": 11,               "LAPTIME": "24.766",               "MEDIUMTIME": "21.545",               "PILOT": "Tony RC",               "PILOTNUMBER": 0,               "PROGRESS": 90,               "SPEED": "21,95",               "STANDARDDEVIATION": "2.369",               "TEMPERATUR": "20 °C",               "TRANSPONDER": "2398220",               "TREND": -1,               "VEHICLE": 4,               "VOLTAGE": "6,9 V"           },           {               "ABSOLUTTIME": "04:06.838",               "BESTTIME": "20.852",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "",               "COLOR": 7,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-2",               "DELAYTIMEPREVIOUS": "+9.836",               "FORECAST": "14 05:14.092",               "INDEX": 4,               "LAPINFO": "",               "LAPS": 11,               "LAPTIME": "21.173",               "MEDIUMTIME": "22.439",               "PILOT": "Clarhaut Vincnnnnnnnnnnnnnnnnnent",               "PILOTNUMBER": 0,               "PROGRESS": 51,               "SPEED": "25,67",               "STANDARDDEVIATION": "1.954",               "TEMPERATUR": "11 °C",               "TRANSPONDER": "8926221",               "TREND": 1,               "VEHICLE": 3,               "VOLTAGE": "7,1 V"           },           {               "ABSOLUTTIME": "04:08.981",               "BESTTIME": "22.157",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "1176",               "COLOR": 7,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-3",               "DELAYTIMEPREVIOUS": "-1",               "FORECAST": "13 05:24.275",               "INDEX": 5,               "LAPINFO": "",               "LAPS": 10,               "LAPTIME": "23.243",               "MEDIUMTIME": "24.898",               "PILOT": "domis fabien",               "PILOTNUMBER": 0,               "PROGRESS": 20,               "SPEED": "23,39",               "STANDARDDEVIATION": "2.735",               "TEMPERATUR": "15 °C",               "TRANSPONDER": "3567179",               "TREND": 1,               "VEHICLE": 6,               "VOLTAGE": "5,8 V"           },           {               "ABSOLUTTIME": "03:45.304",               "BESTTIME": "25.920",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "Rc park",               "COLOR": 1,               "COUNTRY": "BEL",               "DELAYTIMEFIRST": "-5",               "DELAYTIMEPREVIOUS": "-2",               "FORECAST": "10 05:08.071",               "INDEX": 6,               "LAPINFO": "",               "LAPS": 8,               "LAPTIME": "27.370",               "MEDIUMTIME": "28.163",               "PILOT": "BILLE eddy",               "PILOTNUMBER": 0,               "PROGRESS": 100,               "SPEED": "19,86",               "STANDARDDEVIATION": "2.555",               "TEMPERATUR": "6 °C",               "TRANSPONDER": "3830740",               "TREND": -1,               "VEHICLE": 5,               "VOLTAGE": "6,0 V"           }       ],       "KEY": "B18D6AD15E176B658F02",       "METADATA": {           "COUNTDOWN": "00:00:00",           "CURRENTTIME": "00:04:14",           "DIVERGENCE": "00:00:00",           "GROUP": "101 :: Qualification :: Série 1 - Heat 1",           "NAME": "TONY RC MEETING",           "RACETIME": "00:05:00",           "REMAININGTIME": "00:00:46",           "SECTION": "RC PARK 1/10 TT 4X2 OPEN  [101]"       },       "TIMESTAMP": "1345831324",       "VERSION": "1.0"   }}'

while (True):
    try:
        if not LocalOnly:
            response = requests.get("http://192.168.0.176/1/StreamingData").text
        js = json.loads(response)
    except ConnectionError:
        print("Cannot reach publisher server")
        continue

         
    #'{"EVENT":{"VERSION":"1.0","KEY":"B18D6AD1BA680B650A03","TIMESTAMP":"16354661","CONFIG":{"MODE":"LapAndTime","NROFBESTLAPS":0},"METADATA":{"NAME":"Course #5 Amicale - RC PARK","SECTION":"RC PARK 1\/10 TT 4X2 13.5T   [100]","GROUP":"100 :: Finale :: Finale B - Heat 3","RACETIME":"00:05:00","CURRENTTIME":"00:00:55","REMAININGTIME":"00:04:05","COUNTDOWN":"00:00:00","DIVERGENCE":"00:00:00"},"DATA":[]}}'
    #print(response.text)
    
    #js = json.loads('{"EVENT":{"VERSION":"1.0","KEY":"B18D6AD1BA680B650A03","TIMESTAMP":"16354661","CONFIG":{"MODE":"LapAndTime","NROFBESTLAPS":0},"METADATA":{"NAME":"Course #5 Amicale - RC PARK","SECTION":"RC PARK 1\/10 TT 4X2 13.5T   [100]","GROUP":"100 :: Finale :: Finale B - Heat 3","RACETIME":"00:05:00","CURRENTTIME":"00:00:55","REMAININGTIME":"00:04:05","COUNTDOWN":"00:00:00","DIVERGENCE":"00:00:00"},"DATA":[]}}')
    
    # js = json.loads('{   "EVENT": {       "CONFIG": {           "MODE": "LapAndTime",           "NROFBESTLAPS": 0       },       "DATA": [           {               "ABSOLUTTIME": "04:21.095",               "BESTTIME": "19.212",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "BRCA",               "COLOR": 2,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "0.000",               "DELAYTIMEPREVIOUS": "0.000",               "FORECAST": "15 05:03.003",               "INDEX": 1,               "LAPINFO": "",               "LAPS": 13,               "LAPTIME": "20.030",               "MEDIUMTIME": "20.084",               "PILOT": "Boda Clément",               "PILOTNUMBER": 0,               "PROGRESS": 0,               "SPEED": "27,14",               "STANDARDDEVIATION": "1.077",               "TEMPERATUR": "20 °C",               "TRANSPONDER": "9666194",               "TREND": 1,               "VEHICLE": 1,               "VOLTAGE": "5,7 V"           },           {               "ABSOLUTTIME": "04:17.567",               "BESTTIME": "19.351",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "880",               "COLOR": 7,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-1",               "DELAYTIMEPREVIOUS": "-1",               "FORECAST": "14 05:01.595",               "INDEX": 2,               "LAPINFO": "",               "LAPS": 12,               "LAPTIME": "25.779",               "MEDIUMTIME": "21.463",               "PILOT": "Vandenberghe Davidddddddddddddddddd",               "PILOTNUMBER": 0,               "PROGRESS": 6,               "SPEED": "21,09",               "STANDARDDEVIATION": "2.115",               "TEMPERATUR": "12 °C",               "TRANSPONDER": "2857229",               "TREND": -1,               "VEHICLE": 2,               "VOLTAGE": "5,7 V"           },           {               "ABSOLUTTIME": "03:57.002",               "BESTTIME": "19.640",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "",               "COLOR": 1,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-2",               "DELAYTIMEPREVIOUS": "-1",               "FORECAST": "14 05:03.731",               "INDEX": 3,               "LAPINFO": "",               "LAPS": 11,               "LAPTIME": "24.766",               "MEDIUMTIME": "21.545",               "PILOT": "Tony RC",               "PILOTNUMBER": 0,               "PROGRESS": 90,               "SPEED": "21,95",               "STANDARDDEVIATION": "2.369",               "TEMPERATUR": "20 °C",               "TRANSPONDER": "2398220",               "TREND": -1,               "VEHICLE": 4,               "VOLTAGE": "6,9 V"           },           {               "ABSOLUTTIME": "04:06.838",               "BESTTIME": "20.852",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "",               "COLOR": 7,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-2",               "DELAYTIMEPREVIOUS": "+9.836",               "FORECAST": "14 05:14.092",               "INDEX": 4,               "LAPINFO": "",               "LAPS": 11,               "LAPTIME": "21.173",               "MEDIUMTIME": "22.439",               "PILOT": "Clarhaut Vincnnnnnnnnnnnnnnnnnent",               "PILOTNUMBER": 0,               "PROGRESS": 51,               "SPEED": "25,67",               "STANDARDDEVIATION": "1.954",               "TEMPERATUR": "11 °C",               "TRANSPONDER": "8926221",               "TREND": 1,               "VEHICLE": 3,               "VOLTAGE": "7,1 V"           },           {               "ABSOLUTTIME": "04:08.981",               "BESTTIME": "22.157",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "1176",               "COLOR": 7,               "COUNTRY": "FRA",               "DELAYTIMEFIRST": "-3",               "DELAYTIMEPREVIOUS": "-1",               "FORECAST": "13 05:24.275",               "INDEX": 5,               "LAPINFO": "",               "LAPS": 10,               "LAPTIME": "23.243",               "MEDIUMTIME": "24.898",               "PILOT": "domis fabien",               "PILOTNUMBER": 0,               "PROGRESS": 20,               "SPEED": "23,39",               "STANDARDDEVIATION": "2.735",               "TEMPERATUR": "15 °C",               "TRANSPONDER": "3567179",               "TREND": 1,               "VEHICLE": 6,               "VOLTAGE": "5,8 V"           },           {               "ABSOLUTTIME": "03:45.304",               "BESTTIME": "25.920",               "BESTTIMEN": "0.000",               "CARID": 0,               "CLUB": "Rc park",               "COLOR": 1,               "COUNTRY": "BEL",               "DELAYTIMEFIRST": "-5",               "DELAYTIMEPREVIOUS": "-2",               "FORECAST": "10 05:08.071",               "INDEX": 6,               "LAPINFO": "",               "LAPS": 8,               "LAPTIME": "27.370",               "MEDIUMTIME": "28.163",               "PILOT": "BILLE eddy",               "PILOTNUMBER": 0,               "PROGRESS": 100,               "SPEED": "19,86",               "STANDARDDEVIATION": "2.555",               "TEMPERATUR": "6 °C",               "TRANSPONDER": "3830740",               "TREND": -1,               "VEHICLE": 5,               "VOLTAGE": "6,0 V"           }       ],       "KEY": "B18D6AD15E176B658F02",       "METADATA": {           "COUNTDOWN": "00:00:00",           "CURRENTTIME": "00:04:14",           "DIVERGENCE": "00:00:00",           "GROUP": "101 :: Qualification :: Série 1 - Heat 1",           "NAME": "TONY RC MEETING",           "RACETIME": "00:05:00",           "REMAININGTIME": "00:00:46",           "SECTION": "RC PARK 1/10 TT 4X2 OPEN  [101]"       },       "TIMESTAMP": "1345831324",       "VERSION": "1.0"   }}')
    
    
    
    ''' 
    GESTION DES CATEGORIES
    '''  
    round = js['EVENT']['METADATA']['SECTION']+js['EVENT']['METADATA']['GROUP']
    #"RC PARK 1/10 TT 4X2 MOD [101] / Série 1 / Qualification 1"    
    print(f"Manche en cours : {round}")
    # RC PARK 1/10 TT 4X2 OPEN  [101]101 :: Qualification :: Série 1 - Heat 1
    
    positionslash = round.find(" :: ")
    serie = round[positionslash:]
    print(f"Serie en cours : {serie}")

    RoundDict = {
        "100" : "4x2 Standard",
        "101" : "4x2 Modifié",
        "102" : "4xd Modifié",
        "103" : "Truck",
        "104" : "Vintage",
        "105" : "Rookie",
        "Online" : "4x0 Test"
                 }
    
    
    fichier_source =""
    if "[104]" in round:
        texte = round
        round_pretty = "Vintage "
    elif "[100]" in round:
        texte = round
        round_pretty = "4x2 Standard "
    elif "[101]" in round:
        texte = round
        round_pretty = "4x2 Modifié "
    elif "[102]" in round:
        texte = round
        round_pretty = "4x4 Modifié "
    elif "[105]" in round:
        texte = round
        round_pretty = "Rookie "
    elif "[103]" in round:
        texte = round
        round_pretty = "Truck "    
    elif "[Online]" in round:     
        texte = round
        round_pretty = "4x0 Test"     
    else : 
        texte = "Manche Non reconnue"
        round_pretty= "Manche non reconnue"
        
    round_pretty = round_pretty + serie.replace("::","")
    print(round_pretty)
    
    
    
    
    '''Gestion du TEMPS Restant'''

    
    RaceTime = str(js['EVENT']['METADATA'
                      ]['CURRENTTIME'][3:])+" / "+str(js['EVENT']['METADATA']['RACETIME'][3:])
    
    # temps = str(random.randint(1, 5)).zfill(2)+":"+str(random.randint(1,59)).zfill(2)+" / 05:00"
    
    print(RaceTime)

    
    
    
        
    
    ''' GESTION DU FICHIER Tableau.html '''
    NbPilote = len(js['EVENT']['DATA'])
    print("Nbre Pilote " + str(NbPilote))
    #print(js['EVENT']['DATA'][0])
    
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



    for i in range(NbPilote):
        data = js['EVENT']['DATA'][i]
        
        pilotes.append({"Pos":js['EVENT']['DATA'][i]['INDEX'],
                         "Car":js['EVENT']['DATA'][i]['VEHICLE'],
                         "PrenomNom":js['EVENT']['DATA'][i]['PILOT']
                         })
        texte += ""+str(js['EVENT']['DATA'][i]['INDEX']) + ". -" + str(js['EVENT']['DATA'][i]['VEHICLE'])+ "- L"+str(js['EVENT']['DATA'][i]['LAPS'])+" "+js['EVENT']['DATA'][i]['PILOT'].title()+ "\n"

        htmlpilote = '<tr>'
        htmlpilote += '<td>'+str(js['EVENT']['DATA'][i]['INDEX'])+'</td>' #POSITION
        htmlpilote += '<td>'+str(js['EVENT']['DATA'][i]['VEHICLE'])+'</td>' #NUMERO VOITURE
        htmlpilote += '<td>'+str(js['EVENT']['DATA'][i]['PILOT'].upper())+'</td>' #NOM PILOTE
        htmlpilote += '<td>'+str(js['EVENT']['DATA'][i]['LAPS'])+'</td>' #NOMBRE DE TOUR
        htmlpilote += '<td>'+str(js['EVENT']['DATA'][i]['LAPTIME'])+'</td>' #TEMPS
        htmlpilote += '</tr>'

        htmlbody += htmlpilote
    
    htmlbody += '</tbody></table></body>'
    htmlbody += '</html>'

    try:
        #Save round file
        with open(roundFilePath, 'w',encoding='utf-8') as file:
            file.write(round_pretty)
        
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