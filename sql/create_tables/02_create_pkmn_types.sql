DROP TABLE IF EXISTS type_relations;
DROP TABLE IF EXISTS pkmn_types;


CREATE TABLE pkmn_types (
    type_id INT PRIMARY KEY,
    type_name VARCHAR(32) NOT NULL UNIQUE,
	generation INT NOT NULL
);

CREATE TABLE type_relations (
	type_id INT,
	related_type_id INT,
	dmg_multiplier FLOAT NOT NULL,
	PRIMARY KEY (type_id, related_type_id),
	FOREIGN KEY (type_id) REFERENCES pkmn_types(type_id),
	FOREIGN KEY (related_type_id) REFERENCES pkmn_types(type_id)
);

