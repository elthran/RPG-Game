import pdb

import sqlalchemy.exc
import sqlalchemy.orm


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

        # TODO figure out how to handle filter_by?
        """
        self._query = query
        self._table_query = table_query
        self.table_name = table_name

    def __getattr__(self, item):
        """Return an enhanced result object."""

        table_query = self._table_query
        table_name = self.table_name

        class MethodWrapper:
            def __init__(self, method):
                """Hack into query method invocation."""
                self._method = method

            def __call__(self, *args, **kwargs):
                # if item == 'filter_by': pdb.set_trace()
                results = self._method(*args, **kwargs)
                if isinstance(results, sqlalchemy.orm.query.Query):
                    return SmartQuery(results, table_query, table_name)
                if isinstance(results, list):
                    return [SmartResult(entry, table_query, table_name) for entry in results]
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

        I did briefly use Pattern3
        import pattern.text.en

        # user.heroes
        pattern.text.en.singularize('heroes')
        To detect whether I should return an item or a list but decided
        it was to much overhead :P

        Usage:
        obj = old_table_query('hero').first()
        print(obj.user) -> singular user object.
        obj = old_table_query('user').first()
        print(obj.hero) -> all heroes of that user as a list.
        """
        self._result = result
        self._table_query = table_query
        self._table_name = table_name

    def __getattr__(self, item):
        try:
            # in case of normal query on attribute the exists.
            # e.g. hero.name -> returns the hero's name.
            return getattr(self._result, item)
        except AttributeError as original_attrib_error:
            try:
                other_table = self._table_query(item)
            except KeyError:
                # I guess they were looking for an attribute and it doesn't
                # exist.
                raise original_attrib_error
            # In case of valid other table return magic join query
            # hero.journal -> attribute doesn't exist but the
            # journal table has a 'hero_id' return that journal object.
            # user.hero -> detect one to many relationship and return a list
            # of heroes.
            try:
                results = other_table.filter_by(**{self._table_name + "_id": self._result.id}).all()
            except sqlalchemy.exc.InvalidRequestError:
                # Try the inverse relationship many to one
                # hero.user -> detect many to one and return a single user.
                # hero.user -> User.query.filter_by(id=hero.user_id).one()
                try:
                    local_id = getattr(self._result, other_table.table_name + "_id")
                except AttributeError:
                    raise original_attrib_error
                try:
                    results = other_table.filter_by(**{"id": local_id}).one()
                except sqlalchemy.exc.InvalidRequestError:
                    raise  # I'm not sure what this should raise ...
            return results

    def __len__(self):
        return 1

    def __repr__(self):
        return repr(self._result)

