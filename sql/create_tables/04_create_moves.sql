DROP TABLE IF EXISTS move_stat_changes;
DROP TABLE IF EXISTS pokemon_movesets;
DROP TABLE IF EXISTS moves;
DROP TABLE IF EXISTS move_targets;
DROP TABLE IF EXISTS move_ailments;
DROP TABLE IF EXISTS move_damage_class;
DROP TABLE IF EXISTS move_category;

CREATE TABLE move_category(
    move_cat_id INT PRIMARY KEY,
    move_cat_name VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE move_damage_class (
    dmg_class_id INT PRIMARY KEY,
    dmg_class_name VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE move_ailments (
    ailment_id INT PRIMARY KEY,
    ailment_name VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE move_targets (
    target_id INT PRIMARY KEY,
    target_name VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE moves (
    move_id INT PRIMARY KEY,
    move_name VARCHAR(255) NOT NULL UNIQUE,
    type_id INT,
    priority_rank INT,
    power INT,
    accuracy INT,
    effect_chance INT,
    pp INT,
    crit_rate INT,
    drain INT,
    flinch_chance INT,
    healing INT,
    max_hits INT,
    max_turns INT,
    min_hits INT,
    min_turns INT,
    stat_chance INT,
    damage_class_id INT,
    ailment_id INT,
    category_id INT,
    generation_id INT,
    target_id INT,
    FOREIGN KEY (type_id) REFERENCES pkmn_types(type_id),
    FOREIGN KEY (damage_class_id) REFERENCES move_damage_class(dmg_class_id),
    FOREIGN KEY (ailment_id) REFERENCES move_ailments(ailment_id),
    FOREIGN KEY (category_id) REFERENCES move_category(move_cat_id),
    FOREIGN KEY (generation_id) REFERENCES generations(generation_id),
    FOREIGN KEY (target_id) REFERENCES move_targets(target_id)
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
    change INT NOT NULL UNIQUE,
    PRIMARY KEY (move_id, stat_id),
    FOREIGN KEY (move_id) REFERENCES moves(move_id),
    FOREIGN KEY (stat_id) REFERENCES base_stats(stat_id)
);