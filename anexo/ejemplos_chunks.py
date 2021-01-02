#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejemplos de clase
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para mostrar ejemplos prácticos de los visto durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import os
import csv
import sqlite3

# https://extendsclass.com/sqlite-browser.html


def create_schema():

    # Conectarnos a la base de datos
    # En caso de que no exista el archivo se genera
    # como una base de datos vacia
    conn = sqlite3.connect("personas_nacionalidad.db")

    # Crear el cursor para poder ejecutar las querys
    c = conn.cursor()

    # Crar esquema desde archivo
    c.executescript(open("schema.sql", "r").read())

    # Para salvar los cambios realizados en la DB debemos
    # ejecutar el commit, NO olvidarse de este paso!
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()


def insert_nacionalidad( name):
    conn = sqlite3.connect("personas_nacionalidad.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    c.execute("""
        INSERT INTO nacionalidad (country)
        VALUES (?);""", (name,))

    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()


def insert_persona(name, age, nationality):
    conn = sqlite3.connect("personas_nacionalidad.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    values = [name, age, nationality]

    try:
        c.execute("""
            INSERT INTO persona (name, age, fk_nationality_id)
            SELECT ?,?, n.id
            FROM nacionalidad as n
            WHERE n.country =?;""", values)
    except sqlite3.Error as err:
        print(err)

    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()


def insert_persona_grupo(group):
    conn = sqlite3.connect("personas_nacionalidad.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    try:
        c.executemany("""
            INSERT INTO persona (name, age, fk_nationality_id)
            SELECT ?,?, n.id
            FROM nacionalidad as n
            WHERE n.country =?;""", group)
    except sqlite3.Error as err:
        print(err)

    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()


def fill(chunksize=2):
    # Insertar el archivo CSV de nacionalidades
    with open("nacionalidad.csv") as fi:
        reader = csv.DictReader(fi)
        chunk = []

        for row in reader:
            insert_nacionalidad(row['nationality'])

    # Insertar el archivo CSV de personas
    with open("persona.csv") as fi:
        reader = csv.DictReader(fi)
        chunk = []

        for row in reader: 
            items = [row['name'], int(row['age']), row['nationality_id']]
            chunk.append(items)
            if len(chunk) == chunksize:
                insert_persona_grupo(chunk)
                chunk.clear()
        
        if chunk:
            insert_persona_grupo(chunk)



def show(limit=0):
    # Conectarse a la base de datos
    conn = sqlite3.connect("personas_nacionalidad.db")
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    # Leer todas las filas y obtener los datos de a uno
    query = """SELECT p.id, p.name, p.age, n.country
                 FROM persona as p, nacionalidad as n
                 WHERE p.fk_nationality_id = n.id"""

    if limit > 0:
        query = query + ' LIMIT ' + str(limit)

    query = query + ';'

    c.execute(query)

    while True:
        row = c.fetchone()
        if row is None:
            break
        print(row)

    # Cerrar la conexión con la base de datos
    conn.close()


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()

    # Insertar nacionalidades y personas
    fill()
    show()
