DROP TABLE IF EXISTS pokemon;

CREATE TABLE pokemon(
    pokemon_id INT PRIMARY KEY,
    pokemon_name NVARCHAR(64) NOT NULL UNIQUE,
    type1_id INT NOT NULL,
    typ2_id INT,
    height FLOAT,
    mass FLOAT,
    base_experience INT,
    FOREIGN KEY (type1_id) REFERENCES pkmn_types(type_id),
    FOREIGN KEY (type2_id) REFERENCES pkmn_types(type_id)
);