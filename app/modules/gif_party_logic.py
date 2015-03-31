from flask import request, session
import random


# Grabs image for welcome page
def get_image():
    path = '/home/tylerkershner/app/templates/gif_party'
    filename = 'welcome_urls.txt'

    with open('%s/%s' % (path, filename), 'r') as urls_file:
        urls_list = list(urls_file)

    image_url = random.choice(urls_list)
    image_url = image_url[:image_url.find('\n')]

    return image_url


# Return number of images in each file
def get_image_counts():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    session['played'] = []

    with open('%s/all_urls.txt' % path, 'r') as last_played_file:
        all_urls_list = list(last_played_file)

    with open('%s/animals_urls.txt' % path, 'r') as urls_file:
        animals_urls_list = list(urls_file)

    with open('%s/gaming_urls.txt' % path, 'r') as urls_file:
        gaming_urls_list = list(urls_file)

    with open('%s/strange_urls.txt' % path, 'r') as urls_file:
        strange_urls_list = list(urls_file)

    with open('%s/educational_urls.txt' % path, 'r') as urls_file:
        educational_urls_list = list(urls_file)

    data = {
        'main_urls_count': len(all_urls_list),
        'animals_urls_count': len(animals_urls_list),
        'gaming_urls_count': len(gaming_urls_list),
        'strange_urls_count': len(strange_urls_list),
        'educational_urls_count': len(educational_urls_list)
    }

    return data


# Main AJAX call - returns list of URLs to display based on user settings
def gif_party_main():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    if 'category' in session:
        category = session['category']
    else:
        category = 'all'
    if 'number' in session:
        number = session['number']
    else:
        number = 10
    if 'delay' in session:
        delay = session['delay']
    else:
        delay = 60000

    if category == 'all':
        filename = 'all_urls.txt'
    elif category == 'animals':
        filename = 'animals_urls.txt'
    elif category == 'gaming':
        filename = 'gaming_urls.txt'
    elif category == 'strange':
        filename = 'strange_urls.txt'
    elif category == 'educational':
        filename = 'educational_urls.txt'
    else:
        filename = 'all_urls.txt'

    with open('%s/%s' % (path, filename), 'r') as urls_file:
        urls_list = list(urls_file)

    urls = []

    def check_if_played(url):
        if url + '\n' in session['played']:
            print 'Already played this URL'
            return False
        else:
            return True

    for i in range(number):
        choice = random.choice(urls_list)

        checking = False
        while not checking:
            if check_if_played(choice):
                checking = True
            else:
                print 'Choosing different GIF'
                choice = random.choice(urls_list)

        session['played'].append(choice)
        choice = choice[:choice.find('\n')]
        urls.append(choice)

    data = {
        'URLs': urls,
        'number': number,
        'delay': delay,
        'category': category
    }

    return data


# Sets session variable for category
def select_category(category):
    session['category'] = category

    data = {
        'category': session['category']
    }

    return data


# Sets session variable for number of GIFs
def select_number(number):
    session['number'] = int(number)

    data = {
        'number': session['number']
    }

    return data


# Sets session variable for refresh delay
def gif_party_delay():
    delay = request.json
    delay = str(delay) + '000'
    session['delay'] = delay

    data = {
        'delay': session['delay']
    }

    return data