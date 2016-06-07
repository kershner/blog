import random
from datetime import datetime
from . import config as pi_config
from app import models, db


def grab_gif_data():
    config = models.Config.query.first()
    delay = str(config.delay) + '000'

    gif_ids_to_play = [gif_id for gif_id in config.gif_ids_to_play.split(',') if str(gif_id)]
    print '%d URLs remaining...' % len(gif_ids_to_play)

    if not config.gif_ids_to_play:
        gif_ids_to_play = get_new_gif_list()

    gif = None
    while gif is None:
        if not config.gif_ids_to_play:
            gif_ids_to_play = get_new_gif_list()
        choice = random.choice(gif_ids_to_play)
        gif_ids_to_play.remove(choice)
        gif = models.Gif.query.filter_by(id=choice).first()

    config.gif_ids_to_play = ','.join([str(gif_id) for gif_id in gif_ids_to_play])
    config.current_gif = gif.url

    gif.last_played = datetime.now()

    db.session.add(gif)
    db.session.add(config)
    db.session.commit()

    data = {
        'gif': gif.url,
        'delay': delay
    }

    return data


def get_new_gif_list():
    config = models.Config.query.first()
    print 'Generating new list of gif IDs...'
    if config.active_tags:
        new_gif_ids_list = pi_config.get_new_gif_ids_list(config.active_tags.split(','))
        config.gif_ids_to_play = new_gif_ids_list
    else:
        new_gif_ids_list = [str(gif.id) for gif in models.Gif.query.all()]
        config.gif_ids_to_play = ','.join(new_gif_ids_list)

    return new_gif_ids_list
