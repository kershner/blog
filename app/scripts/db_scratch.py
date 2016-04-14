from app import db, models


gifs = models.Gif.query.all()

bad_url_strings = ['gifsec', 'redditmetrics']

for gif in gifs:
    for string in bad_url_strings:
        if string in gif.url:
            print string