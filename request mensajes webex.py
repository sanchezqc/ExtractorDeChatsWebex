import requests
import json
from types import SimpleNamespace

def procesarTexto(mensaje):
    #intenta sacar el texto de un mensaje
    try:
        return mensaje.text
    except:
        return ""

def procesarAdjunto(mensaje):
    #intenta sacar el texto de un mensaje
    try:
        return mensaje.files
    except:
        return ""    

headers = {"Authorization": "Bearer ODFlNjVlNTQtZWZhNS00YTlkLWEzNmYtNTQ4ZDg4YmJlYzNkMTY5NWRiNDYtZTMz_PF84_60368964-7735-4a19-94f7-b83594f8e2e7"}
data = {}
def ejecutar():
    endpointSalas = "https://webexapis.com/v1/rooms"
    a = requests.get(endpointSalas, data=data, headers=headers)
    #salas = a.json()
    x = json.loads(a.text, object_hook=lambda d: SimpleNamespace(**d))
    print(x.items)
    for cadaChat in x.items:
        print("chat con ", cadaChat.title)
        endpointMensajes = "https://webexapis.com/v1/messages?" + "roomId=" + str(cadaChat.id)
        #print(endpointMensajes)
        msjs = requests.get(endpointMensajes, data=data, headers=headers)
        y = json.loads(msjs.text, object_hook=lambda d: SimpleNamespace(**d))
        #print(y.items)
        for cadaMensaje in y.items:
            #print(cadaMensaje)
            mensajeComoTexto = procesarTexto(cadaMensaje)
            if mensajeComoTexto:
                print("[",cadaMensaje.created,"] =>", cadaMensaje.personEmail, "dice: ", mensajeComoTexto )
            else:
                mensajeComoAdjunto =procesarAdjunto(cadaMensaje)
                if mensajeComoAdjunto:
                    print("Se encontró un adjunto: ", mensajeComoAdjunto)
                    #endpointAdjuntos =mensajeComoAdjunto
                    #adjuntos = requests.get(endpointAdjuntos, data=data, headers=headers)
                    #print(adjuntos)

ejecutar()

