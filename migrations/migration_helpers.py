import sqlalchemy


def truncate_table(name, engine):
    """Truncate the passed table.

    This will wipe the table and reset the index counter.
    """
    engine.execute("SET FOREIGN_KEY_CHECKS=0;")
    engine.execute("TRUNCATE TABLE `{}`;".format(name))
    engine.execute("SET FOREIGN_KEY_CHECKS=1;")


def truncate_table_keep_some(name, engine, where='', reset_ids=False, no_fk_checks=False):
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


def reset_table_ids_and_autoincrement(name, engine):
    """Reset the id values in a table and reset the autoincrement.

    This is done by cloning the table resetting the ids then copying back to
    the original.

    I will probably make use less duplication at some point.
    I wonder if I can execute multiple statements with one execute?
    """
    engine.execute("RENAME TABLE `{name}` TO `{name}_work`;".format(name=name))
    engine.execute("CREATE TABLE `{name}_backup` AS SELECT * FROM `{name}_work`".format(name=name))
    try:
        engine.execute("UPDATE `{name}_backup` SET `id` = 0;".format(name=name))
    except sqlalchemy.exc.OperationalError as ex:
        if "Unknown column 'id' in 'field list'" in str(ex):
            pass
        else:
            raise ex
    engine.execute("TRUNCATE `{name}_work`;".format(name=name))
    engine.execute("LOCK TABLE `{name}_work` WRITE, `{name}_backup` WRITE;".format(name=name))
    engine.execute("INSERT INTO `{name}_work` SELECT * FROM `{name}_backup`;".format(name=name))
    engine.execute("UNLOCK TABLES;".format(name=name))
    engine.execute("RENAME TABLE `{name}_work` TO `{name}`;".format(name=name))
    engine.execute("DROP TABLE `{name}_backup`;".format(name=name))
    # Set increment. NOTE: since the increment must be higher than the highest
    # id column value ... this will set it to the right value.
    # It won't set it to 1 necessarily .. but to the 'row count + 1'.
    engine.execute("ALTER TABLE `{name}` AUTO_INCREMENT = 1;".format(name=name))


def set_all(old, new, except_=()):
    """Migrate the data from one object to another."""
    for key in old.keys():
        if key not in except_:
            setattr(new, key, getattr(old, key))
