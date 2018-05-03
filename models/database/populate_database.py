import datetime

import services
import models
import prebuilt_objects


def create_all():
    models.Base.metadata.create_all(checkfirst=True)


def add_prebuilt_objects():
    for obj_list in [
            prebuilt_objects.users,
            prebuilt_objects.game_worlds,
            # prebuilt_objects.all_abilities,
            prebuilt_objects.all_store_items,
            prebuilt_objects.all_marketplace_items,
            prebuilt_objects.all_quests,
            prebuilt_objects.all_specializations,
            prebuilt_objects.all_forums,
            prebuilt_objects.all_monsters]:
        for obj in obj_list:
            models.Base.session.add(obj)
            if isinstance(obj, models.Account):
                obj.password = services.secrets.encrypt(obj.password)
                obj.timestamp = datetime.datetime.utcnow()
        models.Base.save()

    # Bug exists in which the session expires too quickly.
    # Each query seems to create it's own session?
    # import pdb;pdb.set_trace()
    default_quest_paths = models.QuestPath.filter_by(is_default=True, template=True).all()
    for hero in models.Hero.all():
        hero.journal.quest_paths = default_quest_paths
        # hero.journal.quest_paths = models.QuestPath.filter_by(is_default=True, template=True).all()
    # import pdb; pdb.set_trace()
    models.Hero.save()
