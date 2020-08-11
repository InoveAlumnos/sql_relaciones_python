# Ejercicios de práctica [Python]
EL propósito de este ejercicio es que el alumno ponga sus habilidades de SQL junto con otras adqueridas a lo largo de la carrera como el manejo de archivos CSV. Este es un caso típico de ETL en donde se transforma un sistema legacy de datos (un archivo) en una base de datos.

# Enunciado
El objetivo es realizar un ejercicio muy similar al de "ejercicios_clase" pero ahora el alumno será quien genere el esquema de la base de datos para construirla.\

Deberá generar una base de datos de libros basada en los archivo CSV libreria_autor.csv y libreria_libro.csv, los cuales poseen las siguientes columnas:
- id del autor (id) --> número (autoincremental, lo define y completa SQL por ustedes)
- Nombre del autor (author) --> texto

- id del libro (id) --> número (autoincremental, lo define y completa SQL por ustedes)
- Título del libro (title) --> texto
- Cantidad de páginas (pags) --> número
- Nombre del autor (author) --> texto

## create_schema
Deben crear una función "create_schema" la cual se encargará de crear la base de datos y la tabla correspondiente al esquema definido. Deben usar la sentencia CREATE para crear la tabla mencionada.\
Se debe crear una tabla "libro" y una tabla "autor". La coulmna "author" de la tabla "libro" debe estar relacionada (clave ajena) con la tabla "autor".\
IMPORTANTE: Recuerden que es recomendable borrar la tabla (DROP) antes de crearla si es que existe para que no haya problemas al ejecutar la query.

## fill()
Deben crear una función "fill" que lea los datos de los archivos CSV y cargue esas filas de los archivos como filas de las tablas SQL. Pueden resolverlo de la forma que mejor crean. Deben usar la sentencia INSERT para insertar los datos.\

## fetch(id)
Deben crear una función que imprima en pantalla las filas de la tabla "persona", pueden usar esta función para ver que "fill" realizó exactamente lo que era esperado. 
- Deben usar la sentencia SELECT para llegar al objetivo junto con WHERE para leer la fila deseada (si se desea leer una en particular).
- Debe usar el concepto de INNER JOIN para reemplazar el "id" del autor por su nombre definido en la tabla "autor".
Esta función recibe como parámetro un id:
- En caso de que el id sea igual a cero (id=0) deben imprimir todas las filas de la tabla "persona".
- En caso de que id sea mayor a cero (id>0) deben imprimir sola la fila correspondiente a ese id.
IMPORTANTE: Es posible que pasen como id un número no definido en la tabla y el sistema de fetchone les devuelva None, lo cual es correcto, pero el sistema no debe explotar porque haya retornado None. En ese caso pueden imprimir en pantalla que no existe esa fila en la base de datos (más adelante en una API responderá Error 404).

## search_author(book_title)
Deben crear una función que retorne el nombre del autor que pertenece al título del libro pasado como parámetro a esta función. Deben usar la función SELECT junto con WHERE para buscar el autor correspondiente al libro.\
Al finalizar la función rebe retornar el autor:
```
    return author
```

## Esquema del ejercicio
Deben crear su archivo de python y crear las funciones mencionadas en este documento. Deben crear la sección "if _name_ == "_main_" y ahí crear el flujo de prueba de este programa:
```
if __name__ == "__main__":
  # Crear DB
  create_schema()

  # Completar la DB con el CSV
  fill()

  # Leer filas
  fetch()  # Ver todo el contenido de la DB
  fetch(3)  # Ver la fila 3
  fetch(20)  # Ver la fila 20

  # Buscar autor
  print(search_author('Relato de un naufrago'))

```
