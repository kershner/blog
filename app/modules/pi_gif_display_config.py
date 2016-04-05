from sqlalchemy import desc
from app import models


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
        'url': gif.url,
        'created': gif.created_at,
        'last_played': gif.last_played,
        'tags': [str(tag.name) for tag in gif.tags]
    }
    return data
