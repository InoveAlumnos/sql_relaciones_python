DROP TABLE IF EXISTS persona;

DROP TABLE IF EXISTS nacionalidad;

CREATE TABLE nacionalidad(
    [id] INTEGER PRIMARY KEY,
    [name] STRING NOT NULL
);

CREATE TABLE persona(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] STRING NOT NULL,
    [age] INTEGER NOT NULL,
    [nationality] INTEGER NOT NULL REFERENCES nacionalidad(id)
);
