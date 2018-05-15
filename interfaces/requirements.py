# import sqlalchemy as sa
#
# import events
# import base_classes
import services.finder
import build_code


class Requirement:
    # description = sa.Column(sa.String(100))

    def __init__(self, description):
        self.description = description
        self.code = Requirement.parse_requirements(description)

    @staticmethod
    def parse_requirements(requirements):
        """Convert a human readable list of requirements to a code object.

        1. Brawn Attribute Level 3
        2. Dagger Talent of 6, Virtue of -100
        3. 10 Errands Complete, Virtue of 100, Willpower of 4
        4. 5 Locations Discovered, 10 Animals in Bestiary
        5. Alchemy Ability Level 3
        6. Charisma of 7, Fame of 200
        """
        code = []
        type_ = 0
        var = None
        for requirement in requirements.split(','):
            requirement = requirement.split()
            if 'Attribute' in requirement:  # Type 1
                type_ = 1
                var = 'attributes'
            elif "Talent" in requirement:  # Type 2
                type_ = 2
                var = 'proficiencies'
            elif services.finder.is_word(requirement[0]) and 'of' == requirement[1] and services.finder.is_integer(requirement[2]):
                type_ = 3
            elif "Discovered" in requirement:
                type_ = 4
                level = requirement[0]
                code.append("len(hero.journal.known_locations) >= {}".format(level))
            elif "Bestiary" in requirement:
                type_ = 5
            elif "Ability" in requirement:
                type_ = 6
                var = 'abilities'
            else:
                type_ = 7

            if type_ in (1, 2, 6):
                attrib = build_code.normalize_attrib_name(requirement[0])
                level = requirement[-1]
                code.append("hero.{}.{}.level >= {}".format(var, attrib, level))
            elif type_ in (3, 5, 7):
                print("This requirement '{}' (type {}) isn't specific enough!".format(' '.join(requirement), type_))
        code = " and ".join(code)
        return code

    @staticmethod
    def met(obj, hero):
        code = Requirement.parse_requirements(obj.requirements)
        try:
            return eval(code, {'hero': hero})
        except SyntaxError:
            return True  # If code is broken return True :P
        except KeyError:
            return True  # If broken return True
