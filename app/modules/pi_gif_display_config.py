from sqlalchemy import desc
from app import models, db


def get_prev_gifs(offset):
    previous_gifs = models.Gif.query.order_by(desc(models.Gif.last_played)).limit(10).offset(offset).all()
    result = []
    for gif in previous_gifs:
        data = {
            'id': gif.id,
            'url': gif.url,
            'created': gif.created_at,
            'last_played': gif.last_played,
            'tags': [str(tag.name) for tag in gif.tags]
        }
        result.append(data)
    return result


def get_gif_info(gif_id):
    gif = models.Gif.query.get(gif_id)
    data = {
        'id': gif.id,
        'url': gif.url,
        'created': gif.created_at,
        'last_played': gif.last_played,
        'tags': [str(tag.name) for tag in gif.tags]
    }
    return data


def add_tags_to_gif(tags, gif):
    for tag in tags:
        if tag_exists(tag):
            tag = models.Tag.query.filter_by(name=tag).first()
            gif.tags.append(tag)
        else:
            print 'Creating new tag'
            new_tag = models.Tag()
            new_tag.name = tag
            gif.tags.append(new_tag)
            db.session.add(new_tag)
    return gif


def tag_exists(tag_name):
    return models.Tag.query.filter_by(name=str(tag_name)).scalar() is not None
