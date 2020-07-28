CREATE TABLE IF NOT EXISTS protocol (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY,
    protocol INT,
    FOREIGN KEY (protocol) REFERENCES protocol(id)
);

CREATE TABLE IF NOT EXISTS abbreviation (
    id INTEGER PRIMARY KEY,
    abbr TEXT,
    meaning TEXT NOT NULL,
    history INT,
    FOREIGN KEY (history) REFERENCES history(id)
);

CREATE TABLE IF NOT EXISTS datatype (
    id INTEGER PRIMARY KEY,
    name TEXT,
    base INT,
    history INT,
    FOREIGN KEY (base) REFERENCES datatypes(id),
    FOREIGN KEY (history) REFERENCES history(id)
);

CREATE TABLE IF NOT EXISTS fields (
    id INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS section (
    id INTEGER PRIMARY KEY,
    name TEXT,
    history INT,
    FOREIGN KEY (history) REFERENCES history(id)
);

CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY,
    name TEXT,
    kind TEXT,
    section INT,
    history INT,
    FOREIGN KEY (section) REFERENCES section(id)
    FOREIGN KEY (history) REFERENCES history(id)
);

CREATE TABLE IF NOT EXISTS component (
    id INTEGER PRIMARY KEY,
    history INT,
    FOREIGN KEY (history) REFERENCES history(id)
);

-- CREATE UNIQUE INDEX IF NOT EXISTS abbreviation.lookup ON abbreviation(abbr);
-- CREATE UNIQUE INDEX IF NOT EXISTS datatype.lookup ON datatype(name);
