#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejemplos de clase
---------------------------
Autor: Inove Coding School
Version: 1.2

Descripcion:
Programa creado para mostrar ejemplos prácticos de los visto durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.2"

import os
import csv
import sqlite3

from config import config

# https://extendsclass.com/sqlite-browser.html

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
db = config('db', config_path_name)
dataset = config('dataset', config_path_name)

# Obtener el path real del archivo de schema
schema_path_name = os.path.join(script_path, db['schema'])


def create_schema():

    # Conectarnos a la base de datos
    # En caso de que no exista el archivo se genera
    # como una base de datos vacia
    conn = sqlite3.connect(db['database'])

    # Crear el cursor para poder ejecutar las querys
    c = conn.cursor()

    # Crar esquema desde archivo
    c.executescript(open(schema_path_name, "r").read())

    # Para salvar los cambios realizados en la DB debemos
    # ejecutar el commit, NO olvidarse de este paso!
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()


def insert_nacionalidad( name):
    conn = sqlite3.connect(db['database'])
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    c.execute("""
        INSERT INTO nacionalidad (country)
        VALUES (?);""", (name,))

    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()


def insert_persona(name, age, nationality):
    conn = sqlite3.connect(db['database'])
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
    conn = sqlite3.connect(db['database'])
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


def fill():
    # Insertar el archivo CSV de nacionalidades
    # Insertar fila a fila
    with open(dataset['nationality']) as fi:
        data = list(csv.DictReader(fi))

        for row in data:
            insert_nacionalidad(row['nationality'])

    # Insertar el archivo CSV de personas
    # Insertar todas las filas juntas
    with open(dataset['person']) as fi:
        data = list(csv.DictReader(fi))

        data_formateada = [[row['name'], int(row['age']), row['nationality_id']] for row in data]
        insert_persona_grupo(data_formateada)



def show(limit=0):
    # Conectarse a la base de datos
    conn = sqlite3.connect(db['database'])
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


def update_persona_nationality(name, nationality):
    # Conectarse a la base de datos
    conn = sqlite3.connect(db['database'])
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    rowcount = c.execute("""UPDATE persona
                            SET fk_nationality_id =
                            (SELECT n.id FROM nacionalidad as n
                             WHERE n.country =?)
                            WHERE name =?""",
                         (nationality, name)).rowcount

    print('Filas actualizadas:', rowcount)

    # Save
    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()


def delete_persona(name):
    # Conectarse a la base de datos
    conn = sqlite3.connect(db['database'])
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    # Borrar la fila cuyo nombre coincida con la búsqueda
    # NOTA: Recordar que las tupla un solo elemento se definen como
    # (elemento,)
    # Si presta a confusión usar una lista --> [elemento]
    rowcount = c.execute("DELETE FROM persona WHERE name =?", (name,)).rowcount

    print('Filas actualizadas:', rowcount)

    # Save
    conn.commit()
    # Cerrar la conexión con la base de datos
    conn.close()


def count_persona(nationality):
        # Conectarse a la base de datos
    conn = sqlite3.connect(db['database'])
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    # Borrar la fila cuyo nombre coincida con la búsqueda
    # NOTA: Recordar que las tupla un solo elemento se definen como
    # (elemento,)
    # Si presta a confusión usar una lista --> [elemento]
    c.execute("""SELECT COUNT(p.id) AS country_count
                 FROM persona as p, nacionalidad as n
                 WHERE p.fk_nationality_id = n.id
                 AND n.country =?;""", (nationality,))

    result = c.fetchone()
    count = result[0]
    print('Personas de', nationality, 'encontradas:', count)


    # Cerrar la conexión con la base de datos
    conn.close()


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()

    # Insertar nacionalidades y personas
    fill()
    show()

    count_persona('Argentina')

    # update_persona_nationality('Max', 'Holanda')
    # show()

    # group = [('Max', 40, 'Estados Unidos'),
    #          ('SQL', 13, 'Inglaterra'),
    #          ('SQLite', 20, 'Estados Unidos'),
    #          ]

    # insert_persona_grupo(group)
    # show()
