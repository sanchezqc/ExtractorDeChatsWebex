import streamlit as st
import sqlite3
import BaseDeDatos as bd
import requestsApisWebex as apiswebex
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

bd.inicializarTablas()

st.header("Cargar mensajes de webex")
beaererToken = st.text_input("Introduzca su identificador Bearer")
#col1, col2 = st.columns(2)
st.subheader("Cargar salas (chats)")
if st.button("Generar salas de chats"):
    apiswebex.crearSalas(beaererToken)

st.subheader("Salas almacenadas (chats )")

##GRID DE SALAS CHATS
gb = GridOptionsBuilder()
gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
)

gb.configure_column(field="title", header_name="Chat con", width=150)
gb.configure_column(field="id", header_name="Identificador interno del chat", width=150)

conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
df = pd.read_sql_query(con=conn, sql="SELECT * FROM Rooms")
gridOptions = gb.build()
AgGrid(data=df, height= 300, fit_columns_on_grid_load=True, gridOptions=gridOptions)

if st.button("Generar mensajes de chats"):
    apiswebex.crearMensajes(beaererToken)


##GRID DE MENSAJES SIN RELACIONAR
st.subheader("Chats almacenados")
gbMensajes = GridOptionsBuilder()
gbMensajes.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
)
gbMensajes.configure_column(field="title", header_name="Chat con", width=150)
gbMensajes.configure_column(field="personMail", header_name="correo de contacto", width=150)
gbMensajes.configure_column(field="text", header_name="mensaje", width=150)
gbMensajes.configure_column(field="created", header_name="fecha y hora", width=150)
gbMensajes.configure_column(field="id", header_name="identificador interno de mensaje", width=150)
gbMensajes.configure_column(field="roomId", header_name="Identificador interno Sala", width=150)

conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
dfMensajes = pd.read_sql_query(con=conn, sql="SELECT Mensajes.*, Rooms.title FROM Mensajes INNER JOIN Rooms ON Rooms.Id = Mensajes.roomId")
gridOptionsMensajes = gbMensajes.build()
AgGrid(key="gridMensajes", data=dfMensajes, height= 300, fit_columns_on_grid_load=True, gridOptions=gridOptionsMensajes)

if st.button("Generar Personas"):
    apiswebex.crearPersonas(beaererToken)

##GRID DE MENSAJES SIN RELACIONAR
st.subheader("Personas")
gbPersonas = GridOptionsBuilder()
gbPersonas.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
)
gbPersonas.configure_column(field="displayName", header_name="Nombre", width=150)
gbPersonas.configure_column(field="email", header_name="correo", width=150)
gbPersonas.configure_column(field="type", header_name="Tipo contacto", width=150)
gbPersonas.configure_column(field="id", header_name="Id interno", width=150)
gbPersonas.configure_column(field="department", header_name="Departamento", width=150)
gbPersonas.configure_column(field="title", header_name="Puesto", width=150)

conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
dfPersonas = pd.read_sql_query(con=conn, sql="SELECT * FROM Personas")
gridOptionsPersonas = gbPersonas.build()
AgGrid(key="gridPersonas", data=dfPersonas, height= 300, fit_columns_on_grid_load=True, gridOptions=gridOptionsPersonas)

####CHAT

listaSalas = bd.ObtenerNombresSalas()
listaSalasConNombre = []
for cadaSala in listaSalas:
    listaSalasConNombre.append(cadaSala[0])

salaSeleccionada = st.selectbox("Selecciona una conversación", options=listaSalasConNombre)
roomId= ""
for cadaSala in listaSalas:
    if cadaSala[0] == salaSeleccionada:
        roomId = cadaSala[1]

container = st.container(border=True, height=600)

for cadaMensaje in bd.ObtenerMensajesPorSala(roomId):
    #print(cadaMensaje[0])
    messagePrimerPersona = container.chat_message("user")
    mensaje = cadaMensaje[0]
    creado = cadaMensaje[1]
    mail = cadaMensaje[2]
    nombre = cadaMensaje[3]
    messagePrimerPersona.write(creado + "➡️" +nombre +"("+mail+")"+ " dice:\n " + mensaje)
    #messageSegundaPersona = st.chat_message("ai")
    #messageSegundaPersona.write("Segunda persona")
