# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from .models import db


def insert_players_temp():
    trigger_sql = text("""
    CREATE TRIGGER IF NOT EXISTS `insert_players_temp` AFTER INSERT ON `players`
    FOR EACH ROW INSERT INTO `players_temp` (`url`, `id`) VALUES (NEW.`url`, NEW.`id`);
    """)

    db.session.execute(trigger_sql)
    db.session.commit()


def update_teammate_ids():
    procedure_sql = text("""
    CREATE PROCEDURE IF NOT EXISTS update_teammate_ids()
    BEGIN
        DECLARE url_val VARCHAR(191);
        DECLARE id_val INT;

        DECLARE done BOOLEAN DEFAULT FALSE;

        DECLARE player_cursor CURSOR FOR SELECT url, id FROM players_temp;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

        OPEN player_cursor;

        read_loop: LOOP
            FETCH player_cursor INTO url_val, id_val;
            IF (done) THEN
                LEAVE read_loop;
            END IF;

            UPDATE players SET teammate_id = id_val WHERE teammate_url = url_val;
        END LOOP;

        CLOSE player_cursor;
        
        DELETE FROM players_temp;
    END
    """)

    db.session.execute(procedure_sql)
    db.session.commit()


def update_tournaments_ids():
    procedure_sql = text("""
    CREATE PROCEDURE IF NOT EXISTS update_tournaments_ids()
    BEGIN
        DECLARE done INT DEFAULT FALSE;
        DECLARE tournament_url_val VARCHAR(300);
        DECLARE tournament_id_val INT;
        DECLARE cur CURSOR FOR SELECT url_tournament FROM tournaments_results;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

        OPEN cur;
        read_loop: LOOP
            FETCH cur INTO tournament_url_val;
            IF done THEN
                LEAVE read_loop;
            END IF;

            SELECT id INTO tournament_id_val FROM tournaments WHERE url = tournament_url_val;

            UPDATE tournaments_results
            SET tournament_id = tournament_id_val
            WHERE url_tournament = tournament_url_val;
        END LOOP;

        CLOSE cur;
    END
    """)

    db.session.execute(procedure_sql)
    db.session.commit()


def normalization_tournaments_results():
    procedure_sql = text("""
    CREATE PROCEDURE IF NOT EXISTS normalization_tournaments_results()
    BEGIN
        DECLARE done INT DEFAULT FALSE;
        DECLARE cur CURSOR FOR SELECT url_tournament FROM tournaments_results;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

        OPEN cur;
        read_loop: LOOP
            FETCH cur INTO tournament_url_val;
            IF done THEN
                LEAVE read_loop;
            END IF;

            SELECT id INTO tournament_id_val FROM tournaments WHERE url = tournament_url_val;

            UPDATE tournaments_results
            SET tournament_id = tournament_id_val
            WHERE url_tournament = tournament_url_val;
        END LOOP;

        CLOSE cur;
    END
    """)

    db.session.execute(procedure_sql)
    db.session.commit()


def update_tournaments_results():
    procedure_sql = text("""
    CREATE PROCEDURE IF NOT EXISTS update_tournaments_results()
    BEGIN
        UPDATE tournaments_results
        SET
            player1_couple1_id = (SELECT id FROM players WHERE url = url_player1_couple1),
            player2_couple1_id = (SELECT id FROM players WHERE url = url_player2_couple1),
            player1_couple2_id = (SELECT id FROM players WHERE url = url_player1_couple2),
            player2_couple2_id = (SELECT id FROM players WHERE url = url_player2_couple2);
    END
    """)

    db.session.execute(procedure_sql)
    db.session.commit()


def normalization_names():
    procedure_sql = text("""
    CREATE PROCEDURE IF NOT EXISTS normalization_names()
    BEGIN  
        DECLARE name_val VARCHAR(191);
        DECLARE id_val INT;
        DECLARE c CHAR(1);  
        DECLARE s VARCHAR(255);  
        DECLARE i INT DEFAULT 1;  
        DECLARE bool INT DEFAULT 1;  
        DECLARE punct CHAR(17) DEFAULT ' ()[]{},.-_!@;:?/';  
        DECLARE done BOOLEAN DEFAULT FALSE;
        DECLARE player_cursor CURSOR FOR SELECT name, id FROM players;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

        OPEN player_cursor;

        read_loop: LOOP
            FETCH player_cursor INTO name_val, id_val;
            IF (done) THEN
                LEAVE read_loop;
            END IF;
            
            -- Convert name to lowercase and capitalize the first letter
            SET s = LOWER(name_val);
            SET s = CONCAT(UCASE(SUBSTRING(s, 1, 1)), SUBSTRING(s, 2));

            WHILE i < LENGTH(s) DO
                BEGIN
                    SET c = SUBSTRING(s, i, 1);

                    IF LOCATE(c, punct) > 0 THEN
                        SET bool = 1;
                    ELSEIF bool = 1 THEN
                        BEGIN
                            -- Capitalize the first letter of each word
                            IF c >= 'a' AND c <= 'z' THEN
                                BEGIN
                                    SET s = CONCAT(
                                        LEFT(s, i - 1),
                                        UCASE(c),
                                        SUBSTRING(s, i + 1)
                                    );
                                    SET bool = 0;
                                END;
                            ELSEIF c >= '0' AND c <= '9' THEN
                                SET bool = 0;
                            END IF;
                        END;
                    ELSE
                        SET bool = 0;
                    END IF;

                    SET i = i + 1;
                END;
            END WHILE;
                
            -- Update the name column with the modified value
            UPDATE players SET name = s WHERE id = id_val;
            SET i = 1; -- Reset the value of i for the next iteration

        END LOOP;

        CLOSE player_cursor;
        
        DELETE FROM players_temp;
    END
    """)

    db.session.execute(procedure_sql)
    db.session.commit()


def update_competitions_last_updated():
    procedure_sql = text("""
    CREATE EVENT IF NOT EXISTS update_competitions_last_updated
    ON SCHEDULE EVERY 1 DAY
    DO
      UPDATE competitions SET last_update = current_date();
    """)

    db.session.execute(procedure_sql)
    db.session.commit()
