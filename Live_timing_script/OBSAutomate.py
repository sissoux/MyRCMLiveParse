import obsws_python as obs
import time
import random

class scene():
    def __init__(self, name:str, minTime:int=None, maxTime:int=None, autoSwitch=True) -> None:
        self.name = name
        self.minTime = minTime
        self.maxTime = maxTime
        self.allowedAutoSwitch = autoSwitch
    
    def getDelay(self):
        return random.randint(self.minTime,self.maxTime)

class OBS_Auto():
    SceneList = {
        "Podium"            :scene("Podium", 2, 6), 
        "Comptage"          :scene("Comptage", 30, 75), 
        "Table"             :scene("Table", 30,75), 
        "SerieDisplay"      :scene("SerieDisplay", autoSwitch=False),
        "StatisticsDisplay" :scene("StatisticsDisplay", autoSwitch=False)
    }
    autoSceneList = [value[1] for value in SceneList.items() if value[1].allowedAutoSwitch]


    def __init__(self, IP, PassWord, Port=4455) -> None:
        self.wsHhost = IP
        self.wsPort = Port
        self.wsPW = PassWord

    def connect(self):
        self.OBS = obs.ReqClient(host=self.wsHhost, port=self.wsPort, password=self.wsPW, timeout=3)

    def initialize(self):
        self.previousTime = time.time()
        self.sceneDelay = 0
        self.init = True
        self.preventPodium = False
        self.toScene = None
        self.autoSwitchEnabled = False
        self.preventPodium = True

    def setScene(self, scene:scene):
        try:
            self.OBS.set_current_program_scene(self.toScene.name)
        except:
            print("Failed switching scene")


    def updateScene(self, ForceScene=None):
        if (time.time() - self.previousTime > self.AutoSwitchDelay and self.autoSwitchEnabled) or (ForceScene is not None):
            self.previousTime = time.time()
            self.fromScene = self.toScene
            if ForceScene is not None:
                self.toScene = ForceScene
            else:
                self.toScene = self.autoSceneList[random.randint(1*self.preventPodium,len(self.autoSceneList))]
            self.setScene(self.toScene)
            self.AutoSwitchDelay = scene.getDelay()

    def showStatistics(self, duration):
        self.updateScene(ForceScene=)
        pass

