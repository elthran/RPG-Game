import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.ext.hybrid

import models


class Display(models.Base):
    """Stores data for Location objects that is displayed in the game
    using html.
    """
    name = sa.Column(sa.String(50))
    page_title = sa.orm.synonym('name')
    page_heading = sa.Column(sa.String(200))
    page_image = sa.Column(sa.String(50))
    paragraph = sa.Column(sa.String(200))

    """
    External relationships:
    
    This is set up so that each external relationship is one to one and can be
    accessed through the generic 'self.obj' attribute using
    a list of or statements ... only one should be set at a time.
    """
    # One location -> one display (bidirectional)
    location_id = sa.Column(sa.Integer, sa.ForeignKey('location.id',
                                             ondelete="CASCADE"))
    _location = sa.orm.relationship('Location', uselist=False,
                             back_populates='display')

    @sa.ext.hybrid.hybrid_property
    def obj(self):
        """Returns the object that this is connected to.

        Only one type of object may be connected at a time.
        This is not enforced and should be.
        """
        return self._location or None

    def __init__(self, obj, page_heading=None, paragraph=None):
        """Build display object based on objects attributes.

        I think that I should add in a link to the correct HTML template
        as well? Based on object type?

        Consider making all of these attributes property methods instead
        so that I don't have to run an update function.

        NOTE: update method overrides all attributes!
        """

        self.name = obj.name
        self.page_heading = page_heading or self.default_heading()

        # eg. page_image = town if Town object is passed or cave if Cave
        # object is passed.
        self.page_image = obj.type.lower() + '.jpg'
        self.paragraph = paragraph or self.default_paragraph()

    def default_heading(self):
        return "You are in {}".format(self.name)

    def default_paragraph(self):
        return "There are many places to visit within" \
               " the {}. Have a look!".format(self.page_image)

    def update(self):
        """Update self to reflect changes in obj properties.

        This is not automatic ... though maybe it should be.
        Currently you need to define a validator on each object
        that calls this function.

        !IMPORTANT! this could overwrite custom attributes incorrectly.

        ONLY RUN THIS if you change the object's:
            name or
            type
        after creation.
        e.g.
            USE update()
        cave = node_grid[2]
        cave.name = "Outside Creepy cave"
        cave.type = 'cave'
        cave.update()
        cave.display.page_heading = "You are outside a cave called {}".format(cave.name)
        cave.display.page_image = "generic_cave_entrance.jpg"
        cave.display.paragraph = "There are many scary places to die within the cave. Have a look!"
            DON'T USE update()
        old_mans_hut = Location("Old Man's Hut", 'house')
        old_mans_hut.display.page_heading = "Old Man's Hut"
        old_mans_hut.display.page_image = 'hut.jpg'
        old_mans_hut.display.paragraph = "Nice to see you again kid. What do you need?"
        """

        if self.page_heading == self.default_heading():
            self.page_heading = "You are in {}".format(self.obj.name)
        if self.paragraph == self.default_paragraph():
            self.paragraph = "There are many places to visit within " \
                             "the {}. Have a look!".format(self.obj.type)

        self.name = self.obj.name
        self.page_image = self.obj.type.lower() + '.jpg'
