from enum import StrEnum

class TeamNames(StrEnum):
    TeamRocket = "Rocket"
    TiBolid = "pouet"

for team in TeamNames:
    print(team)


class scene():
    def __init__(self, name:str, minTime:int=None, maxTime:int=None, autoSwitch=True) -> None:
        self.name = name
        self.minTime = minTime
        self.maxTime = maxTime
        self.allowedAutoSwitch = autoSwitch

SceneList = {
    "Podium"            :scene("Podium", 2, 6), 
    "Comptage"          :scene("Comptage", 30, 75), 
    "Table"             :scene("Table", 30,75), 
    "SerieDisplay"      :scene("SerieDisplay", autoSwitch=False),
    "StatisticsDisplay" :scene("StatisticsDisplay", autoSwitch=False)
}
autoSceneList = [value[1] for value in SceneList.items() if value[1].allowedAutoSwitch]
for s in SceneList:
    print(SceneList[s].name)

for s in autoSceneList:
    print(s.name)