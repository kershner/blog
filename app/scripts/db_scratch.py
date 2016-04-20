import requests
import praw
import cPickle
import json
import random
from flask import jsonify
from sqlalchemy import text
import timeit
from app import app, db, models


def request_url(url):
    try:
        r = requests.get(url, stream=True, timeout=1, allow_redirects=True)
        size_in_bytes = int(r.headers['content-length'])
        float_size = float(size_in_bytes) / 1051038
        code = r.status_code
        data = {
            'size': size_in_bytes,
            'float_size': size_in_bytes,
            'code': code
        }
        return data
    except Exception as e:
        # print e
        return None


# Expects list of tag strings as input
def get_gif_ids_by_tags(tags):
    tag_ids = []
    for tag in tags:
        tag_ids.append(models.Tag.query.filter_by(name=tag).first().id)

    ids_string = '(' + ','.join(map(str, tag_ids)) + ')'
    sql = 'SELECT gif_id FROM gif_tags WHERE tag_id IN %s' % ids_string

    my_db_bind = db.get_engine(app, 'gifs_db')
    rows = db.session.execute(sql, bind=my_db_bind)

    gifs_ids = [entry[0] for entry in rows]
    return gifs_ids


# gif_ids_to_play = ','.join([str(gif.id) for gif in models.Gif.query.all()])
# print len(gif_ids_to_play.split(','))
# random_gif = models.Gif.query.get(random.choice(gif_ids_to_play))
#
# config = models.Config.query.first()
# print config.gif_ids_to_play
# config.gif_ids_to_play = gif_ids_to_play
# db.session.add(config)
# db.session.commit()
#
# print 'Eat shit fuqqboi#$@#$@#$@##@'
#
# print len(models.Config.query.first().gif_ids_to_play.split(','))


# input_tags = ['animals']
# gifs = get_gifs_ids_by_tags(input_tags)
# r = praw.Reddit(user_agent='Raspberry Pi Project by billcrystals')

# for gif in gifs:
#     print gif

config = models.Config.query.first()
# config.gif_ids_to_play = ','.join(['1', '240', '420'])
# db.session.add(config)
# db.session.commit()
#
# print 'Session Commitedd Fuqqboi'
#
# print config.active_tags

bad_gifs = []
gifs = models.Gif.query.all()
for gif in gifs:
    if 'gifeye' in gif.url:
        bad_gifs.append(gif.url)
print bad_gifs


# Subreddit stuff for later ########################################################################################################################################
# def get_gif_count(subreddit):
#     count = 0
#     # submissions = r.get_subreddit(subreddit).get_hot(limit=100)
#     submissions = r.get_subreddit(subreddit).get_top_from_all(limit=100)
#     for submission in submissions:
#         if submission.url.endswith('.gif'):
#             count += 1
#     return count
#
# subs_to_try = ['WeatherGifs', 'SuperAthleteGifs', 'RealLifeDoodles', 'GifRecipes', 'gtagifs', 'ANormalDayInRussia', 'HighlightGIFS', 'trippy', 'Panda_Gifs',
#                'StartledCats', 'reversegif', 'funny_gifs', 'Unexpected', 'dashcamgifs', 'sc2gifs', 'gifsthatkeepongiving', 'traingifs', 'howitsmade_gifs',
#                'gaminggifs', 'Rave_Gifs', 'babybeastgifs', 'AnimalTextGifs', 'pre_celebration_gifs', 'fractalius_gifs', 'thisismylifenow', 'AnimalsBeingDerps',
#                'SlyGifs', 'EditingAndLayout', 'rickandmortyGIFs', 'tarantinogifs', 'babyrhinogifs', 'DubbedGIFS',
#                'FullMovieGifs']
#
# # Only get results from top_from_all
# not_good_subs = ['DubbedGIFS', 'FullMovieGifs']
#
# total_gifs = 0
# for sub in subs_to_try:
#     gif_number = get_gif_count(sub)
#     print '%d gifs from %s' % (gif_number, sub)
#     total_gifs += gif_number
#
# print '\n%d total Subs' % len(subs_to_try)
# print '%d potential GIFs' % total_gifs
####################################################################################################################################################################
