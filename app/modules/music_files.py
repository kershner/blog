import os
from mutagen.mp3 import MP3


# Sorts through directory containing MP3s, returns organized lists
def get_songs():
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.dirname(path) + '/static/music/'
    files = sorted(os.listdir(path), reverse=True)
    known_songs = ['23', '25', '27', '28', '29', '30']
    songs = []
    loops = []
    song_count = 1
    loop_count = 1
    for item in files:
        css_class = ''
        name = item[:item.find('.')]
        length = MP3(path + name + '.mp3').info.length
        m, s = divmod(length, 60.0)
        length = '%d:%d' % (int(m), int(s))
        if name in known_songs:
            if song_count % 2 == 0:
                css_class = 'highlight'
            if name == '29':
                length = '4:05'
            songs.append([name, length, css_class])
            song_count += 1
        else:
            if loop_count % 2 == 0:
                css_class = 'highlight'
            if name == '18':
                length = '1:05'
            if name == '33':
                length = '1:09'
            loops.append([name, length, css_class])
            loop_count += 1

    data = {
        'songs': songs,
        'loops': loops
    }

    return data