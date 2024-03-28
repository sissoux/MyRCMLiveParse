# from obswebsocket import obsws, requests
import secret
import time
import obsws_python as obs

wsHhost = '192.168.0.15'
wsPort = 4455
wsPW = secret.WebsocketPW

# pass conn info if not in config.toml
OBS = obs.ReqClient(host='localhost', port=4455, password=wsPW, timeout=3)
# resp = cl.get_version()
# print(f"OBS Version: {resp.obs_version}")
OBS.set_current_program_scene("Table")

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