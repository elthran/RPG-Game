import pdb

import sqlalchemy.exc


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


class TableQuery:
    def __init__(self, session, meta):
        """Allows quick querying of table.

        This class saves me having to do:
            old_session.query(old_meta.tables['users'])
        and instead do:
            old_table_query('users')
        """
        self.session = session
        self.meta = meta

    def __call__(self, table_name):
        """Return a query on a table object."""

        try:
            smart_query = SmartQuery(self.session.query(self.meta.tables[table_name]), self, table_name)
        except KeyError:
            raise KeyError("No table named '{}' exists.".format(table_name))
        return smart_query

    def join_to_hero(self, result_hero, table_name):
        """Simulates a hero.relationship_name call.

        Allows me to treat a result object like a normal database object.

        e.g.
        Normally you can do:
            hero.journal.id
        But with a table_query object you don't have access to relationships.
        So this lets you do:
            join(hero, 'journal').id
        """
        return self(table_name).filter_by(hero_id=result_hero.id).one()


class SmartQuery:
    def __init__(self, query, table_query, table_name):
        """Improve on querying by returning smarter results.

        Basically hacks into the query result chain and returns an
        enhanced result object.
        """
        self._query = query
        self._table_query = table_query
        self._table_name = table_name

    def __getattr__(self, item):
        """Return an enhanced result object."""

        table_query = self._table_query
        table_name = self._table_name

        class MethodWrapper:
            def __init__(self, method):
                """Hack into query method invocation."""
                self._method = method

            def __call__(self, *args, **kwargs):
                results = self._method(*args, **kwargs)
                if isinstance(results, list):
                    return [SmartResult(result, table_query, table_name) for result in results]
                return SmartResult(results, table_query, table_name)

        return MethodWrapper(getattr(self._query, item))


class SmartResult:
    def __init__(self, result, table_query, table_name):
        """Allow automatic relationship interpolation in table queries.

        Usage:
        old_table_query = TableQuery(old_session, old_meta)
        for old_hero in old_table_query('hero').all():
            old_hero.journal

        This code has automatically recreated the relationship between
        hero and journal and returned the journal object.
        """
        self._result = result
        self._table_query = table_query
        self._table_name = table_name

    def __getattr__(self, item):
        try:
            # in case of normal query on attribute the exists.
            # e.g. hero.name -> returns the hero's name.
            return getattr(self._result, item)
        except AttributeError:
            try:
                other_table = self._table_query(item)
            except KeyError:
                # raise
                import pattern3.text.en
                singular = pattern3.text.en.singularize(item)
                try:
                    other_table = self._table_query(singular)
                except KeyError:
                    raise
                print("Now do extra cool stuff!")
            # In case of valid other table return magic join query
            # hero.journal -> attribute doesn't exist but the
            # journal table has a 'hero_id' return that journal object.
            results = other_table.filter_by(**{self._table_name + "_id": self._result.id}).all()
            if len(results) == 1:
                return results[0]
            return results

