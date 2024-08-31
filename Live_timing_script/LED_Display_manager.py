import json
import requests
import time
import re
import datetime
from random import randint
from pathlib import Path
import pandas as pd

class Pilot:
    def __init__(self, **kwargs):
        self.positionChangeTimer = 0
        self.newBestTimer = 0
        self.previousPosition = -1
        self.previousVehicle = -1
        self.pace_5m = 0
        self.pace_1h = 0
        self.newBestHoldTime = 0
        self.newPositionHoldTime = 2
        self.update(0, **kwargs)

    def update(self, position, **kwargs):
        self.absoluttime =      kwargs.get('ABSOLUTTIME', None)
        self.besttime =         kwargs.get('BESTTIME', None)
        self.besttimen =        kwargs.get('BESTTIMEN', None)
        self.carid =            kwargs.get('CARID', None)
        self.club =             kwargs.get('CLUB', None)
        self.color =            kwargs.get('COLOR', None)
        self.country =          kwargs.get('COUNTRY', None)
        self.delaytimefirst =   kwargs.get('DELAYTIMEFIRST', None)
        self.delaytimeprevious = kwargs.get('DELAYTIMEPREVIOUS', None)
        self.forecast =         kwargs.get('FORECAST', None)
        self.forecast_short =   self.forecast.split(" ")[0]
        self.index =            kwargs.get('INDEX', None)
        self.laps =             kwargs.get('LAPS', None)
        self.laptime =          kwargs.get('LAPTIME', None)
        self.mediumtime =       kwargs.get('MEDIUMTIME', None)
        self.pilot =            kwargs.get('PILOT', None)
        self.pilotnumber =      kwargs.get('PILOTNUMBER', None)
        self.progress =         kwargs.get('PROGRESS', None)
        self.speed =            kwargs.get('SPEED', None)
        self.standarddeviation = kwargs.get('STANDARDDEVIATION', None)
        self.temperature =      kwargs.get('TEMPERATUR', None)
        self.transponder =      kwargs.get('TRANSPONDER', None)
        self.trend =            kwargs.get('TREND', None)
        self.vehicle =          kwargs.get('VEHICLE', None)
        self.voltage =          kwargs.get('VOLTAGE', None)
        self.position = position
        self.updateTime()

        self.newBest = self.laptime_s==self.besttime_s

        if self.vehicle != self.previousVehicle :
            self.positionChangeTimer = time.time()
        self.previousVehicle = self.vehicle
        self.newPosition = (self.positionChangeTimer + self.newPositionHoldTime) > time.time()

    
    def updateTime(self):
        try:
            self.besttime_s = float(self.besttime)
            self.besttimen_s = float(self.besttimen)
            self.laptime_s = float(self.laptime)
            self.mediumtime_s = float(self.mediumtime)
            # m, s = map(float, str(self.absoluttime).split(":"))
            # s = int(s)
            # self.absoluttime_s = datetime.timedelta(minutes=m, seconds=float(s))
        except ValueError as e:
            print(f"ParseError: {e}")

class Round:
    RoundDict = {
        "100" : "4x2 Standard",
        "101" : "4x2 Modifié",
        "102" : "4xd Modifié",
        "103" : "Truck",
        "104" : "Vintage",
        "105" : "Rookie",
        "TT10 EL 4x2 STD CF" : "4x2 Standard",
        "TT10 EL 4x2 MOD CF" : "4x2 Modifié",
        "TT10 EL 4x4 MOD CF" : "4x4 Modifié",
        "TT10 EL TR CF" : "Truck",
        "Online" : "4x0 Test",
        "EFRA 10 MOD" : "EFRA 1/10E Modified",
        "EFRA 10 FRONTI" : "EFRA 1/10E Fronti",
        "EFRA 10 SPEC" : "EFRA 1/10E Stock"
                 }
    
    def __init__(self, **kwargs):
        self.pilotList = [Pilot(**pilot) for pilot in kwargs['DATA']]
        self.NewLap = []
        self.update(**kwargs)
        
    def update(self, bypassLapDetect=False, **kwargs):
        self.countdown =        kwargs['METADATA'].get('COUNTDOWN', None)
        self.currenttime =      kwargs['METADATA'].get('CURRENTTIME', None)
        self.divergence =       kwargs['METADATA'].get('DIVERGENCE', None)
        self.group =            kwargs['METADATA'].get('GROUP', None)
        self.name =             kwargs['METADATA'].get('NAME', None)
        self.racetime =         kwargs['METADATA'].get('RACETIME', None)
        self.remainingtime =    kwargs['METADATA'].get('REMAININGTIME', None)
        self.section =          kwargs['METADATA'].get('SECTION', None)
        self.verbose = False
        self.updateRaceTime(randomize=False)
        self.updatePilotList(kwargs['DATA'])
        self.parseCategory()
    
    def ReloadDataFramesFromFile(self, BasePath):
        for pilot in self.pilotList:
            try:
                df = pd.read_csv(Path(BasePath, pilot.pilot+".csv"))
            except FileNotFoundError:
                print(f"Failed to reload from file for {pilot.pilot}. Fresh start.")
        
    def getPace(self, pilotkey, period, timeCol="RaceTime_s", valueCol="Laps"):
        try:
            for d in self.PilotDataFrameDict[pilotkey].rolling(window=period, on=timeCol, min_periods=1):
                pass
            return d[valueCol].iloc[-1] - d[valueCol].iloc[0]
        except ValueError as e:
            print(f"Failed getting Pace: {e}")
        except KeyError as e:
            print(f"Failed getting Pace: {e}")
        return 0

    def updateRaceTime(self, randomize=False):
        h, m, s = map(int, str(self.racetime).split(":"))
        self.racetime_s = datetime.timedelta(hours=h, minutes=m, seconds=s)
        self.racetime_s_float = self.racetime_s.total_seconds()
        h, m, s = map(int, str(self.remainingtime).split(":"))
        self.remainingtime = datetime.timedelta(hours=h, minutes=m, seconds=s) + datetime.timedelta(seconds=randint(1,60))*randomize
        

    def getRaceTime_pretty(self):
        #returns a pretty string of the current race time
        if self.racetime_s.seconds>3600:
            return f"{self.remainingtime} / {self.racetime_s}"
        else:
            return f"{str(self.remainingtime)[-5:]} / {str(self.racetime_s)[-5:]}"
    
    def parseCategory(self):
        self.roundData = f"{self.section}{self.group}"
        try:
            categoryMatch = re.findall(pattern="\[(.*)\].*?::(.*)", string=self.roundData)
            catNumber = categoryMatch[0][0]
            serie = categoryMatch[0][1:][0].replace("::","-")
            tempserie = serie.split("-")
            self.round_pretty = f"{self.RoundDict[catNumber]}\n{tempserie[0].strip()}\n{tempserie[1].strip()} - {tempserie[2].strip()}"
            self.category_pretty = f"{self.RoundDict[catNumber]}"
            self.serie_pretty = f"{tempserie[0].strip()} - {tempserie[1].strip()} - {tempserie[2].strip()}"
            self.SerieNumber = tempserie[1].strip()[-1]

        except IndexError:
            print("Error parsing category")
            self.round_pretty = "Manche non reconnue"
            self.category_pretty = "Manche non reconnue"
            self.serie_pretty = "Manche non reconnue"
        except KeyError:
            self.round_pretty = "Manche non reconnue"
            self.category_pretty = "Manche non reconnue"
            self.serie_pretty = "Manche non reconnue"
            
        if self.verbose:
            print(f"Manche en cours : {self.roundData} ==> {self.round_pretty}")
    
    def updatePilotList(self, data:list):

        try:
            self.numberOfPilots = len(data)
            for i, pilot in enumerate(data):
                self.pilotList[i].update(i, **pilot)
        except IndexError:
            print("Error updating pilot list.")



LocalOnly = True
UseWebSocket = False

PublisherServer_IP = "192.168.1.136"

# from displayDriver import Display
# disp = Display(numberOfLines=3, Port="/dev/ttyS0")

index = 0
with open("jsontemplate.txt", 'r', encoding="utf-8") as timefile:
    InputTestFile = timefile.readlines()
response = InputTestFile[0]
Tstart = time.time()

newRound = False
PreviousGroup = None
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
            #print(response)
        js = json.loads(response)
    except ConnectionError:
        print("Cannot reach publisher server")
        continue

    # Check if we entered a new round to create new pilot list
    currentGroup = js['EVENT']['METADATA']['SECTION']+js['EVENT']['METADATA']['GROUP']

    if PreviousGroup != currentGroup:
        PreviousGroup = currentGroup
        currentRound = Round(**js['EVENT'])
        newRound = True
    else:
        newRound = False
        currentRound.update(**js['EVENT'])

    print(f"Current round = {currentRound.round_pretty}")
    print(f"RaceTime = {currentRound.getRaceTime_pretty()}")

    # PilotsToBeDisplayed = [f"{pilot.vehicle:02d}-{pilot.besttime_s:05.2f}-{pilot.laps:04d}" for pilot in currentRound.pilotList[:disp.numberOfLines]]

    # if len(currentRound.pilotList)>=disp.numberOfLines: 
    #     disp.setLines(PilotsToBeDisplayed)
    #     disp.updateDisplay()


    time.sleep(5)


