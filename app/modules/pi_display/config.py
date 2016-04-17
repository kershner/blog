from sqlalchemy import desc
from app import app, models, db


def get_prev_gifs(offset):
    previous_gifs = models.Gif.query.order_by(desc(models.Gif.last_played)).limit(10).offset(offset).all()
    result = []
    for gif in previous_gifs:
        data = {
            'id': gif.id,
            'url': gif.url,
            'desc': gif.description,
            'created': str(gif.created_at),
            'last_played': str(gif.last_played),
            'tags': [str(tag.name) for tag in gif.tags]
        }
        result.append(data)
    return result


def get_gif_info(gif_id):
    gif = models.Gif.query.get(gif_id)
    data = {
        'id': gif.id,
        'url': gif.url,
        'desc': gif.description,
        'created': str(gif.created_at),
        'last_played': str(gif.last_played),
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


# Expects list of tag ids returns list of gif_ids
def get_new_gif_ids_list(tag_ids):
    if len(tag_ids):
        print 'Generating gif_ids by tag names...'
        new_gif_ids_list = get_gif_ids_by_tags([str(name) for name in tag_ids])
        return new_gif_ids_list
    else:
        # All Gifs
        print 'Generating all gif_ids...'
        return [gif.id for gif in models.Gif.query.all()]


# Expects list of tag ids as input, returns list of gif IDs with those tags
def get_gif_ids_by_tags(tag_ids):
    tag_ids = [tag_id for tag_id in tag_ids if str(tag_id)]
    if tag_ids:
        ids_string = '(' + ','.join(map(str, tag_ids)) + ')'
        sql = 'SELECT gif_id FROM gif_tags WHERE tag_id IN %s' % ids_string

        my_db_bind = db.get_engine(app, 'gifs_db')
        rows = db.session.execute(sql, bind=my_db_bind)
        result = [entry[0] for entry in rows]
    else:
        result = [gif.id for gif in models.Gif.query.all()]

    return result


# Takes in two lists, removes elements from all list that are present in inactive list
def filter_inactive_tags(all_gif_ids, inactive_tag_gif_ids):
    return [gif_id for gif_id in all_gif_ids if gif_id not in inactive_tag_gif_ids]

