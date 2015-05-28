-- PostgreSQL fixtures for dreamframework dev
-- v 0.1 - fixtures required to create a team and match simulation

DO $$
DECLARE
    sport_id INT;
    country_id INT;
    league_id INT;
    division_id INT;

BEGIN
INSERT INTO core_sport ("name") VALUES ('Association Football')
    RETURNING id INTO sport_id;

INSERT INTO core_country ("name", "country_code", "created", "modified")
    VALUES ('International', 'intl', NOW(), NOW())
    RETURNING id INTO country_id;

INSERT INTO core_league ("name", "min_age", "max_age", "gender", "schedule", "created", "modified", "country_id", "sport_id")
    VALUES ('International League', 16, 40, 'm', 0, NOW(), NOW(), country_id, sport_id)
    RETURNING id INTO league_id;

INSERT INTO core_division ("level", "teams_num", "name", "created", "modified", "league_id")
    VALUES (1, 4, 'Premier Division', NOW(), NOW(), league_id)
    RETURNING id INTO division_id;

INSERT INTO soccer_engineparam ("section", "key", "value", "description") VALUES
    ('rules', 'match_minutes', '90', ''),
    ('rules', 'match_periods', '2', ''),
    ('rules', 'match_ticks_per_minute', '10', ''),
    ('pitch', 'grid_width', '70', ''),
    ('pitch', 'grid_length', '110', ''),
    ('tactics', 'board_grid_rows', '5', ''),
    ('tactics', 'board_grid_cols', '7', '')
  ;

INSERT INTO soccer_fieldzone ("code", "row", "col") VALUES
    ('LB1', 1, 1),
    ('LB2', 1, 2),
    ('GK', 1, 4),
    ('CB1', 1, 3),
    ('CB2', 1, 5),
    ('RB1', 1, 6),
    ('RB2', 1, 7),
    ('LD1', 2, 1),
    ('LD2', 2, 2),
    ('CD1', 2, 3),
    ('CD2', 2, 4),
    ('CD3', 2, 5),
    ('RD1', 2, 6),
    ('RD2', 2, 7),
    ('LM1', 3, 1),
    ('LM2', 3, 2),
    ('CM1', 3, 3),
    ('CM2', 3, 4),
    ('CM3', 3, 5),
    ('RM1', 3, 6),
    ('RM2', 3, 7),
    ('LA1', 4, 1),
    ('LA2', 4, 2),
    ('CA1', 4, 3),
    ('CA2', 4, 4),
    ('CA3', 4, 5),
    ('RA1', 4, 6),
    ('RA2', 4, 7),
    ('LS1', 5, 1),
    ('LS2', 5, 2),
    ('CS1', 5, 3),
    ('CS2', 5, 4),
    ('CS3', 5, 5),
    ('RS1', 5, 6),
    ('RS2', 5, 7)
  ;

INSERT INTO soccer_requirement ("id", "name", "type") VALUES
    (1, 'Player.HasBall', 'bool'),
    (2, 'Game.ActionStatus', 'enum'),
    (3, 'Team.PhaseOfPlay', 'enum'),
    (4, 'Team.SetPieces', 'enum'),
    (5, 'Game.TickId', 'int')
  ;

INSERT INTO soccer_requirementenumvalue ("id", "value", "requirement_id") VALUES
    -- Game.ActionStatus (ID=2)
    (1, 'play_ongoing', 2),
    (2, 'play_interrupted', 2),
    -- Team.PhaseOfPlay (ID=3)
    (3, 'phase_offensive', 3),
    (4, 'phase_buildplay', 3),
    (5, 'phase_counterattack', 3),
    (6, 'phase_pressing', 3),
    (7, 'phase_defensive', 3),
    -- Team.SetPieces (ID=4)
    (8, 'setpieces_freekick', 4),
    (9, 'setpieces_corner', 4),
    (10, 'setpieces_throwin', 4),
    (11, 'setpieces_goalkick', 4),
    (12, 'setpieces_kickoff', 4),
    (13, 'setpieces_indirectfreekick', 4),
    (14, 'setpieces_none', 4)
  ;

INSERT INTO soccer_playeraction ("id", "name", "description", "enabled") VALUES
    (1, 'Pass', '', TRUE),
    (2, 'Shoot', '', false),
    (3, 'Clear', '', false),
    (4, 'Follow', '', false),
    (5, 'Cross', '', false),
    (6, 'Move_Offensive', '', false),
    (7, 'Move_Defensive', '', TRUE),
    (8, 'Move_Home', '', false),
    (9, 'Rest', '', false),
    (10, 'Intercept', '', false),
    (11, 'Recover', '', false),
    (12, 'Tackle', '', false),
    (13, 'Ball_Advance', '', false),
    (14, 'Ball_Sprint', '', false),
    (15, 'Ball_Dribble', '', false),
    (16, 'Indirect_Kick_Pass', '', TRUE)
  ;

INSERT INTO soccer_actionrequirement("condition", "value", "action_id", "requirement_id") VALUES
    ('is',        'true',         16,       1),
    ('is',        '2',            16,       2),
    ('can_be',    '[12, 13]',     16,       4),
    ('is',        'true',         1,        1),
    ('is',        'false',        7,        1),
    ('can_be',    '[6, 7]',       7,        3)
  ;

END $$