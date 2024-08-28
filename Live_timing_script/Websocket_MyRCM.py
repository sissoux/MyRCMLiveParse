import asyncio
import ssl
import websockets
import json 



async def WSconnect_MyRCM():
    # Créer un contexte SSL qui ignore la validation des certificats
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Connecter au WebSocket
    async with websockets.connect('wss://www.myrcm.ch/myrcm/websocket', ssl=ssl_context) as websocket:
        print("connected")
        '''message = {
            "message": "Hello WebSocket!"
        }
        # Convertir l'objet JSON en chaîne de caractères
        await websocket.send(json.dumps(message))
        
        response = await websocket.recv()
        print(f"Réponse du serveur : {response}")'''
       
        await websocket.send("{\"EventKey\":\"80751\",\"Language\":\"-\",\"Format\":\"JSON\"}")
        response = await websocket.recv()
        response = await websocket.recv()
        #print(f"Réponse du serveur : {response}")
        return response

def get_websocket_response():
    return asyncio.run(WSconnect_MyRCM())