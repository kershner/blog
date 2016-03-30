import random
from app import models

# Local path
path = 'c:/programming/projects/blog/app/templates/pi_display/logs'

# Server path
# path = '/home/tylerkershner/app/templates/pi_display/logs/'


def pi_display_main():
    # Open config file, grab variables from it
    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config = list(config_file)

    delay = config[2][:config[2].find('\n')]
    gif_urls = random.sample([gif.url for gif in models.Gif.query.all()], 1000)

    delay = str(delay) + '000'

    data = {
        'urls': gif_urls,
        'delay': delay
    }

    return data
