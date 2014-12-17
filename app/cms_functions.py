from markdown import markdown
import bleach
from datetime import datetime, timedelta
import collections
import os


# Return filenames from a high-level directory
def dog_icons():
    base_url = '/static/images/dogsicons/dogsicon'
    icons = []
    counter = 1
    for x in range(0, 7):
        icons.append(base_url + str(counter) + '.png')
        counter += 1

    return icons


# Strip out HTML tags, create markdown
def generate_markdown(text, clean):
    tags = ['pre', 'code', 'iframe']
    attrs = {
        'code': ['data-language', 'class'],
        'iframe': ['class', 'width', 'height', 'src', 'frameborder', 'allowfullscreen']
    }

    if clean:
        clean_text = bleach.clean(text, tags, attrs, strip=True)
        return clean_text
    else:
        clean_text = bleach.clean(text, tags, attrs)
        return markdown(clean_text)


# Return true if a post was created in current month/year
def get_recent_posts(post):
    today = datetime.today()
    last_month = today - timedelta(weeks=4)
    two_months_ago = today - timedelta(weeks=8)
    current_month = today.month
    current_year = today.year

    try:
        if int(post.month) == current_month and int(post.year) == current_year:
            return 'Current Month'
        elif int(post.month) == last_month.month and int(post.year) == last_month.year:
            return 'Last Month'
        elif int(post.month) == two_months_ago.month and int(post.year) == two_months_ago.year:
            return 'Two Months Ago'
    except TypeError:
        return False


# Generate statistics from posts
def stats(posts):
    word_list = []
    total_posts = 0
    for post in posts:
        words_1 = (str(post.title).split())
        words_2 = (str(post.subtitle).split())
        words_3 = (str(post.content).split())
        for word in words_1:
            word_list.append(word)
        for word in words_2:
            word_list.append(word)
        for word in words_3:
            word_list.append(word)
        total_posts += 1
    counter = collections.Counter(word_list)
    most_common, number_occurrences = counter.most_common(1)[0]

    statistics = {
        'posts': total_posts,
        'words': len(word_list),
        'avg_words': (len(word_list) / total_posts),
        'most_common': most_common,
        'number': number_occurrences
    }

    return statistics


# Check inputs against hidden file
def password_validate(username, password):
    path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.abspath(os.path.join(path, os.pardir))
    file_object = filepath + '/cms_settings.txt'

    if not username or not password:
        message = 'All fields are required'
        return [False, message]

    with open(file_object, 'r') as f:
        data = f.read().split()
        if username == data[0]:
            if password == data[1]:
                print 'Access granted!'
                return [True, None]
            else:
                message = 'Invalid password.'
                return [False, message]
        else:
            message = 'Invalid username.'
            return [False, message]


def get_theme(color):
    if color == 'rgb(227, 244, 241)' or color == 'green':
        return 'green'
    elif color == 'rgb(242, 242, 242)' or color == 'grey':
        return 'grey'
    elif color == 'rgb(255, 255, 255)' or color == 'white':
        return 'white2'
    elif color == 'rgb(41, 102, 192)' or color == 'blue':
        return 'blue'
    else:
        return
