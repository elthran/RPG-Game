import math
import random
import datetime
import pdb

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from sqlalchemy.orm import validates
from sqlalchemy.orm.collections import attribute_mapped_collection

from attributes import AttributeContainer
from abilities import AbilityContainer
import proficiencies
from inventory import Inventory
from journal import Journal
from specializations import SpecializationContainer
from session_helpers import SessionHoistMixin
from base_classes import Base, Map


class Hero(SessionHoistMixin, Base):
    """Store data about the Hero/Character object.

    """
    __tablename__ = 'hero'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))  # Was nullable=False now it isn't. I hope that is a good idea.
    character_name = orm.synonym('name')

    background = Column(String(50)) # Temporary. It's replacing 'fathers job' for now
    age = Column(Integer)
    house = Column(String(50))
    experience = Column(Integer)
    experience_maximum = Column(Integer)
    renown = Column(Integer)  # How famous you are
    virtue = Column(Integer)  # How good/evil you are
    devotion = Column(Integer)  # How religious you are
    gold = Column(Integer)

    basic_ability_points = Column(Integer)
    archetype_ability_points = Column(Integer)
    calling_ability_points = Column(Integer)
    pantheon_ability_points = Column(Integer)
    attribute_points = Column(Integer)
    proficiency_points = Column(Integer)

    # All elthran's new code for random stuff
    current_terrain = Column(String(50))
    deepest_dungeon_floor = Column(Integer)  # High score for dungeon runs
    current_dungeon_floor = Column(Integer)  # Which floor of dungeon your on
    current_dungeon_floor_progress = Column(
        Integer)  # Current progress in current cave floor
    random_encounter_monster = Column(
        Boolean)  # Checks if you are currently about to fight a monster
    player_kills = Column(Integer)
    monster_kills = Column(Integer)
    deaths = Column(Integer)

    # Time code of when the (account?) was created
    timestamp = Column(DateTime)
    # Date of last login
    last_login = Column(String(50))

    login_alerts = Column(String(50))  # Testing messages when you are attacked or get a new message

    # Relationships
    # User to Hero. One to many. Ordered!
    # Note deleting the user deletes all their heroes!
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    user = relationship("User", back_populates='heroes')

    # Many heroes -> one map/world. (bidirectional)
    map_id = Column(Integer, ForeignKey('location.id', ondelete="SET NULL"))
    current_world = relationship("Location", back_populates='heroes',
                                 foreign_keys='[Hero.map_id]')
    # Each current_location -> can be held by Many Heroes (bidirectional)
    current_location_id = Column(Integer, ForeignKey('location.id',
                                                     ondelete="SET NULL"))
    current_location = relationship(
        "Location", back_populates='heroes_by_current_location',
        foreign_keys='[Hero.current_location_id]')

    # Each current_city -> can be held by Many Heroes (bidirectional)
    # (Town or Cave)
    city_id = Column(Integer, ForeignKey('location.id', ondelete="SET NULL"))
    current_city = relationship(
        "Location", back_populates='heroes_by_city',
        foreign_keys='[Hero.city_id]')

    # When you die, you should return to the last city you were at.
    last_city_id = Column(Integer, ForeignKey('location.id',
                                              ondelete="SET NULL"))
    last_city = relationship(
        "Location", back_populates='heroes_by_last_city',
        foreign_keys='[Hero.last_city_id]')

    # Each hero can have one set of Abilities. (bidirectional, One to One).
    # Deleting a Hero deletes all their Abilities.
    abilities = relationship("AbilityContainer",
                             uselist=False, back_populates='hero',
                             cascade="all, delete-orphan")

    # Hero to specializations relationship
    specializations = relationship(
        "SpecializationContainer", back_populates="hero", uselist=False,
        cascade="all, delete-orphan")

    # Each Hero has One inventory. (One to One -> bidirectional)
    # inventory is list of character's items.
    inventory = relationship("Inventory", back_populates="hero", uselist=False,
                             cascade="all, delete-orphan")

    # Attributes One to One despite the name
    attributes = relationship(
        "AttributeContainer", back_populates='hero', uselist=False,
        cascade="all, delete-orphan")

    # Hero to Proficiency is One to Many
    base_proficiencies = relationship(
        "Proficiency",
        collection_class=attribute_mapped_collection('name'),
        back_populates='hero',
        cascade="all, delete-orphan")

    # all_proficiencies = relationship(
    #     "Proficiency",
    #     collection_class=attribute_mapped_collection('name'),
    #     primaryjoin="and_(Ability.id==Proficiency.ability_id, "
    #                 "AbilityContainer.id==Ability.ability_container_id, "
    #                 "Hero.id==AbilityContainer.hero_id)",
    #     cascade="all, delete-orphan",
    # )

    # Journal to Hero is One to One
    journal = relationship('Journal', back_populates='hero', uselist=False,
                           cascade="all, delete-orphan")

    # Many to one with Triggers, Each hero has many triggers.
    triggers = relationship('Trigger', back_populates='hero',
                            cascade="all, delete-orphan")

    # @eltran ... this probably won't work as the var will disappear on
    # database reload.
    # variable used for keeping track of clicked attributes on the user table
    clicked_user_attribute = ""

    @orm.validates('current_world')
    def validate_current_world(self, key, value):
        if 'map' == value.type:
            return value
        raise Exception("'current_world' Location type must be 'map' not '{}'."
                        "".format(value.type))

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
        get_summed_proficiencies() rechecks _all_ proficiecies.
        The more efficient way is to do it once and then call
            hero.proficiencies afterwards. Until you need to recheck.
        You can also recheck just one value using:
            get_summed_proficiencies(key_name='defence')

        """
        summed = {}
        if key_name:
            prof = self.base_proficiencies[key_name]
            summed[prof.name] = [prof.level, prof.base, prof.modifier, prof.type_]
            # print(self.session.query(proficiencies.Proficiency).)
            # pdb.set_trace()
            for obj in self.equipped_items() + [obj for obj in self.abilities
                                                if obj.level]:
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
            Class = getattr(proficiencies, type_)
            summed[key_name] = Class(level=lvl, base=base, modifier=mod)

            # If proficiencies exists update it. If not just return this
            # mapped object.
            try:
                self.proficiencies[key_name] = summed[key_name]
            except AttributeError:
                pass
            return summed[key_name]
        else:  # Get the latest combined values of all proficiencies!
            for key in self.base_proficiencies:
                prof = self.base_proficiencies[key]
                summed[prof.name] = [prof.level, prof.base, prof.modifier, prof.type_]

            for obj in self.equipped_items() + [obj for obj in self.abilities]:
                for key in obj.proficiencies:
                    prof = obj.proficiencies[key]
                    if prof.name in summed:
                        current_level, current_base, current_modifier, type_ = summed[prof.name]
                        summed[prof.name] = [current_level + prof.level,
                                             current_base + prof.base,
                                             current_modifier + prof.modifier,
                                             type_]
                    else:
                        summed[prof.name] = [prof.level, prof.base, prof.modifier, prof.type_]

            for key in summed:
                lvl, base, mod, type_ = summed[key]

                Class = getattr(proficiencies, type_)
                summed[key] = Class(level=lvl, base=base, modifier=mod)
            self.proficiencies = Map(summed)
            return self.proficiencies

    def __init__(self, **kwargs):
        """Initialize the Hero object.

        Currently only accepts keywords. Consider changing this.
        Consider having some Non-null values?

        exp_percent is now updated by current_exp using a validator.
        max_exp should be assigned a value before current_exp.
        """

        # Skills and abilities
        self.attributes = AttributeContainer()  # Must go above proficiencies

        # set self.base_proficiencies
        # e.g.
        # import proficiencies
        # Class = proficiencies.Accuracy
        # obj = Accuracy()
        # accuracy.hero = self (current hero object)
        # hero.base_proficiencies['accuracy'] = Accuracy()
        for cls_name in proficiencies.ALL_CLASS_NAMES:
            # attributes.Attribute
            ProfClass = getattr(proficiencies, cls_name)
            if not ProfClass.hidden:
                ProfClass().hero = self

            # obj = Class()
            # obj.hero = self
            # OR
            # self.base_proficiencies[obj.name] = obj

        self.abilities = AbilityContainer()
        self.inventory = Inventory()
        self.journal = Journal()
        self.specializations = SpecializationContainer()

        # Data and statistics
        self.age = 7
        # self.archetype = None
        # self.calling = SpecializationContainer()
        # self.pantheon = SpecializationContainer()
        self.house = None
        self.background = ""
        self.experience_percent = 0
        self.experience = 0
        self.experience_maximum = 10
        self.renown = 0
        self.virtue = 0
        self.devotion = 0
        self.gold = 50

        # Spendable points
        self.basic_ability_points = 5
        self.archetype_ability_points = 0
        self.calling_ability_points = 0
        self.pantheon_ability_points = 0
        self.attribute_points = 0
        self.proficiency_points = 0

        # Achievements and statistics
        self.current_terrain = "city"
        self.deepest_dungeon_floor = 0
        self.current_dungeon_floor = 0
        self.current_dungeon_floor_progress = 0
        self.random_encounter_monster = None
        self.player_kills = 0
        self.monster_kills = 0
        self.deaths = 0

        # Time code and login alerts
        self.timestamp = datetime.datetime.utcnow()
        self.last_login = ""
        self.login_alerts = "testing"

        for key in kwargs:
            setattr(self, key, kwargs[key])

        self.refresh_character(full=True)
        self.init_on_load()

    @orm.reconstructor
    def init_on_load(self):
        """Runs when the database is reload and at the end of __init__.
        """
        # I don't even know if this is supposed to be rebuilt? (Marlen)
        self.refresh_proficiencies()

        # resets experience_percent
        self.experience = self.experience

    @validates('experience')
    def validate_experience(self, key_name, current):
        # Update experience percent on experience change.
        try:
            self.experience_percent = min(round(current / self.experience_maximum, 2) * 100, 100)
        except (TypeError, ZeroDivisionError):
            self.experience_percent = 0
        return max(current or 0, 0)

    # def not_yet_implemented(self):
    #     self.kill_quests = BaseDict()
    #     self.chest_equipped = []
    #     self.errands = []
    #     self.completed_quests = []
    #     self.completed_achievements = []
    #     self.bestiary = []
    #     self.wolf_kills = 0

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
        new_amount = amount * self.get_summed_proficiencies('understanding').final
        new_amount = int(new_amount) + (random.random() < new_amount - int(new_amount)) # This will round the number weighted by its decimal (so 1.2 has 20% chance of rounding up)
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
        return new_amount

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

    @validates('current_location')
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
