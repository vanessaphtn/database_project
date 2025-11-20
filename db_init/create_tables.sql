CREATE TABLE IF NOT EXISTS artists (
    artistId SERIAL PRIMARY KEY,
    name VARCHAR(200) UNIQUE,
    nationality VARCHAR(100),
    birth INT,
    death INT,
    gender VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS departments (
    departmentId SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS origins (
    originId SERIAL PRIMARY KEY,
    city VARCHAR(100),
    country VARCHAR(100),
    region VARCHAR(100),
    culture VARCHAR(100),
    UNIQUE(city, country, region, culture)
);

CREATE TABLE IF NOT EXISTS periods (
    periodId SERIAL PRIMARY KEY,
    period TEXT,
    dynasty TEXT,
    reign TEXT,
    UNIQUE(period, dynasty, reign)
);

CREATE TABLE IF NOT EXISTS mediums (
    mediumId SERIAL PRIMARY KEY,
    medium VARCHAR(200) UNIQUE
);

CREATE TABLE IF NOT EXISTS artworks (
    objectId INT PRIMARY KEY,
    periodId INT REFERENCES periods(periodId),
    originId INT REFERENCES origins(originId),
    departmentId INT NOT NULL REFERENCES departments(departmentId),
    isHighlight BOOLEAN,
    isPublicDomain BOOLEAN,
    objectName TEXT,
    classification TEXT, 
    title TEXT,
    accessionYear INT,
    objectDate TEXT,
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
