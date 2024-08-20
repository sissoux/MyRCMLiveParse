from OBSAutomate import OBS_Auto
import secret
import time

OBS = OBS_Auto(IP = 'localhost', Port=4455, PassWord=secret.OBSWebSocketPW, verbose=True, debug=False)

FullStatShowPeriod = 30
ShowFullStat = False

StatShowTimer = time.time()

while True:
    if time.time() - StatShowTimer > FullStatShowPeriod and ShowFullStat:
        StatShowTimer = time.time()
        OBS.showStatistics(20)
    else:
        OBS.updateScene()



