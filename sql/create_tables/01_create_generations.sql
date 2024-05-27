DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS game_versions;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS generations;

CREATE TABLE generations (
    generation_id INT PRIMARY KEY,
    generation_name VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE regions (
    region_id INT PRIMARY KEY,
    region_name VARCHAR(32) NOT NULL UNIQUE
    generation_id INT,
    FOREIGN KEY (generation_id) REFERENCES generations(generation_id)
);

CREATE TABLE locations (
    location_id INT PRIMARY KEY,
    location_name VARCHAR(64) NOT NULL UNIQUE,
    region_id INT,
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);

CREATE TABLE game_versions (
    version_id INT PRIMARY KEY,
    version_name VARCHAR(64) UNIQUE NOT NULL,
    generation_id INT,
    FOREIGN KEY (generation_id) REFERENCES generations(generation_id)
);

CREATE TABLE games (
    game_id INT PRIMARY KEY,
    game_name VARCHAR(64) NOT NULL UNIQUE,
    version_id INT,
    FOREIGN KEY (version_id) REFERENCES game_versions(version_id)
);