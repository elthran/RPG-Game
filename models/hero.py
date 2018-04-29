import datetime

import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.ext.hybrid

from game import round_number_intelligently
import models


class Hero(models.mixins.SessionHoistMixin, models.Base):
    """Store data about the Hero/Character object.

    """
    __tablename__ = 'hero'

    id = sa.Column(sa.Integer, primary_key=True)
    creation_phase = sa.Column(sa.Boolean)
    name = sa.Column(sa.String(50))  # Was nullable=False now it isn't. I hope that is a good idea.
    character_name = sa.orm.synonym('name')

    background = sa.Column(sa.String(50))  # Temporary. It's replacing 'fathers job' for now
    age = sa.Column(sa.Integer)
    house = sa.Column(sa.String(50))
    experience = sa.Column(sa.Integer)
    experience_maximum = sa.Column(sa.Integer)
    gold = sa.Column(sa.Integer)

    basic_ability_points = sa.Column(sa.Integer)
    archetype_ability_points = sa.Column(sa.Integer)
    calling_ability_points = sa.Column(sa.Integer)
    pantheon_ability_points = sa.Column(sa.Integer)
    attribute_points = sa.Column(sa.Integer)
    proficiency_points = sa.Column(sa.Integer)

    # All elthran's new code for random stuff
    # Checks if you are currently about to fight a monster
    current_terrain = sa.Column(sa.String(50))
    random_encounter_monster = sa.Column(sa.Boolean)
    spellbook_page = sa.Column(sa.Integer)

    # Time code of when the (account?) was created
    timestamp = sa.Column(sa.DateTime)
    # Date of last login
    last_login = sa.Column(sa.String(50))

    login_alerts = sa.Column(sa.String(200))  # Testing messages when you are attacked or get a new message

    # Relationships
    # User to Hero. One to many. Ordered!
    # Note deleting the user deletes all their heroes!
    account_id = sa.Column(sa.Integer, sa.ForeignKey('account.id', ondelete="CASCADE"))
    account = sa.orm.relationship("Account", back_populates='heroes')

    # Many heroes -> one map/world. (bidirectional)
    map_id = sa.Column(sa.Integer, sa.ForeignKey('location.id', ondelete="SET NULL"))
    current_world = sa.orm.relationship("Location", back_populates='heroes', foreign_keys='[Hero.map_id]')
    # Each current_location -> can be held by Many Heroes (bidirectional)
    current_location_id = sa.Column(sa.Integer, sa.ForeignKey('location.id', ondelete="SET NULL"))
    current_location = sa.orm.relationship(
        "Location", back_populates='heroes_by_current_location',
        foreign_keys='[Hero.current_location_id]')

    # Each current_city -> can be held by Many Heroes (bidirectional)
    # (Town or Cave)
    city_id = sa.Column(sa.Integer, sa.ForeignKey('location.id', ondelete="SET NULL"))
    current_city = sa.orm.relationship(
        "Location", back_populates='heroes_by_city',
        foreign_keys='[Hero.city_id]')

    # When you die, you should return to the last city you were at.
    last_city_id = sa.Column(sa.Integer, sa.ForeignKey('location.id', ondelete="SET NULL"))
    last_city = sa.orm.relationship(
        "Location", back_populates='heroes_by_last_city',
        foreign_keys='[Hero.last_city_id]')

    # Each has a keyed list of abilities.
    # Deleting a Hero deletes all their Abilities.
    abilities = sa.orm.relationship(
        "Ability",
        collection_class=models.attribute_mapped_dict_hybrid('attrib_name'),
        back_populates='hero',
        cascade="all, delete-orphan")

    # Each Hero has One inventory. (One to One -> bidirectional)
    # inventory is list of character's items.
    inventory = sa.orm.relationship("Inventory", back_populates="hero", uselist=False, cascade="all, delete-orphan")

    # Attributes One to One despite the name
    attributes = sa.orm.relationship(
        "Attribute",
        collection_class=models.attribute_mapped_dict_hybrid('attrib_name'),
        back_populates='hero',
        cascade="all, delete-orphan")

    # Hero to Proficiency is One to Many
    base_proficiencies = sa.orm.relationship(
        "Proficiency",
        collection_class=models.attribute_mapped_dict_hybrid('name'),
        back_populates='hero',
        cascade="all, delete-orphan")

    # see http://docs.sqlalchemy.org/en/latest/orm/join_conditions.html#composite-secondary-joins
    # all_proficiencies = sa.orm.relationship(
    #     "Proficiency",
    #     collection_class=attribute_mapped_dict_hybrid('name'),
    #     primaryjoin="join(Hero, Proficiency, Hero.id==Proficiency.hero_id)."
    #                 "join(Hero, Ability, Hero.id==Ability.hero_id)."
    #                 "join(Ability, Proficiency, Ability.id==Proficiency.ability_id)",
    #     cascade="all, delete-orphan",
    # )

    # Journal to Hero is One to One
    journal = sa.orm.relationship('Journal', back_populates='hero', uselist=False, cascade="all, delete-orphan")

    # # Each hero has many Triggers. One to Many
    # triggers = sa.orm.relationship('Trigger', secondary='trigger_to_hero',
    #                         back_populates='heroes')

    # Hero to Handlers is One to Many.
    handlers = sa.orm.relationship('Handler', back_populates='hero', cascade="all, delete-orphan")

    # @eltran ... this probably won't work as the var will disappear on
    # database reload.
    # variable used for keeping track of clicked attributes on the user table
    clicked_user_attribute = ""

    # noinspection PyUnusedLocal
    @sa.orm.validates('current_world')
    def validate_current_world(self, key, value):
        if 'map' == value.type:
            return value
        raise Exception("'current_world' Location type must be 'map' not '{}'."
                        "".format(value.type))

    # Hero to Specializations relationship - One to Many
    # These relationships can be modified through the 'specializations'
    # container.
    _specializations = sa.orm.relationship(
        "Specialization",
        collection_class=models.attribute_mapped_dict_hybrid("attrib_name"),
        back_populates="hero",
        cascade="all, delete-orphan")
    # Hero to Calling is One to One
    _calling = sa.orm.relationship(
        "Specialization",
        primaryjoin="and_(Hero.id==Specialization.hero_id, "
                    "Specialization.type=='Calling')",
        back_populates="hero",
        uselist=False,
        cascade="all, delete-orphan")
    # Hero to Archetype is One to One
    _archetype = sa.orm.relationship(
        "Specialization",
        primaryjoin="and_(Hero.id==Specialization.hero_id, "
                    "Specialization.type=='Archetype')",
        uselist=False,
        back_populates="hero",
        cascade="all, delete-orphan")
    # Hero to Pantheon is One to One.
    _pantheon = sa.orm.relationship(
        "Specialization",
        primaryjoin="and_(Hero.id==Specialization.hero_id, "
                    "Specialization.type=='Pantheon')",
        uselist=False,
        back_populates="hero",
        cascade="all, delete-orphan")

    @sa.ext.hybrid.hybrid_property
    def specializations(self):
        """Wrapper for the hero Specialziation objects.

        These variables can be accessed via:
        for obj in hero.specializations:
            print(obj)
        -> all (Container)
        -> archetype object
        -> calling object
        -> pantheon object

        hero.specializations.archetype
        hero.specializations.calling
        hero.specializations.pantheon
        hero.specializations.all

        hero.specializations.all is a container class too! So you can do:
        for obj in hero.specializations.all:
            print(obj)
        To print out _all_ Specialization objects attached to this hero.

        also:
        hero.specializations.all.brute -> if this hero has Brute Spec.
        """

        collection = models.DictHybrid(key_attr='attrib_name')
        collection['all'] = self._specializations
        collection['archetype'] = self._archetype
        collection['calling'] = self._calling
        collection['pantheon'] = self._pantheon
        return collection

    @specializations.setter
    def specializations(self, value):
        """Update the specializations classes relationships.

        If passing a template ... make a new value an use that instead.

        You can add a new object to the hero via. I know that that is a bit
        counter-intuitive but hey ... it works.
            hero.specializations = specialization

        To remove an object from the hero do:
            hero.specializations.archetype.hero = None
        This will set the objects hero to None which will remove it from this
        hero. I'm not sure if doing hero.specializations.archetype = None
        will have any effect.
        """
        if value.template:
            getattr(models.specializations, value.name)().hero = self
        else:
            value.hero = self

    def __init__(self, **kwargs):
        """Initialize the Hero object.

        Currently only accepts keywords. Consider changing this.
        Consider having some Non-null values?

        exp_percent is now updated by current_exp using a validator.
        max_exp should be assigned a value before current_exp.
        """

        # Add all attributes to hero.
        for cls_name in models.attributes.ALL_CLASS_NAMES:
            # noinspection PyPep8Naming
            AttributeClass = getattr(models.attributes, cls_name)
            AttributeClass().hero = self

        # set self.base_proficiencies
        # e.g.
        # import proficiencies
        # Class = proficiencies.Accuracy
        # obj = Accuracy()
        # accuracy.hero = self (current hero object)
        # hero.base_proficiencies['accuracy'] = Accuracy()
        for cls_name in models.proficiencies.ALL_CLASS_NAMES:
            # attributes.Attribute
            # noinspection PyPep8Naming
            ProfClass = getattr(models.proficiencies, cls_name)
            ProfClass().hero = self

        self.base_proficiencies['endurance'].current = self.base_proficiencies['endurance'].final

        # Attach one of each Ability to hero.
        for cls_name in models.abilities.ALL_CLASS_NAMES:
            # noinspection PyPep8Naming
            AbilityClass = getattr(models.abilities, cls_name)
            AbilityClass().hero = self

        # Attach one of each Specialization to hero.
        for cls_name in models.specializations.ALL_CLASS_NAMES:
            # noinspection PyPep8Naming
            Class = getattr(models.specializations, cls_name)
            obj = Class()
            if obj.type == "Specialization":
                obj.hero = self

        self.inventory = models.Inventory()
        self.journal = models.Journal()

        # Data and statistics
        self.age = 7
        # self.archetype = None
        # self.calling = SpecializationContainer()
        # self.pantheon = SpecializationContainer()
        self.house = None
        self.experience_percent = 0
        self.experience = 0
        self.experience_maximum = 10
        self.gold = 50

        # Spendable points
        self.basic_ability_points = 0
        self.archetype_ability_points = 0
        self.calling_ability_points = 0
        self.pantheon_ability_points = 0
        self.attribute_points = 0
        self.proficiency_points = 0

        # Achievements and statistics
        self.current_terrain = "city"
        self.random_encounter_monster = None
        self.spellbook_page = 1

        # Time code and login alerts
        self.timestamp = datetime.datetime.utcnow()
        self.last_login = ""
        self.login_alerts = "testing"

        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.refresh_character(full=True)
        self.init_on_load()

    @sa.orm.reconstructor
    def init_on_load(self):
        """Runs when the database is reload and at the end of __init__.
        """
        # I don't even know if this is supposed to be rebuilt? (Marlen)
        # self.refresh_proficiencies()

        # resets experience_percent
        self.experience = self.experience

    # noinspection PyUnusedLocal
    @sa.orm.validates('experience')
    def validate_experience(self, key_name, current):
        # Update experience percent on experience change.
        try:
            self.experience_percent = min(round(current / self.experience_maximum, 2) * 100, 100)
        except (TypeError, ZeroDivisionError):
            self.experience_percent = 0
        return max(current or 0, 0)

    def get_summed_proficiencies(self, key_name=None):
        """Summed value of all derivative proficiency objects.

        Returns a Map object. This is a virtual object dictionary.

        Should allow you to do this:
            hero.get_summed_proficiencies()['defence'].modifier
            hero.get_summed_proficiencies()['defence'].get_final_value()
            hero.get_suumed_proficiencies()['defence'].percent

        OR
            hero.get_summed_proficiencies().defence.modifier
        OR (more efficiently)
            hero.get_summed_proficiencies('defence').modifier

        NOTE: the value of get_summed_proficiencies is saved in the
        hero.proficiencies attribute.
        This can be used for much increase efficiency. Since each call of
        get_summed_proficiencies() rechecks _all_ proficiencies.
        The more efficient way is to do it once and then call
            hero.proficiencies afterwards. Until you need to recheck.
        You can also recheck just one value using:
            get_summed_proficiencies(key_name='defence')

        """

        all_other_proficiencies = self.equipped_items() + [obj for obj in self.abilities if obj.level]

        summed = {}
        if key_name:
            prof = self.base_proficiencies[key_name]

            # outside_profs = self.session.query(
            #     proficiencies.Proficiency).filter_by(type_=prof.type_, hero_id=None)
            # outside_profs += self.session.query(
            #     proficiencies.Proficiency).filter_by(type_=prof.type_, hero_id=self.id)
            # outside_profs += self.session.query(
            #     proficiencies.Proficiency).filter_by(type_=prof.type_, ability_id=self.id)
            # print("Before printing profs!")
            # for prof in outside_profs:
            #     print(prof.name)
            # print("After printing profs!")
            # exit()

            summed[prof.name] = [prof.level, prof.base, prof.modifier, prof.type_]
            # print(self.session.query(proficiencies.Proficiency).)
            # pdb.set_trace()
            for obj in all_other_proficiencies:
                try:
                    prof = obj.proficiencies[key_name]
                except KeyError:
                    continue
                if prof.name in summed:
                    current_level, current_base, current_modifier, type_ = summed[prof.name]
                    summed[prof.name] = [current_level + prof.level,
                                         current_base + prof.base,
                                         current_modifier + prof.modifier,
                                         type_]
                else:
                    summed[prof.name] = [prof.level, prof.base, prof.modifier, prof.type_]

            lvl, base, mod, type_ = summed[key_name]

            # convert dict of values into dict of database objects
            # noinspection PyPep8Naming
            Class = getattr(models.proficiencies, type_)
            summed[key_name] = Class(level=lvl, base=base, modifier=mod)
            summed[key_name].current = self.base_proficiencies[key_name].current

            # If proficiencies exists update it. If not just return this
            # mapped object.
            try:
                self.proficiencies[key_name] = summed[key_name]
            except AttributeError:
                pass
            return summed[key_name]
        else:  # Get the latest combined values of all proficiencies!
            for prof in self.base_proficiencies:
                summed[prof.name] = [prof.level, prof.base, prof.modifier,
                                     prof.type_]

            for obj in all_other_proficiencies:
                for prof in obj.proficiencies:
                    if prof.name in summed:
                        # Add 1st to 1st, 2nd to 2nc etc.
                        # Drops the type which we add back in afterwards.
                        summed[prof.name] = [sum(v) for v in zip(
                            summed[prof.name],
                            [prof.level, prof.base, prof.modifier])]
                        summed[prof.name].append(prof.type_)
                    else:
                        summed[prof.name] = [prof.level, prof.base,
                                             prof.modifier, prof.type_]

            for key in summed:
                lvl, base, mod, type_ = summed[key]

                # noinspection PyPep8Naming
                Class = getattr(models.proficiencies, type_)
                summed[key] = Class(level=lvl, base=base, modifier=mod)
                summed[key].current = self.base_proficiencies[key].current
            # noinspection PyAttributeOutsideInit
            self.proficiencies = models.DictHybrid(summed, key_attr='name')
            return self.proficiencies

    def refresh_proficiencies(self):
        pass
        # for proficiency in self.proficiencies:
        #     proficiency.update(self)

    def refresh_character(self, full=False):
        # self.refresh_proficiencies()
        if full:
            self.base_proficiencies['health'].current = \
                self.base_proficiencies['health'].final
            self.base_proficiencies['sanctity'].current = \
                self.base_proficiencies['sanctity'].final
            self.base_proficiencies['endurance'].current = \
                self.base_proficiencies['endurance'].final

    # I dont think this is needed if the validators are working?
    # I don't think I ever call this function and the bar seems
    # to be updating properly
    def update_experience_bar(self):
        self.experience_percent = round(self.experience / self.experience_maximum, 2) * 100

    def gain_experience(self, amount):
        new_amount = amount * (1 + self.get_summed_proficiencies('understanding').final / 100)  # Each value of understanding should add 1% exp gained
        new_amount = round_number_intelligently(new_amount)
        self.experience += new_amount
        if self.experience >= self.experience_maximum:
            self.experience -= self.experience_maximum
            self.experience_maximum += 5
            self.attribute_points += 1
            self.proficiency_points += 1
            self.basic_ability_points += 1
            self.archetype_ability_points += 1
            self.age += 1
            self.refresh_character(full=True)
        return new_amount  # This way you can just run this function anytime you want to add exp, it calculates your modifiers and updates, then returns the value in case you want to print it

    def equipped_items(self):
        return self.inventory.equipped or []  # Might work without OR.

    def non_equipped_items(self):
        return self.inventory.unequipped or []

    def consume_item(self, item_name):
        for my_item in self.inventory:
            if my_item.name == item_name:
                my_item.apply_effect()
                my_item.amount_owned -= 1
                if my_item.amount_owned == 0:
                    self.inventory.remove(my_item)
                break

                # @validates('current_city')
                # def validate_current_city(self, key, location):
                # """Assert that current_city is in fact a city.

                # Also allow current_city to be None.
                # """
                # try:
                # assert location.type in ("Cave", "Town")
                # return location
                # except AttributeError:
                # assert location is None
                # return None

    def check_daily_login_reward(self, time):
        if self.last_login == "":
            self.login_alerts += "First time logging in!"
            print("first time log in EVER (printed from game.py)")
        elif self.last_login != time[:10]:
            reward = 3
            self.login_alerts += "Thanks for logging in today! You earn " + str(
                reward) + " experience."
            self.gain_experience(reward)
            print("first time log in TODAY (printed from game.py)")
        else:
            print("you have already logged in today (printed from game.py)")
        self.last_login = time[:10]

    # noinspection PyUnusedLocal
    @sa.orm.validates('current_location')
    def validate_current_location(self, key, location):
        """Updates value of current_city on assignment.

        If current_location is a city ... set value of current_city as well.
        If not remove the value of current_city.
        """
        if location.type in ("cave", "town"):
            self.current_city = location

        # So the game remembers your last visited city
        if location.type == 'town':
            self.last_city = location
        if location.type == 'map':
            self.current_world = location
        return location

    def get_other_heroes_at_current_location(self):
        """Return a list of heroes at the same location as this one.

        Note including self.
        This is probably inefficient ...
        """
        return [hero
                for hero in self.current_location.heroes_by_current_location
                if self.id != hero.id]


if __name__ == "__main__":
    import os
    os.system("python3 -m pytest -vv rpg_game_tests/test_{}".format(__file__))
