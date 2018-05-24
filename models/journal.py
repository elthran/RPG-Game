"""
Journal specification.

A journal should be able to store data on (triggered events).
Such as quest completion or beast encountered or map areas explored.

    A database table linking to object data.
    A comment on each event.

e.g. #1
    Quest Log
    -"Get acquainted with the Blacksmith Quest" completed @ 15:30 - 2017/11/08

    (click quest name to get more info about the quest)

e.g. #2
    Map Log
    -Found Blacksmith in Thornwall @ 15:25 - 2017/11/08

    (Click location names for more info)

So maybe:
    -object
    -info/description of event
    -time + date

Journal is almost a Frontend for lots of other objects?

Project breakdown:

1. Design backend for quests
    -build to allow for type checking/instanceOf checking
    -build to allow quest_path.description property
    -build to describe what happens when you click on the current quest in a
        quest_path. I quest it would bring up info on the current quest?

2. Design backend for persons
3. Design backend for places
4. Design backend for beasts

5. Design frontend for quests
    -pull data from the current quest in the questpath and the questpath itself
6. Design frontend for person
7. Design frontend for places
8. Design frontend for beasts

9. Design event system link-in.
    -Journal entries should be populated by the occurrence of events
"""

import flask
import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.ext.hybrid
import sqlalchemy.ext.orderinglist

import models
import models.achievements


# For testing

# journal_quest_path_association_table = Table(
#     'journal_quest_path_association',
#     Base.metadata,
#     Column('journal_id', Integer, ForeignKey('journal.id',
#                                              ondelete="SET NULL")),
#     Column('quest_path_id', Integer, ForeignKey('quest_path.id',
#                                                 ondelete="SET NULL"))
# )

journal_to_location = sa.Table(
    'journal_to_location', models.Base.metadata,
    sa.Column('journal_id', sa.Integer, sa.ForeignKey('journal.id', ondelete="SET NULL")),
    sa.Column('location_id', sa.Integer, sa.ForeignKey('location.id', ondelete="SET NULL"))
)


# I think I can combine the entry and Journal.
# This would give me custom places such as beasts or quests in the Journal
# The add_entry would sort the new objects into the right category.
class Journal(models.Base):
    # Relationships
    # Hero to Journal is One to One
    hero_id = sa.Column(sa.Integer, sa.ForeignKey('hero.id', ondelete="CASCADE"))
    hero = sa.orm.relationship(
        "Hero",
        back_populates='journal',
        cascade="all, delete-orphan",
        single_parent=True)

    # Journal to QuestPath is One to Many
    # QuestPath provides many special methods.
    quest_paths = sa.orm.relationship("QuestPath", back_populates='journal', cascade="all, delete-orphan", foreign_keys="[QuestPath.journal_id]", order_by="QuestPath.name")

    _current_quest_paths = sa.orm.relationship(
        "QuestPath",
        primaryjoin="and_(Journal.id==QuestPath.journal_id, "
                    "QuestPath.completed==False)",
        cascade="all, delete-orphan",
        order_by="QuestPath.name"
    )

    @property
    def current_quest_paths(self):
        return self._current_quest_paths

    _notifications = sa.orm.relationship(
        "Entry",
        back_populates="journal",
        order_by="Entry.position",
        collection_class=sa.ext.orderinglist.ordering_list('position'),
        cascade="all, delete-orphan")

    @property
    def notifications(self):
        return Journal.MockNotificationOrderingList(self)

    @notifications.setter
    def notifications(self, value):
        """Assign to self._notifications directly.

        I'm not totally sure this is enough. If you passed in a list of items ...
        it might be best to vet them and make sure that they are actually
        Entry objects.
        """
        self._notifications = value

    # noinspection PyProtectedMember
    class MockNotificationOrderingList:
        def __init__(self, journal):
            self.journal = journal

        def append(self, item):
            self.journal._notifications.append(Entry(item))

        def insert(self, index, entity):
            self.journal._notifications.insert(index, Entry(entity))

        def __iter__(self):
            return self.journal._notifications.__iter__()

        def __repr__(self):
            return self.journal._notifications.__repr__()

        def __getattribute__(self, item):
            # pdb.set_trace()
            if item in ['append', 'insert', 'journal']:
                return object.__getattribute__(self, item)
            else:
                return self.journal._notifications.__getattribute__(item)

    # Journal to Achievements is One to One.
    achievements = sa.orm.relationship("Achievements", back_populates="journal", uselist=False, cascade="all, delete-orphan")

    # @property
    # def quest_notification(self):
    #     return self.notification.get_description()

    # noinspection PyUnusedLocal
    @sa.orm.validates('quest_paths')
    def validate_quest_path(self, key, quest_path):
        """Overload quest_path assignment.

        Build a new path if current one is a template.
        Activate the current_quest as well.
        """
        if quest_path.template:
            quest_path = quest_path.clone()
        self.notifications.append(quest_path)
        # self.notifications.append(Entry(quest_path))
        return quest_path

    # I need to work out the cascade -> should be some kind of SET NULL.
    known_locations = sa.orm.relationship("Location", secondary="journal_to_location", back_populates='journals')

    def __init__(self):
        self.achievements = models.achievements.Achievements()

        # This will let you create an entry object using an instantiated journal
        # hero.journal.notifications.append(hero.journal.Entry(some_object))

    # Each journal can have many entries
    # entries = relationship("Entry", back_populates='journal')

    # def add_entry(self, obj):
    #     entry = Entry(obj, datetime.now(), obj.description)
    #     self.entries.append(entry)


# noinspection PyPropertyAccess
class Entry(models.Base):
    """Various entries into the Journal class.

    For the Notifications:
        each object should have a get_description method.
    So you can do:
    for obj in journal.notifications:
        obj.get_description()
    """
    timestamp = sa.Column(sa.DateTime)
    position = sa.Column(sa.Integer)
    info = sa.Column(sa.String(50))
    name = sa.Column(sa.String(50))
    description = sa.Column(sa.String(200))
    type = sa.Column(sa.String(50))

    # relationships
    journal_id = sa.Column(sa.Integer, sa.ForeignKey('journal.id', ondelete="CASCADE"))
    journal = sa.orm.relationship("Journal", back_populates='_notifications')

    # Each entry can have object (beast, person or place)
    # I may need to build the inverse of the relationship ... not positive
    # though.
    # _beast = relationship()
    # _person = relationship()
    # _place = relationship("Location")
    _beast = sa.Column(sa.String(50))
    _person = sa.Column(sa.String(50))
    _place = sa.Column(sa.String(50))
    _quest_path = sa.orm.relationship("QuestPath")
    _quest_path_id = sa.Column(sa.Integer, sa.ForeignKey('quest_path.id', ondelete="CASCADE"))

    @sa.ext.hybrid.hybrid_property
    def obj(self):
        """Return whichever object has a connection with this one."""
        # pdb.set_trace()
        return self._beast or self._person or self._place or self._quest_path

    @obj.setter
    def obj(self, value):
        """Assign object to appropriate column.

        From @elthran - not implemented
        That’s simple. I’m going to do about 4 types:
        - quest
        - achievement
        - friend message
        - generic notice (like level up)
        """
        # dir(value)
        # pdb.set_trace()
        if value.__tablename__ == "beast":
            self._beast = value
            self.type = "beast"
        elif value.__tablename__ == "person":
            self._person = value
            self.type = "person"
        elif value.__tablename__ == "quest_path":
            self._quest_path = value
            self.type = "quest_path"
        else:
            raise "TypeError: 'obj' does not accept " \
                  "__tablename__ '{}':".format(value.type)

    def __init__(self, obj):
        # pdb.set_trace()
        self.obj = obj
        self.name = obj.name
        self.description = obj.description

    # all of these can be way more generic and get there data from files.
    # Could even add this code in the the into the 'obj.setter' code.
    @property
    def header(self):
        header_template = None
        if self.type == "quest_path":
            header_template = """
                {% if quest_notification.total_reward %}
                    {{ quest_notification.name }}
                {% else %}
                    {{ quest_notification.name }} ({{ quest_notification.stage }} / {{ quest_notification.stages }})
                {% endif %}
            """
        return flask.render_template_string(header_template, quest_notification=self.obj.get_description())

    @property
    def body(self):
        body_template = None
        if self.type == "quest_path":
            body_template = """
                {% if quest_notification.total_reward %}
                    Completed!
                {% else %}
                    Required: {{ quest_notification.current_quest.name }}
                {% endif %}
            """

        return flask.render_template_string(body_template, quest_notification=self.obj.get_description())

    @property
    def footer(self):
        footer_template = None
        if self.type == "quest_path":
            footer_template = """
                {% if quest_notification.total_reward %}
                    Total reward: {{ quest_notification.total_reward }}xp
                {% else %}
                    Reward: {{ quest_notification.current_quest.reward }}xp
                {% endif %}
            """
        return flask.render_template_string(footer_template, quest_notification=self.obj.get_description())

    @property
    def url(self):
        url_template = "/quest_log"
        return flask.render_template_string(url_template)

    @property
    def redirect_message(self):
        url_template = "Click anywhere in this box to visit your journal."
        return flask.render_template_string(url_template)
