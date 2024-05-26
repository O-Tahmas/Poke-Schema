DROP TABLE IF EXISTS move_stat_changes;
DROP TABLE IF EXISTS pokemon_movesets;
DROP TABLE IF EXISTS moves;
DROP TABLE IF EXISTS move_targets;
DROP TABLE IF EXISTS move_ailments;
DROP TABLE IF EXISTS move_damage_classes;
DROP TABLE IF EXISTS move_categories;

CREATE TABLE move_categories(
    id INT PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE move_damage_classes (
    id INT PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE move_ailments (
    id INT PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE move_targets (
    id INT PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE moves (
    move_id INT PRIMARY KEY,
    move_name VARCHAR(255) NOT NULL UNIQUE,
    type_id INT,
    priority_rank SMALLINT,
    power SMALLINT,
    accuracy SMALLINT,
    effect_chance SMALLINT,
    pp SMALLINT,
    crit_rate SMALLINT,
    drain SMALLINT,
    flinch_chance SMALLINT,
    healing SMALLINT,
    max_hits SMALLINT,
    max_turns SMALLINT,
    min_hits SMALLINT,
    min_turns SMALLINT,
    stat_chance SMALLINT,
    damage_class_id INT,
    ailment_id INT,
    category_id INT,
    target_id INT,
    generation_id INT,
    FOREIGN KEY (type_id) REFERENCES pkmn_types(type_id),
    FOREIGN KEY (damage_class_id) REFERENCES move_damage_classes(id),
    FOREIGN KEY (ailment_id) REFERENCES move_ailments(id),
    FOREIGN KEY (category_id) REFERENCES move_categories(id),
    FOREIGN KEY (target_id) REFERENCES move_targets(id),
    FOREIGN KEY (generation_id) REFERENCES generations(generation_id)
);

CREATE TABLE pokemon_movesets (
    move_id INT,
    learned_by_pokemon INT,
    PRIMARY KEY (move_id, learned_by_pokemon),
    FOREIGN KEY (move_id) REFERENCES moves(move_id) ,
    FOREIGN KEY (learned_by_pokemon) REFERENCES pokemon(pokemon_id)
);

CREATE TABLE move_stat_changes (
    move_id INT,
    stat_id INT,
    change INT NOT NULL,
    PRIMARY KEY (move_id, stat_id),
    FOREIGN KEY (move_id) REFERENCES moves(move_id),
    FOREIGN KEY (stat_id) REFERENCES base_stats(stat_id)
);