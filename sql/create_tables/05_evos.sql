DROP TABLE IF EXISTS evolution_chains;
DROP TABLE IF EXISTS evolution_triggers;

CREATE TABLE evolution_triggers (
    trigger_id INT PRIMARY KEY,
    evolution_trigger VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE evolution_chains (
    chain_group_id INT,
    pokemon_id INT,
    trigger_id INT,
    evolution_order SMALLINT NOT NULL,
    gender SMALLINT,
    held_item SMALLINT,
    item SMALLINT,
    known_move SMALLINT,
    known_move_type SMALLINT,
    location SMALLINT,
    min_affection SMALLINT,
    min_beauty SMALLINT,
    min_happiness SMALLINT,
    min_level SMALLINT,
    needs_overworld_rain SMALLINT,
    party_species SMALLINT,
    party_type SMALLINT,
    relative_physical_stats SMALLINT,
    time_of_day VARCHAR(32),
    trade_species SMALLINT,
    PRIMARY KEY (chain_group_id, pokemon_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemon(pokemon_id),
    FOREIGN KEY (trigger_id) REFERENCES evolution_triggers(trigger_id)
);