CREATE TABLE IF NOT EXISTS artists (
    artistId SERIAL PRIMARY KEY,
    artistDisplayName VARCHAR(200),
    nationality VARCHAR(100),
    birth INT,
    death INT,
    gender VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS departments (
    departmentId SERIAL PRIMARY KEY,
    name VARCHAR(100) 
);

CREATE TABLE IF NOT EXISTS origins (
    originId SERIAL PRIMARY KEY,
    city VARCHAR(100),
    country VARCHAR(100),
    region VARCHAR(100),
    culture VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS periods (
    periodId SERIAL PRIMARY KEY,
    period VARCHAR(100),
    dynasty VARCHAR(200),
    reign VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS mediums (
    mediumId SERIAL PRIMARY KEY,
    medium VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS artworks (
    objectId INT PRIMARY KEY,
    periodId INT REFERENCES periods(periodId),
    originId INT REFERENCES origins(originId),
    departmentId INT NOT NULL REFERENCES departments(departmentId),
    isHighlight BOOLEAN,
    isPublicDomain BOOLEAN,
    objectName VARCHAR(100),
    classification VARCHAR(100), 
    title TEXT,
    accessionYear INT,
    objectDate VARCHAR(100),
    objectBeginDate INT,
    objectEndDate INT,
    dimensions TEXT
);

CREATE TABLE IF NOT EXISTS artworkArtist(
    objectId INT NOT NULL REFERENCES artworks(objectId) ON DELETE CASCADE,
    artistId INT NOT NULL REFERENCES artists(artistId) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS artworkMedium(
    objectId INT NOT NULL REFERENCES artworks(objectId) ON DELETE CASCADE,
    mediumId INT NOT NULL REFERENCES mediums(mediumId) ON DELETE CASCADE
);
