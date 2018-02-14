USE `rpg_database`;
alter table `item`
	drop foreign key `item_ibfk_1`;

alter table `item`
	add constraint `item_ibfk_1`
    foreign key (`inventory_id`)
    references `inventory` (`id`)
    ON DELETE CASCADE