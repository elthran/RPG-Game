# import sqlalchemy as sa
#
# import events
# import base_classes


class Requirement:
    # description = sa.Column(sa.String(100))

    def __init__(self, description):
        self.description = description
        self.code = Requirement.parse_requirements(description)

    @staticmethod
    def parse_requirements(reqs):
        reqs = reqs.split(',')
        req = reqs[0]  # ignore other requirements for now.
        req = req.split()
        attrib = req[0].lower()
        level = req[-1]
        return "hero.attributes.{}.level >= {}".format(attrib, level)

    @staticmethod
    def met(obj, hero):
        code = Requirement.parse_requirements(obj.requirements)
        try:
            return eval(code, {'hero': hero})
        except SyntaxError:
            return True  # If code is broken return True :P
        except KeyError:
            return True  # If broken return True
