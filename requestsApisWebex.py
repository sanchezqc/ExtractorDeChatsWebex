import requests
import json
from types import SimpleNamespace
import BaseDeDatos as bd

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

def crearSalas(tokenBearer):
    if(tokenBearer!= ""):
        headers = {"Authorization": "Bearer "+ tokenBearer}
        data = {}
        endpointSalas = "https://webexapis.com/v1/rooms"
        resultadoSalasW = requests.get(endpointSalas, data=data, headers=headers)
        resultadoComoObjetoSalas = json.loads(resultadoSalasW.text, object_hook=lambda d: SimpleNamespace(**d))
        #print(resultadoComoObjetoSalas.items)
        for cadaSala in resultadoComoObjetoSalas.items:
                bd.insertarSala(cadaSala.id, cadaSala.title)

def crearMensajes(tokenBearer):
    if(tokenBearer!= ""):
        headers = {"Authorization": "Bearer "+ tokenBearer}
        data = {}
        listaDeSalas = bd.ObtenerSalas()
        for cadaSala in listaDeSalas:
            #print(cadaSala[0], cadaSala[1])
            idSala = cadaSala[0]
            endpointMensajes = "https://webexapis.com/v1/messages?" + "roomId=" + str(idSala)
            msjs = requests.get(endpointMensajes, data=data, headers=headers)
            mensajesComoObjeto = json.loads(msjs.text, object_hook=lambda d: SimpleNamespace(**d))
            for cadaMensaje in mensajesComoObjeto.items:
                #print(cadaMensaje)
                mensajeComoTexto = procesarTexto(cadaMensaje)
                if mensajeComoTexto:
                    print("[",cadaMensaje.created,"] =>", cadaMensaje.personEmail, "dice: ", mensajeComoTexto )
                    bd.insertarMensajes(cadaMensaje.id, cadaMensaje.roomId, mensajeComoTexto, cadaMensaje.created, cadaMensaje.personEmail)
                else:
                    mensajeComoAdjunto =procesarAdjunto(cadaMensaje)
                    print("[",cadaMensaje.created,"] =>", cadaMensaje.personEmail, "dice: ", mensajeComoAdjunto )
                    #if mensajeComoAdjunto:
                        #bd.insertarMensajes(cadaMensaje.id, cadaMensaje.roomId, mensajeComoAdjunto, cadaMensaje.created, cadaMensaje.personEmail)

def crearPersonas(tokenBearer):
    if(tokenBearer!= ""):
        headers = {"Authorization": "Bearer "+ tokenBearer}
        data = {}
        listaDeCorreos= bd.ObtenerCorreosPersonas()
        for cadaCorreo in listaDeCorreos:
            #print(cadaSala[0], cadaSala[1])
            correo = cadaCorreo[0]
            endpointPersonas = "https://webexapis.com/v1/people?" + "email=" + str(correo)
            persona = requests.get(endpointPersonas, data=data, headers=headers)
            personaComoObjeto = json.loads(persona.text, object_hook=lambda d: SimpleNamespace(**d))
            for cadaPersona in personaComoObjeto.items:
                print(cadaPersona)
                if cadaPersona.type == "bot":
                    bd.insertarPersona(cadaPersona.id, cadaPersona.displayName, cadaPersona.type, "bot", "bot", cadaPersona.emails[0])
                else:
                    bd.insertarPersona(cadaPersona.id, cadaPersona.displayName, cadaPersona.type, cadaPersona.department, cadaPersona.title, cadaPersona.emails[0])
                