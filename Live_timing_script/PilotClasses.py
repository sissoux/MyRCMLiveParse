class Pilot:
    def __init__(self, **kwargs):
        self.update(**kwargs)

    def update(self, **kwargs):
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

class Round:
    def __init__(self, **kwargs):
        self.countdown =        kwargs['METADATA'].get('COUNTDOWN', None)
        self.currenttime =      kwargs['METADATA'].get('CURRENTTIME', None)
        self.divergence =       kwargs['METADATA'].get('DIVERGENCE', None)
        self.group =            kwargs['METADATA'].get('GROUP', None)
        self.name =             kwargs['METADATA'].get('NAME', None)
        self.racetime =         kwargs['METADATA'].get('RACETIME', None)
        self.remainingtime =    kwargs['METADATA'].get('REMAININGTIME', None)
        self.section =          kwargs['METADATA'].get('SECTION', None)
        self.pilotList = [Pilot(**pilot) for pilot in kwargs['DATA']]
    
    def updatePilotList(self, data:list):
        for i, pilot in enumerate(data):
            self.pilotList[i].update(**pilot)
