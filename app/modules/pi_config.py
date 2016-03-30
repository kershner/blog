from sqlalchemy import text
from flask import request, json, session
from urllib2 import quote
from app import app, db, models

# Local path
path = 'c:/programming/projects/blog/app/templates/pi_display/logs'

# Server path
# path = '/home/tylerkershner/app/templates/pi_display/logs/'

tags = {
    'animals': models.Tag.query.filter_by(name='animals').first().id,
    'gaming': models.Tag.query.filter_by(name='gaming').first().id,
    'strange': models.Tag.query.filter_by(name='strange').first().id,
    'educational': models.Tag.query.filter_by(name='educational').first().id
}


# Initalizes session variables, returns variables for display in template
def pi_config_main():
    session['prev'] = -1
    session['prev_stop'] = -2
    session['prev_start'] = 3

    main_urls_list = [gif.url for gif in models.Gif.query.all()]
    animals_urls_list = get_gifs_by_tag(tags['animals'])
    gaming_urls_list = get_gifs_by_tag(tags['gaming'])
    strange_urls_list = get_gifs_by_tag(tags['strange'])
    educational_urls_list = get_gifs_by_tag(tags['educational'])

    with open('%s/pi_display_config.txt' % local_path, 'r') as config_file:
        config = list(config_file)

    data = {
        'main_urls_count': len(main_urls_list),
        'animals_urls_count': len(animals_urls_list),
        'gaming_urls_count': len(gaming_urls_list),
        'strange_urls_count': len(strange_urls_list),
        'educational_urls_count': len(educational_urls_list),
        'category': config[0][:config[0].find('\n')],
        'current_gif': config[1][:config[1].find('\n')],
        'delay': config[2][:config[2].find('\n')]
    }

    return data


# AJAX call to update config site to currently playing GIF
def pi_config_update():
    session['prev'] = -1

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config = list(config_file)
        current_gif = config[1][:config[1].find('\n')]
        message = 'Currently Playing GIF'
        data = {
            'current_gif': current_gif,
            'message': message
        }

        return data


# AJAX call when 'previous GIF' is clicked
def get_prev():
    session['prev'] -= 1

    with open('%s/last_played.txt' % path, 'a+') as f:
        last_played_list = list(f)
        gifs = last_played_list[int('%d' % session['prev'])][:last_played_list[int('%d' % session['prev'])].find('\n')]
        message = 'Previous GIF'
        data = {
            'last_played': gifs,
            'message': message
        }

        return data


# Set category
def set_category():
    category = request.args.get('category', 0, type=str)

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config = list(config_file)
        delay = config[2][:config[2].find('\n')]

    with open('%s/pi_display_config.txt' % path, 'w+') as config_file:
        config_file.write('%s' % category + '\n')
        config_file.write(config[1])
        config_file.write(config[2])
        message = 'Category changed to %s' % category.title()
        data = {
            'message': message,
            'category': category.title(),
            'delay': delay
        }

        return data


# Set refresh delay
def set_delay():
    delay = request.args.get('delay', 0, type=str)

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config = list(config_file)
        category = config[0][:config[0].find('\n')]

    with open('%s/pi_display_config.txt' % path, 'w+') as config_file:
        config_file.write(config[0])
        config_file.write(config[1])
        config_file.write('%s' % delay + '\n')
        message = 'Delay changed to %s seconds' % delay
        data = {
            'message': message,
            'category': category.title(),
            'delay': delay
        }

        return data


# Clear session (mostly for removing auto-update)
def clear():
    session['prev_stop'] = -2
    session['prev_start'] = 3
    message = 'Session cleared'
    data = {
        'message': message
    }

    return data


def get_gifs_by_tag(tag_ids):
    ids_string = str(tag_ids)
    if type(tag_ids) is list:
        ids_string = ','.join(str(i) for i in tag_ids)

    tag_ids = '(%s)' % ids_string
    gif_db_bind = db.get_engine(app, 'gifs_db')
    sql = text('SELECT gif_id FROM gif_tags WHERE tag_id in ' + tag_ids + ';')
    rows = db.session.execute(sql, bind=gif_db_bind)
    urls = []

    for row in rows:
        url = models.Gif.query.get(row[0]).url
        urls.append(url)

    return urls