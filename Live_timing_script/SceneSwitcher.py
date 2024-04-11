from OBSAutomate import OBS_Auto
import secret
import time

OBS = OBS_Auto(IP = 'localhost', Port=4455, PassWord=secret.OBSWebSocketPW, verbose=True, debug=True)

FullStatShowPeriod = 30

StatShowTimer = time.time()

while True:
    if time.time() - StatShowTimer > FullStatShowPeriod:
        StatShowTimer = time.time()
        OBS.showStatistics(20)
    else:
        OBS.updateScene()



