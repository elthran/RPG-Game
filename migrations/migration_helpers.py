def truncate_table(name, engine):
    """Truncate the passed table.

    This will wipe the table and reset the index counter.
    """
    engine.execute("SET FOREIGN_KEY_CHECKS=0;")
    engine.execute("TRUNCATE TABLE `{}`;".format(name))
    engine.execute("SET FOREIGN_KEY_CHECKS=1;")


def truncate_table_keep_some(name, engine, where='', reset_ids=False,
                             no_fk_checks=False):
    """Truncate a table but keep some values.

    Where clause must be valid SQL for a where clause.
    e.g.
    where='template=true'
    Would keep all records where template=true.
    """
    if no_fk_checks:
        engine.execute("SET FOREIGN_KEY_CHECKS=0;")
    engine.execute("RENAME TABLE `{name}` TO `{name}_work`;".format(name=name))
    engine.execute("CREATE TABLE `{name}_backup` AS SELECT * FROM `{name}_work` WHERE {where};".format(name=name, where=where))
    if reset_ids:
        # Sets the ID column in the backup table to 0. As this is the default
        # value ... when it is copied back to the work table .. it will
        # be auto-filled to 1,2,3,4,5 ... apparently. It wan't what I was expecting.
        engine.execute("UPDATE `{name}_backup` SET `id` = 0;".format(name=name))

    engine.execute("TRUNCATE `{name}_work`;".format(name=name))
    engine.execute("LOCK TABLE `{name}_work` WRITE, `{name}_backup` WRITE;".format(name=name))
    engine.execute("INSERT INTO `{name}_work` SELECT * FROM `{name}_backup`;".format(name=name))
    engine.execute("UNLOCK TABLES;".format(name=name))
    engine.execute("RENAME TABLE `{name}_work` TO `{name}`;".format(name=name))
    engine.execute("DROP TABLE `{name}_backup`;".format(name=name))
    if no_fk_checks:
        engine.execute("SET FOREIGN_KEY_CHECKS=1;")


def set_all(old, new, except_=[]):
    """Migrate the data from one object to another."""
    for key in old.keys():
        if key not in except_:
            setattr(new, key, getattr(old, key))
