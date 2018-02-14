USE `rpg_database`;
ALTER TABLE `trigger`
	DROP FOREIGN KEY `trigger_ibfk_1`;

ALTER TABLE `trigger`
	ADD CONSTRAINT `trigger_ibfk_1`
    FOREIGN KEY (`hero_id`)
    REFERENCES `hero` (`id`)
    ON DELETE CASCADE