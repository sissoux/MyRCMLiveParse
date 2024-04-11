import re
import time
import datetime
from random import randint
from pathlib import Path
from enum import StrEnum
import pandas as pd
from copy import deepcopy

class Teams():
    class Names(StrEnum):
        rocket = "Rocket"
        aliExpress = "Team Ali Express"
        cingles = "Les Cinglés"
        tiBolid = "TI'BOLID Revival"
        diabolo = "Team DIA BOLO"

    TeamDict = {
        "4813580" : Names.rocket,
        "1056266" : Names.aliExpress,
        "8682086" : Names.cingles,
        "2567134" : Names.tiBolid,
        "3109958" : Names.diabolo   
    }
    
    # Best / avg / laps / pace on 5 min / logo / photo voiture / pace 1h / forecast / avg pit stop time


class Pilot:
    def __init__(self, **kwargs):
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
        self.pace_5m = 0
        self.pace_1h = 0
        self.updateTime()

    def fillDataFrame(self, RaceTime, inputdf=None)->pd.DataFrame:
        df = pd.DataFrame({
                            'ABSOLUTTIME'       :self.absoluttime,
                            'BESTTIME'          :self.besttime,
                            'BESTTIMEN'         :self.besttimen,
                            'LAPS'              :self.laps,
                            'LAPTIME'           :self.laptime,
                            'MEDIUMTIME'        :self.mediumtime,
                            'PILOT'             :self.pilot,
                            'PILOTNUMBER'       :self.pilotnumber,
                            'FORECAST'          :self.forecast,
                            'PROGRESS'          :self.progress,
                            'STANDARDDEVIATION' :self.standarddeviation,
                            'TRANSPONDER'       :self.transponder,
                            'VEHICLE'           :self.vehicle,
                            'TEMPERATUR'        :self.temperature,
                            'RACETIME'          :RaceTime
                        }, index=[0]) 
        if inputdf is not None:
            return pd.concat([inputdf, df])
        else:
            return df

    
    def updateTime(self):
        try:
            self.besttime_s = float(self.besttime)
            self.besttimen_s = float(self.besttimen)
            self.laptime_s = float(self.laptime)
            self.mediumtime_s = float(self.mediumtime)
            m, s = map(float, str(self.absoluttime).split(":"))
            s = int(s)
            self.absoluttime_s = datetime.timedelta(minutes=m, seconds=float(s))
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
        "Online" : "4x0 Test"
                 }
    
    FileDictionnary = {
        "TT10 EL 4x2 STD CF" : "Qual-42S-S",
        "TT10 EL 4x2 MOD CF" : "Qual-42M-S",
        "TT10 EL 4x4 MOD CF" : "Qual-44M-S",
        "TT10 EL TR CF" : "Qual-TRK-S"
    }

    FinaleFileDictionnary={
        "TT10 EL 4x2 STD CF" : "42S.Final-",
        "TT10 EL 4x2 MOD CF" : "42M.Final-",
        "TT10 EL 4x4 MOD CF" : "44M.Final-",
        "TT10 EL TR CF" : "TRK.Final-"
    }
    
    def __init__(self, **kwargs):
        self.pilotList = [Pilot(**pilot) for pilot in kwargs['DATA']]
        self.PilotDataFrameDict = {pilot.pilot:pd.DataFrame() for pilot in self.pilotList}
        self.CurrentPilotDict = None
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
        self.PreviousPilotDict = deepcopy(self.CurrentPilotDict)
        self.CurrentPilotDict = {pilot.pilot:pilot for pilot in self.pilotList}
        if self.PreviousPilotDict is not None:
            for pilotKey in self.CurrentPilotDict:
                if self.PreviousPilotDict[pilotKey].laps != self.CurrentPilotDict[pilotKey].laps or bypassLapDetect:
                    self.NewLap.append(pilotKey)
                    print(f"Detected new lap for {pilotKey}, Adding data into dataframe")
                    self.PilotDataFrameDict[pilotKey] = self.CurrentPilotDict[pilotKey].fillDataFrame(inputdf=self.PilotDataFrameDict[pilotKey], RaceTime=self.racetime_s)
                    # print(self.PilotDataFrameDict[pilotKey])
                    self.CurrentPilotDict[pilotKey].pace_5m = self.getPace(pilotKey, period="40s", valueCol="LAPS", timeCol="RACETIME")
                    self.CurrentPilotDict[pilotKey].pace_1h = self.getPace(pilotKey, period="1h", valueCol="LAPS", timeCol="RACETIME")
                # print(f"{pilotKey} --> {self.CurrentPilotDict[pilotKey].laps} / {self.PreviousPilotDict[pilotKey].laps}")

        
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
            self.SerieNumber = tempserie[1].strip()[-1]

            if self.SerieNumber.isnumeric():
                self.picPath = Path("QUALIF_HD", self.FileDictionnary[catNumber]+self.SerieNumber+".jpg" )
                self.bannerPath = Path("QUALIF_HD", "bandeau", "bandeau"+self.FileDictionnary[catNumber]+self.SerieNumber+".jpg" )
                print(self.picPath)
            else:
                self.picPath = Path("FINALES_HD", self.FinaleFileDictionnary[catNumber]+self.SerieNumber+".jpg" )
                self.bannerPath = Path("FINALES_HD", "bandeau", "bandeau"+self.FinaleFileDictionnary[catNumber]+self.SerieNumber+".jpg" )
                print(self.picPath)
                print(self.bannerPath)



        except IndexError:
            print("Error parsing category")
            self.round_pretty = "Manche non reconnue"
        except KeyError:
            self.round_pretty = "Manche non reconnue"
        if self.verbose:
            print(f"Manche en cours : {self.roundData} ==> {self.round_pretty}")
    
    def updatePilotList(self, data:list):
        try:
            self.numberOfPilots = len(data)
            for i, pilot in enumerate(data):
                self.pilotList[i].update(i, **pilot)
        except IndexError:
            print("Error updating pilot list.")
