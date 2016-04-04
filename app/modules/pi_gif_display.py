import random
from datetime import datetime
from app import models, db


def get_data():
    config = models.Config.query.get(1)
    delay = str(config.delay) + '000'
    gif = random.choice(models.Gif.query.all())

    gif.last_played = datetime.now()
    config.current_gif = gif.url

    db.session.add(gif)
    db.session.add(config)
    db.session.commit()

    data = {
        'gif': gif.url,
        'delay': delay
    }

    return data
