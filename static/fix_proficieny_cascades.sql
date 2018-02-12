USE `rpg_database`;

alter table `proficiency`
	drop foreign key `proficiency_ibfk_1`;

alter table `proficiency`
	add constraint `proficiency_ibfk_1`
    foreign key (`proficiencies_id`)
    references `proficiencies` (`id`)
    ON DELETE CASCADE;