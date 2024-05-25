DROP TABLE IF EXISTS pokemon;
DROP TABLE IF EXISTS base_stats;
DROP TABLE IF EXISTS pokemon_base_stats;

CREATE TABLE pokemon(
    pokemon_id INT PRIMARY KEY,
    pokemon_name VARCHAR(64) NOT NULL UNIQUE,
    type1_id INT NOT NULL,
    type2_id INT,
    height INT,
    mass INT,
    base_experience INT,
    FOREIGN KEY (type1_id) REFERENCES pkmn_types(type_id),
    FOREIGN KEY (type2_id) REFERENCES pkmn_types(type_id)
);

CREATE TABLE base_stats(
    stat_id INT PRIMARY KEY,
    stat_name varchar(32) UNIQUE NOT NULL
);

CREATE TABLE pokemon_base_stats(
    pokemon_id INT,
    stat_id INT,
    stat_value INT,
    PRIMARY KEY (pokemon_id, stat_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY (stat_id) REFERENCES base_stats(stat_id)
);
