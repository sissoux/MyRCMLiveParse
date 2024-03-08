# from obswebsocket import obsws, requests
import secret
import time
import obsws_python as obs

wsHhost = 'localhost'
wsPort = 4455
wsPW = secret.WebsocketPW

# pass conn info if not in config.toml
cl = obs.ReqClient(host='localhost', port=4455, password='mystrongpass', timeout=3)
# OBS_client = obsws(host=wsHhost, port=wsPort, password=wsPW)

# cl.get

# OBS_client.connect()
# Scenes = OBS_client.call(requests.GetSceneList())
# for s in Scenes:
#     print(s)

# print(OBS_client.call(requests.GetVersion()).getObsVersion())
# print(OBS_client.call(requests.GetSceneList()).Get())
# time.sleep(3)
# OBS_client.disconnect()