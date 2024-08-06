import os
import psycopg2
from psycopg2 import sql
from datetime import datetime
import pytz


def obtener_horas(inicial, turno):
    inicial = inicial.upper()
    if 'A' <= inicial <= 'E':
        horaBienvenida = "10:00 hrs."
        horaCharla = "9:00 hrs."
    elif 'F' <= inicial <= 'L':
        horaBienvenida = "12:00 hrs."
        horaCharla = "11:00 hrs."
    elif 'M' <= inicial <= 'Q':
        horaBienvenida = "14:00 hrs."
        horaCharla = "15:00 hrs."
    elif 'R' <= inicial <= 'Z':
        horaBienvenida = "16:00 hrs."
        horaCharla = "17:00 hrs."

    EI14, EI15, EI16, EI14hora, EI15hora, EI16hora = "", "", "", "", "", ""
    if turno == "Matutino":
        if 'A' <= inicial <= 'C':
            EI14, EI14hora = "Inscripción", "09:30"
        elif 'D' <= inicial <= 'G':
            EI14, EI14hora = "Inscripción", "11:30"
        elif 'H' <= inicial <= 'L':
            EI15, EI15hora = "Inscripción", "09:30"
        elif 'M' <= inicial <= 'O':
            EI15, EI15hora = "Inscripción", "11:30"
        elif 'P' <= inicial <= 'R':
            EI16, EI16hora = "Inscripción", "09:30"
        elif 'S' <= inicial <= 'Z':
            EI16, EI16hora = "Inscripción", "11:30"
    elif turno == "Vespertino":
        if 'A' <= inicial <= 'C':
            EI14, EI14hora = "Inscripción", "15:00"
        elif 'D' <= inicial <= 'G':
            EI14, EI14hora = "Inscripción", "17:00"
        elif 'H' <= inicial <= 'L':
            EI15, EI15hora = "Inscripción", "15:00"
        elif 'M' <= inicial <= 'O':
            EI15, EI15hora = "Inscripción", "17:00"
        elif 'P' <= inicial <= 'R':
            EI16, EI16hora = "Inscripción", "15:00"
        elif 'S' <= inicial <= 'Z':
            EI16, EI16hora = "Inscripción", "17:00"

    if 'P' <= inicial <= 'R':
        EI14, EI14hora = "EMA", "08:00"
    elif 'S' <= inicial <= 'T':
        EI14, EI14hora = "EMA", "11:00"
    elif 'U' <= inicial <= 'Z':
        EI14, EI14hora = "EMA", "14:00"
    elif 'A' <= inicial <= 'B':
        EI15, EI15hora = "EMA", "08:00"
    elif 'C' <= inicial <= 'D':
        EI15, EI15hora = "EMA", "11:00"
    elif 'E' <= inicial <= 'G':
        EI15, EI15hora = "EMA", "14:00"
    elif 'H' <= inicial <= 'L':
        EI16, EI16hora = "EMA", "08:00"
    elif inicial == 'M':
        EI16, EI16hora = "EMA", "11:00"
    elif inicial == 'N' or inicial == 'O':
        EI16, EI16hora = "EMA", "14:00"

    return {
        'horaBienvenida': horaBienvenida,
        'horaCharla': horaCharla,
        'EI14': EI14,
        'EI14hora': EI14hora,
        'EI15': EI15,
        'EI15hora': EI15hora,
        'EI16': EI16,
        'EI16hora': EI16hora
    }


def insertarEstadisticas(letra,apellido):
    # Obtener la URL de la base de datos desde la variable de entorno
    database_url = os.getenv('apikeyEstadisticas')
    if database_url is None:
        raise ValueError("No se encontró la variable de entorno apikeyEstadisticas")
    # Obtener la hora actual de México
    tz = pytz.timezone('America/Mexico_City')
    now = datetime.now(tz)
    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        # Crear la consulta de inserción
        insertInfoQuery = sql.SQL('''
            INSERT INTO public.estadisticas (apellido, letra, hora)
            VALUES (%s, %s, %s)
        ''')
        hora = now
        # Ejecutar la consulta
        cur.execute(insertInfoQuery, (apellido, letra, hora))
        conn.commit()
        # Cerrar el cursor y la conexión
        cur.close()
        conn.close()
    except psycopg2.OperationalError as e:
        print(f"No se pudo conectar a la base de datos: {e}")
    except psycopg2.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
