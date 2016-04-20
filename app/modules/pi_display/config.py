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


# Expects list of tag ids, returns list of gif IDs with those tags
def get_gif_ids_by_tags(tag_ids, inactive_tags=None):
    my_db_bind = db.get_engine(app, 'gifs_db')
    tag_ids = [tag_id for tag_id in tag_ids if str(tag_id)]
    result = [gif.id for gif in models.Gif.query.all()]
    if tag_ids:
        print 'Active tags passed!'
        ids_string = '(' + ','.join(map(str, tag_ids)) + ')'
        sql = 'SELECT gif_id FROM gif_tags WHERE tag_id IN %s' % ids_string
        if inactive_tags is not None:
            print 'Also passing inactive tags!'
            inactive_ids_string = '(' + ','.join(map(str, inactive_tags)) + ')'
            sql += ' AND tag_id NOT IN %s' % inactive_ids_string

        rows = db.session.execute(sql, bind=my_db_bind)
        result = [entry[0] for entry in rows]
    else:
        print 'No active tags passed...'
        if inactive_tags is not None:
            print 'But passing inactive tags!'
            all_gif_ids = [gif.id for gif in models.Gif.query.all()]
            inactive_ids_string = '(' + ','.join(map(str, inactive_tags)) + ')'
            sql = 'SELECT gif_id FROM gif_tags WHERE tag_id IN %s' % inactive_ids_string

            rows = db.session.execute(sql, bind=my_db_bind)
            inactive_gif_ids = [entry[0] for entry in rows]
            result = filter_inactive_tags(all_gif_ids, inactive_gif_ids)

    return result


def get_tag_gif_counts():
    my_db_bind = db.get_engine(app, 'gifs_db')
    all_tags = models.Tag.query.all()
    for tag in all_tags:
        sql = 'SELECT count(gif_id) FROM gif_tags WHERE tag_id = %s' % str(tag.id)
        rows = db.session.execute(sql, bind=my_db_bind)
        result = [entry[0] for entry in rows]
        tag.gif_count = int(result[0])

    return all_tags


def get_total_gifs_in_rotation():
    gif_config = models.Config.query.first()

    active_tag_ids = [int(tag_id) for tag_id in gif_config.active_tags.split(',') if tag_id]
    inactive_tag_ids = [int(tag_id) for tag_id in gif_config.inactive_tags.split(',') if tag_id]

    total_gif_ids_in_rotation = get_gif_ids_by_tags(active_tag_ids, inactive_tag_ids)
    return len(total_gif_ids_in_rotation)


# Takes in two lists, removes elements from all list that are present in inactive list
def filter_inactive_tags(gif_ids, inactive_tag_gif_ids):
    return [gif_id for gif_id in gif_ids if gif_id not in inactive_tag_gif_ids]