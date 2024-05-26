DROP TABLE IF EXISTS moves;

CREATE TABLE moves (
    move_id INT PRIMARY KEY,
    move_name VARCHAR(255) NOT NULL UNIQUE,
    type_id INT,
    power INT,
    accuracy INT,
    pp INT,
    FOREIGN KEY (type_id) REFERENCES pkmn_types(type_id)
);
