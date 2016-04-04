from sqlalchemy import desc
from app import app, db, models

tags = {
    'animals': models.Tag.query.filter_by(name='animals').first().id,
    'gaming': models.Tag.query.filter_by(name='gaming').first().id,
    'strange': models.Tag.query.filter_by(name='strange').first().id,
    'educational': models.Tag.query.filter_by(name='educational').first().id
}


def pi_config_main():
    data = {

    }

    return data


def get_prev_gifs(offset):
    previous_gifs = models.Gif.query.order_by(desc(models.Gif.last_played)).limit(10).offset(offset).all()
    result = [str(gif.url) for gif in previous_gifs]
    return result
