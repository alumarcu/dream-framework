-- PostgreSQL fixtures for dreamframework dev
-- v 0.1 - fixtures required to create a team and match simulation

DO $$
DECLARE
    sport_id INT;
    country_id INT;
    league_id INT;
    division_id INT;

BEGIN
INSERT INTO "core_sport" ("id", "name", "common_key") VALUES
	(1, 'Association Football', 'soccer') RETURNING id INTO sport_id;

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

-- Inserting two test teams
INSERT INTO "auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") VALUES
	(2, 'pbkdf2_sha256$20000$nZr1cEUmOlo7$oRodZ/QYVuPx8T8rkXknZm6xV3RguMteBAhP2LVmgIw=', NULL, 'false', 'alice', '', '', 'alice@test.com', 'false', 'true', '2015-06-14 13:33:04.438289+03'),
	(3, 'pbkdf2_sha256$20000$MxsHWDMaIVWI$hFyFch51OqlMLUpZRcxpUM5igofLW21ZbGC03iwi1pA=', NULL, 'false', 'bob', '', '', 'bob@test.com', 'false', 'true', '2015-06-14 13:33:44.465875+03');

INSERT INTO "core_club" ("id", "manager_id", "country_id", "name", "created", "modified") VALUES
	(1, 1, 1, 'FC Alice Wicked Gang', '2015-06-14 13:33:04.466114+03', '2015-06-14 13:33:04.466128+03'),
	(2, 2, 1, 'FC Bobby and the Rebels', '2015-06-14 13:33:44.490839+03', '2015-06-14 13:33:44.490852+03');

INSERT INTO "core_team" ("id", "club_id", "name", "gender", "created", "modified") VALUES
	(1, 1, 'Alice Wicked Gang', 'm', '2015-06-14 13:33:04.46775+03', '2015-06-14 13:33:04.467764+03'),
	(2, 2, 'Bobby and the Rebels', 'm', '2015-06-14 13:33:44.492124+03', '2015-06-14 13:33:44.492137+03');

INSERT INTO "core_teamdivision" ("id", "team_id", "division_id") VALUES
	(1, 1, 1),
	(2, 2, 1);

INSERT INTO "core_manager" ("id", "user_id", "name", "age", "gender", "created", "modified") VALUES
	(1, 2, 'Alice Test', NULL, 'u', '2015-06-14 13:33:04.464469+03', '2015-06-14 13:33:04.464489+03'),
	(2, 3, 'Bob Test', NULL, 'u', '2015-06-14 13:33:44.489756+03', '2015-06-14 13:33:44.489772+03');

INSERT INTO "core_npc" ("id", "club_id", "team_id", "first_name", "last_name", "nickname", "age", "gender", "role", "created", "modified") VALUES
	(1, 1, 1, 'Tarathiel', 'Kadyrk', '', 28, 'm', '', '2015-06-14 13:33:04.538338+03', '2015-06-14 13:33:04.538359+03'),
	(2, 1, 1, 'Elyamour', 'Camlars', '', 22, 'm', '', '2015-06-14 13:33:04.539245+03', '2015-06-14 13:33:04.539258+03'),
	(3, 1, 1, 'Ailduin', 'Blaise', '', 18, 'm', '', '2015-06-14 13:33:04.539659+03', '2015-06-14 13:33:04.539673+03'),
	(4, 1, 1, 'Garelon', 'Kahevere', '', 21, 'm', '', '2015-06-14 13:33:04.540022+03', '2015-06-14 13:33:04.540034+03'),
	(5, 1, 1, 'Taegen', 'Gorlart', '', 17, 'm', '', '2015-06-14 13:33:04.540382+03', '2015-06-14 13:33:04.540395+03'),
	(6, 1, 1, 'Vortidred', 'Ozakane', '', 25, 'm', '', '2015-06-14 13:33:04.540797+03', '2015-06-14 13:33:04.54081+03'),
	(7, 1, 1, 'Gorre', 'Blafir', '', 29, 'm', '', '2015-06-14 13:33:04.54116+03', '2015-06-14 13:33:04.541172+03'),
	(8, 1, 1, 'Chapanfal', 'Kahevere', '', 22, 'm', '', '2015-06-14 13:33:04.54154+03', '2015-06-14 13:33:04.541553+03'),
	(9, 1, 1, 'Darthoridan', 'Mengwain', '', 30, 'm', '', '2015-06-14 13:33:04.541905+03', '2015-06-14 13:33:04.541917+03'),
	(10, 1, 1, 'Anlyth', 'Ywaiberis', '', 21, 'm', '', '2015-06-14 13:33:04.542272+03', '2015-06-14 13:33:04.542298+03'),
	(11, 1, 1, 'Garelon', 'Mengwain', '', 18, 'm', '', '2015-06-14 13:33:04.543093+03', '2015-06-14 13:33:04.543114+03'),
	(12, 1, 1, 'Aumanas', 'Bleoramurs', '', 21, 'm', '', '2015-06-14 13:33:04.54399+03', '2015-06-14 13:33:04.54429+03'),
	(13, 1, 1, 'Tarathiel', 'Gahevere', '', 31, 'm', '', '2015-06-14 13:33:04.54628+03', '2015-06-14 13:33:04.546344+03'),
	(14, 1, 1, 'Ydebron', 'Gahmule', '', 21, 'm', '', '2015-06-14 13:33:04.547258+03', '2015-06-14 13:33:04.547273+03'),
	(15, 1, 1, 'Lhoris', 'Gahevere', '', 22, 'm', '', '2015-06-14 13:33:04.54766+03', '2015-06-14 13:33:04.547673+03'),
	(16, 1, 1, 'Darthoridan', 'Blaise', '', 26, 'm', '', '2015-06-14 13:33:04.548024+03', '2015-06-14 13:33:04.548037+03'),
	(17, 1, 1, 'Vortidred', 'Ladeam', '', 28, 'm', '', '2015-06-14 13:33:04.548395+03', '2015-06-14 13:33:04.548408+03'),
	(18, 1, 1, 'Alescien', 'Astokin', '', 25, 'm', '', '2015-06-14 13:33:04.548791+03', '2015-06-14 13:33:04.548804+03'),
	(19, 2, 2, 'Darthoridan', 'Ettase', '', 18, 'm', '', '2015-06-14 13:33:44.494635+03', '2015-06-14 13:33:44.494651+03'),
	(20, 2, 2, 'Naesala', 'Ladeam', '', 22, 'm', '', '2015-06-14 13:33:44.495144+03', '2015-06-14 13:33:44.495157+03'),
	(21, 2, 2, 'Antoscien', 'Laihan', '', 31, 'm', '', '2015-06-14 13:33:44.495508+03', '2015-06-14 13:33:44.49552+03'),
	(22, 2, 2, 'Taegen', 'Arardin', '', 20, 'm', '', '2015-06-14 13:33:44.49589+03', '2015-06-14 13:33:44.495903+03'),
	(23, 2, 2, 'Brubal', 'Kahevere', '', 27, 'm', '', '2015-06-14 13:33:44.49625+03', '2015-06-14 13:33:44.496262+03'),
	(24, 2, 2, 'Darthoridan', 'Branna', '', 17, 'm', '', '2015-06-14 13:33:44.496609+03', '2015-06-14 13:33:44.496655+03'),
	(25, 2, 2, 'Elephon', 'Bleoramurs', '', 31, 'm', '', '2015-06-14 13:33:44.49701+03', '2015-06-14 13:33:44.497022+03'),
	(26, 2, 2, 'Llarm', 'Gorlart', '', 18, 'm', '', '2015-06-14 13:33:44.497367+03', '2015-06-14 13:33:44.497379+03'),
	(27, 2, 2, 'Ailduin', 'Elyakane', '', 23, 'm', '', '2015-06-14 13:33:44.497744+03', '2015-06-14 13:33:44.497757+03'),
	(28, 2, 2, 'Rolim', 'Bleoramurs', '', 31, 'm', '', '2015-06-14 13:33:44.498104+03', '2015-06-14 13:33:44.498117+03'),
	(29, 2, 2, 'Darthoridan', 'Evawlwyd', '', 18, 'm', '', '2015-06-14 13:33:44.498462+03', '2015-06-14 13:33:44.498475+03'),
	(30, 2, 2, 'Ruvaen', 'Brielydd', '', 21, 'm', '', '2015-06-14 13:33:44.498857+03', '2015-06-14 13:33:44.498877+03'),
	(31, 2, 2, 'Elyamour', 'Phengaine', '', 30, 'm', '', '2015-06-14 13:33:44.499979+03', '2015-06-14 13:33:44.500012+03'),
	(32, 2, 2, 'Tarathiel', 'Blafir', '', 24, 'm', '', '2015-06-14 13:33:44.500948+03', '2015-06-14 13:33:44.500963+03'),
	(33, 2, 2, 'Rolim', 'Brielydd', '', 20, 'm', '', '2015-06-14 13:33:44.50157+03', '2015-06-14 13:33:44.501585+03'),
	(34, 2, 2, 'Thallan', 'Kahevere', '', 20, 'm', '', '2015-06-14 13:33:44.502031+03', '2015-06-14 13:33:44.502045+03'),
	(35, 2, 2, 'Taegen', 'Arthwythi', '', 26, 'm', '', '2015-06-14 13:33:44.502724+03', '2015-06-14 13:33:44.502748+03'),
	(36, 2, 2, 'Vortidred', 'Ettase', '', 25, 'm', '', '2015-06-14 13:33:44.503266+03', '2015-06-14 13:33:44.503283+03');

INSERT INTO "core_match" ("id", "division_id", "round", "season", "can_be_draw", "stadium", "status", "render_progress", "date_scheduled", "created", "modified") VALUES
	(1, 1, NULL, NULL, 'true', NULL, 11, NULL, '2016-06-14 13:34:23+03', '2015-06-14 13:34:30.540248+03', '2015-06-19 01:15:53.726838+03');

INSERT INTO "core_matchteam" ("id", "match_id", "team_id", "role", "points", "reward", "tactics", "tactics_ref", "created", "modified") VALUES
	(1, 1, 1, 'home', 0, 0, '{"players":[{"id":1,"field_zone":"GK","field_position":[0,0],"roles":[]},{"id":2,"field_zone":"LD2","field_position":[0,0],"roles":[]},{"id":3,"field_zone":"CD2","field_position":[0,0],"roles":[]},{"id":4,"field_zone":"RD1","field_position":[0,0],"roles":[]},{"id":5,"field_zone":"LM2","field_position":[0,0],"roles":[]},{"id":6,"field_zone":"CM1","field_position":[0,0],"roles":[]},{"id":7,"field_zone":"CM2","field_position":[0,0],"roles":["captain", "playmaker"]},{"id":8,"field_zone":"CM3","field_position":[0,0],"roles":[]},{"id":9,"field_zone":"RM1","field_position":[0,0],"roles":["field_free_kicks"]},{"id":10,"field_zone":"CA1","field_position":[0,0],"roles":[]},{"id":11,"field_zone":"CA3","field_position":[0,0],"roles":["striker"]}],"relations":[],"substitutions":[]}', '0000000001_C38D41A7EA0DC95DAE18A65507147AD2', '2015-06-14 13:42:02.154531+03', '2015-06-14 14:00:39.163962+03'),
	(2, 1, 2, 'away', 0, 0, '{"players":[{"id":19,"field_zone":"GK","field_position":[0,0],"roles":["captain"]},{"id":20,"field_zone":"LD2","field_position":[0,0],"roles":[]},{"id":21,"field_zone":"CD2","field_position":[0,0],"roles":[]},{"id":22,"field_zone":"RD1","field_position":[0,0],"roles":[]},{"id":23,"field_zone":"LM2","field_position":[0,0],"roles":[]},{"id":24,"field_zone":"CM1","field_position":[0,0],"roles":[]},{"id":25,"field_zone":"CM2","field_position":[0,0],"roles":[]},{"id":26,"field_zone":"CM3","field_position":[0,0],"roles":["playmaker"]},{"id":27,"field_zone":"RM1","field_position":[0,0],"roles":[]},{"id":28,"field_zone":"CA1","field_position":[0,0],"roles":["striker"]},{"id":29,"field_zone":"CA3","field_position":[0,0],"roles":["field_free_kicks"]}],"relations":[],"substitutions":[]}', '0000000001_75DEEA4605A286CA39EEDF1D77D9621B', '2015-06-14 13:43:24.911552+03', '2015-06-14 14:00:49.555927+03');

END $$