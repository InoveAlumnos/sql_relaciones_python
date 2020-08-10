DROP TABLE IF EXISTS persona;

DROP TABLE IF EXISTS nacionalidad;

CREATE TABLE nacionalidad(
    [id] INTEGER PRIMARY KEY,
    [country] STRING NOT NULL
);

CREATE TABLE persona(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] STRING NOT NULL,
    [age] INTEGER NOT NULL,
    [fk_nationality_id] INTEGER NOT NULL REFERENCES nacionalidad(id)
);
