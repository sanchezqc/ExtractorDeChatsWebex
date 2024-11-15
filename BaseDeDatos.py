import sqlite3

def inicializarTablas():
    conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Rooms(id VARCHAR,' +
            'title VARCHAR)')
    cur.execute('CREATE TABLE IF NOT EXISTS Mensajes(id VARCHAR,' +
            'roomId VARCHAR,'+
            'text VARCHAR,'+
            'created DATETIME,'+
            'personMail VARCHAR'+
            ')')
    cur.execute('CREATE TABLE IF NOT EXISTS Personas(id VARCHAR,' +
            'displayName VARCHAR,'+
            'type VARCHAR,'+
            'department VARCHAR,'+
            'title VARCHAR,'+
            'email VARCHAR'
            ')')
    conn.commit()
    conn.close()

def ExisteSala(id)-> bool:
    conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Rooms WHERE id ='"+ id+"'")
    resultado = cur.fetchone()
    rowsAffected = resultado[0]
    conn.close()    
    if rowsAffected==0:
        return False
    else:
        return True


def insertarSala(id, title):
    conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    if not ExisteSala(id):
        cur.execute("INSERT INTO Rooms (id, title) values(?,?)",(id, title))
        conn.commit()
    else:
        cur.execute("UPDATE Rooms SET title = (?) WHERE id = (?) ",(title, id))
        conn.commit()
    conn.close()

def ObtenerSalas():
    conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM Rooms")
    resultado = cur.fetchall()
    return resultado

def ExisteMensaje(id)-> bool:
    conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Mensajes WHERE id ='"+ id+"'")
    resultado = cur.fetchone()
    rowsAffected = resultado[0]
    conn.close()    
    if rowsAffected==0:
        return False
    else:
        return True

def insertarMensajes(id, roomId, text, created, personMail):
    conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    if not ExisteMensaje(id):
        cur.execute("INSERT INTO Mensajes (id, roomId, text, created, personMail) values(?,?,?,?,?)",(id, roomId, text, created, personMail))
        conn.commit()
    else:
        cur.execute("UPDATE Mensajes SET roomId = (?), text = (?), created = (?), personMail = (?) WHERE id = (?) ",(roomId, text, created, personMail, id))
        conn.commit()
    conn.close()

def ObtenerCorreosPersonas():
    conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute("SELECT distinct personMail FROM Mensajes")
    resultado = cur.fetchall()
    return resultado

def ExistePersona(id)-> bool:
    conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Personas WHERE id ='"+ id+"'")
    resultado = cur.fetchone()
    rowsAffected = resultado[0]
    conn.close()    
    if rowsAffected==0:
        return False
    else:
        return True

def insertarPersona(id, displayName, type, department, title, email):
    conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    if not ExistePersona(id):
        cur.execute("INSERT INTO Personas (id, displayName, type, department, title, email) values(?,?,?,?,?,?)",(id, displayName, type, department, title, email))
        conn.commit()
    else:
        cur.execute("UPDATE Mensajes SET displayName = (?), type = (?), department = (?), title = (?), email = (?) WHERE id = (?) ",(displayName, type, department, title, email,id))
        conn.commit()
    conn.close()

def ObtenerPersonas():
    conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute("SELECT email FROM Personas")
    resultado = cur.fetchall()
    return resultado

def ObtenerMensajesPorSala(idSala):
    conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute("SELECT text, created, personMail, displayName FROM Mensajes INNER JOIN Personas ON Mensajes.personMail = Personas.email WHERE roomId='"+idSala+"' order by created")
    resultado = cur.fetchall()
    return resultado

def ObtenerNombresSalas():
    conn= sqlite3.connect('BD.sqlite',detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute("SELECT title, id FROM Rooms order by title")
    resultado = cur.fetchall()
    return resultado