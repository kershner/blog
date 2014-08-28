from flask import jsonify, render_template, request, flash, redirect, url_for, session
from forms import DateCheckerForm, BackorderForm, ApplicationForm, DeaForm, NewAccountForm, ShadyForm, DiscrepancyForm,\
    StillNeed, LicenseNeeded, DeaVerify, DeaForms, SlideshowDelay, GifParty, RedditImageScraper
from urllib import quote
import datetime
import random
import re
import praw
import requests
from functools import wraps
from app import app, db, models


##############################################################################
## Blog ######################################################################
@app.route('/')
def home():
    return render_template("/blog/home.html",
                           title="Home")


@app.route('/warning')
def warning():
    return render_template("/blog/warning.html",
                           title="Warning")


@app.route('/archive')
def archive():
    return render_template("/blog/archive.html",
                           title="Blog Archive")


@app.route('/may14')
def may14():
    return render_template("/blog/blog_archive/may14.html",
                           title="May 2014")


@app.route('/jun14')
def jun14():
    return render_template("/blog/blog_archive/jun14.html",
                           title="June 2014")


@app.route('/jul14')
def jul14():
    return render_template("/blog/blog_archive/jul14.html",
                           title="July 2014")


@app.route('/about')
def about():
    return render_template("/blog/about.html",
                           title="About Me")


@app.route('/projects')
def projects():
    return render_template("/blog/projects.html",
                           title="Projects")


@app.route('/pta')
def project1():
    return render_template("/blog/projects/project01.html",
                           title="Python Text Adventure")


@app.route('/cstools-project')
def project2():
    return render_template("/blog/projects/project02.html",
                           title="CSTools")


@app.route('/gif_display')
def gif_display():
    return render_template("/blog/projects/project03.html",
                           title="Raspberry Pi GIF Display")


@app.route('/gif-party')
def gif_party_project():
    return render_template("/blog/projects/project04.html",
                           title="Gif Party!")


@app.route('/reddit-scraper')
def reddit_scraper_project():
    return render_template("/blog/projects/project05.html",
                           title="Reddit Scraper")


@app.route('/cstoolswriteup-part1')
def project2writeup1():
    return render_template("/blog/writeups/project02-part1.html",
                           title="CSTools Writeup")


@app.route('/cstoolswriteup-part2')
def project2writeup2():
    return render_template("/blog/writeups/project02-part2.html",
                           title="CSTools Writeup")


@app.route('/piproject1')
def piproject1():
    return render_template("/blog/writeups/project03-part1.html",
                           title="GIF Picture Frame Writeup Part 1")


@app.route('/piproject2')
def piproject2():
    return render_template("/blog/writeups/project03-part2.html",
                           title="GIF Picture Frame Writeup Part 2")


##############################################################################
# Pi Display
##############################################################################
@app.route('/pi_display')
def pi_display():
    return render_template('/pi_display/pi_display.html')


@app.route('/pi_display_json')
def pi_display_json():
    path = 'E:/programming/projects/blog/app/templates/pi_display/logs'

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    category = config_file_list[1][config_file_list[1].find('=') + 2:config_file_list[1].find('\n')]
    delay = config_file_list[3][config_file_list[3].find('=') + 2:config_file_list[3].find('\n')]

    if category == 'all':
        filename = 'all_urls.txt'
        toplay_filename = 'all_urls_to_play.txt'
    elif category == 'animals':
        filename = 'animals_urls.txt'
        toplay_filename = 'animals_urls_to_play.txt'
    elif category == 'gaming':
        filename = 'gaming_urls.txt'
        toplay_filename = 'gaming_urls_to_play.txt'
    elif category == 'strange':
        filename = 'strange_urls.txt'
        toplay_filename = 'strange_urls_to_play.txt'
    elif category == 'educational':
        filename = 'educational_urls.txt'
        toplay_filename = 'educational_urls_to_play.txt'
    else:
        filename = 'urls.txt'
        toplay_filename = "urls_to_play.txt"

    with open('%s/%s' % (path, filename), 'r') as urls_file:
        urls_list = list(urls_file)

    with open('%s/%s' % (path, toplay_filename), 'r') as urls_toplay_file:
        urls_toplay_list = list(urls_toplay_file)

    # If there are no more URLs in the to_play file, create a new one
    if len(urls_toplay_list) > 1:
        pass
    else:
        urls_toplay_file = open('%s/%s' % (path, toplay_filename), 'a+')
        for entry in urls_list:
            urls_toplay_file.write(entry)
        urls_toplay_file.close()

    with open('%s/%s' % (path, toplay_filename), 'r') as urls_toplay_file:
        urls_toplay_list = list(urls_toplay_file)

    # Choose random URL from to_play list, writing to config file
    gif_url = random.choice(urls_toplay_list)
    with open('%s/pi_display_config.txt' % path, 'w+') as config_file:
        config_file.write(config_file_list[0])
        config_file.write(config_file_list[1])
        config_file.write('CURRENT_GIF = %s' % gif_url)
        config_file.write(config_file_list[3])

    # Opening/closing to_play_urls.txt (taking advantage of side effect to erase contents)
    open('%s/%s' % (path, toplay_filename), 'w').close()

    # Rewrite to_play.txt without current gif URL (won't play twice)
    with open('%s/%s' % (path, toplay_filename), 'a+') as urls_to_play:
        for entry in urls_toplay_list:
            if entry == gif_url:
                pass
            else:
                urls_to_play.write(entry)

    with open('%s/last_played.txt' % path, 'a+') as last_played:
        last_played.write(gif_url)

    delay = str(delay) + '000'

    obj = {
        "URL": gif_url,
        "delay": delay
    }

    return jsonify(obj)


##############################################################################
# Pi Display Config
##############################################################################
@app.route('/pi_display_config', methods=['GET', 'POST'])
def pi_display_config():
    form = SlideshowDelay()

    #path = 'H:/programming/projects/blog/app/templates/pi_display/logs'
    path = 'E:/programming/projects/blog/app/templates/pi_display/logs'

    with open('%s/all_urls.txt' % path, 'r') as urls_file:
        main_urls_list = list(urls_file)

    with open('%s/animals_urls.txt' % path, 'r') as urls_file:
        animals_urls_list = list(urls_file)

    with open('%s/gaming_urls.txt' % path, 'r') as urls_file:
        gaming_urls_list = list(urls_file)

    with open('%s/strange_urls.txt' % path, 'r') as urls_file:
        strange_urls_list = list(urls_file)

    with open('%s/educational_urls.txt' % path, 'r') as urls_file:
        educational_urls_list = list(urls_file)

    with open('%s/pi_display_config.txt' % path, 'r') as urls_file:
        config_file_list = list(urls_file)

    with open('%s/last_played.txt' % path, 'r') as last_played_file:
        last_played_list = list(last_played_file)

    main_urls_count = len(main_urls_list)
    animals_urls_count = len(animals_urls_list)
    gaming_urls_count = len(gaming_urls_list)
    strange_urls_count = len(strange_urls_list)
    educational_urls_count = len(educational_urls_list)
    last_played_1 = last_played_list[-6]
    last_played_2 = last_played_list[-5]
    last_played_3 = last_played_list[-4]
    last_played_4 = last_played_list[-3]
    last_played_5 = last_played_list[-2]

    category = config_file_list[1][config_file_list[1].find('=') + 2:config_file_list[1].find('\n')]
    delay = config_file_list[3][config_file_list[3].find('=') + 2:config_file_list[3].find('\n')]
    current_gif = config_file_list[2][config_file_list[2].find('=') + 2:config_file_list[2].find('\n')]

    if request.method == 'POST':
        if not form.validate():
            flash('Enter a time delay (in seconds)')
            return redirect(url_for('pi_display_config'))

        else:
            delay = str(form.delay.data)

            with open('%s/pi_display_config.txt' % path, 'w+') as config_file:
                config_file.write(config_file_list[0])
                config_file.write(config_file_list[1])
                config_file.write(config_file_list[2])
                config_file.write('DELAY = %s' % delay + '\n')

            return redirect(url_for('pi_display_config'))

    elif request.method == 'GET':
        return render_template("/pi_display/pi_display_config.html",
                               current_gif=current_gif,
                               form=form,
                               main_urls_count=main_urls_count,
                               animals_urls_count=animals_urls_count,
                               gaming_urls_count=gaming_urls_count,
                               strange_urls_count=strange_urls_count,
                               educational_urls_count=educational_urls_count,
                               last_played_1=last_played_1,
                               last_played_2=last_played_2,
                               last_played_3=last_played_3,
                               last_played_4=last_played_4,
                               last_played_5=last_played_5,
                               category=category,
                               delay=delay)


@app.route('/pi_display_config_all')
def pi_display_config_all():
    #path = 'H:/programming/projects/blog/app/templates/pi_display/logs'
    path = 'E:/programming/projects/blog/app/templates/pi_display/logs'

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/pi_display_config.txt' % path, 'w+') as config_file:
        config_file.write(config_file_list[0])
        config_file.write('CATEGORY = all' + '\n')
        config_file.write(config_file_list[2])
        config_file.write(config_file_list[3])

    return redirect(url_for('pi_display_config'))


@app.route('/pi_display_config_animals')
def pi_display_config_animals():
    #path = 'H:/programming/projects/blog/app/templates/pi_display/logs'
    path = 'E:/programming/projects/blog/app/templates/pi_display/logs'

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/pi_display_config.txt' % path, 'w+') as config_file:
        config_file.write(config_file_list[0])
        config_file.write('CATEGORY = animals' + '\n')
        config_file.write(config_file_list[2])
        config_file.write(config_file_list[3])

    return redirect(url_for('pi_display_config'))


@app.route('/pi_display_config_gaming')
def pi_display_config_gaming():
    #path = 'H:/programming/projects/blog/app/templates/pi_display/logs'
    path = 'E:/programming/projects/blog/app/templates/pi_display/logs'

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/pi_display_config.txt' % path, 'w+') as config_file:
        config_file.write(config_file_list[0])
        config_file.write('CATEGORY = gaming' + '\n')
        config_file.write(config_file_list[2])
        config_file.write(config_file_list[3])

    return redirect(url_for('pi_display_config'))


@app.route('/pi_display_config_strange')
def pi_display_config_strange():
    #path = 'H:/programming/projects/blog/app/templates/pi_display/logs'
    path = 'E:/programming/projects/blog/app/templates/pi_display/logs'

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/pi_display_config.txt' % path, 'w+') as config_file:
        config_file.write(config_file_list[0])
        config_file.write('CATEGORY = strange' + '\n')
        config_file.write(config_file_list[2])
        config_file.write(config_file_list[3])

    return redirect(url_for('pi_display_config'))


@app.route('/pi_display_config_educational')
def pi_display_config_educational():
    #path = 'H:/programming/projects/blog/app/templates/pi_display/logs'
    path = 'E:/programming/projects/blog/app/templates/pi_display/logs'

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/pi_display_config.txt' % path, 'w+') as config_file:
        config_file.write(config_file_list[0])
        config_file.write('CATEGORY = educational' + '\n')
        config_file.write(config_file_list[2])
        config_file.write(config_file_list[3])

    return redirect(url_for('pi_display_config'))


@app.route('/previously/1-20')
def previously():
    #path = 'H:/programming/projects/blog/app/templates/pi_display/logs'
    path = 'E:/programming/projects/blog/app/templates/pi_display/logs'

    with open('%s/last_played.txt' % path, 'r') as last_played_file:
        last_played_list = list(last_played_file)

    list_length = len(last_played_list)
    last_ten = ''.join(last_played_list[:-11:-1]).split()
    next_ten = ''.join(last_played_list[-11:-21:-1]).split()

    return render_template('/pi_display/previously.html',
                           list_length=list_length,
                           last_ten=last_ten,
                           next_ten=next_ten,
                           number=20)


@app.route('/previously/21-40')
def previously_2():
    #path = 'H:/programming/projects/blog/app/templates/pi_display/logs'
    path = 'E:/programming/projects/blog/app/templates/pi_display/logs'

    with open('%s/last_played.txt' % path, 'r') as last_played_file:
        last_played_list = list(last_played_file)

    list_length = len(last_played_list)
    last_ten = ''.join(last_played_list[:-11:-1]).split()
    next_ten = ''.join(last_played_list[-11:-21:-1]).split()
    next_ten1 = ''.join(last_played_list[-21:-31:-1]).split()
    next_ten2 = ''.join(last_played_list[-31:-41:-1]).split()

    return render_template('/pi_display/previously.html',
                           list_length=list_length,
                           last_ten=last_ten,
                           next_ten=next_ten,
                           next_ten1=next_ten1,
                           next_ten2=next_ten2,
                           number=40)


@app.route('/previously/41-60')
def previously_3():
    #path = 'H:/programming/projects/blog/app/templates/pi_display/logs'
    path = 'E:/programming/projects/blog/app/templates/pi_display/logs'

    with open('%s/last_played.txt' % path, 'r') as last_played_file:
        last_played_list = list(last_played_file)

    list_length = len(last_played_list)
    last_ten = ''.join(last_played_list[:-11:-1]).split()
    next_ten = ''.join(last_played_list[-11:-21:-1]).split()
    next_ten1 = ''.join(last_played_list[-21:-31:-1]).split()
    next_ten2 = ''.join(last_played_list[-31:-41:-1]).split()
    next_ten3 = ''.join(last_played_list[-41:-51:-1]).split()
    next_ten4 = ''.join(last_played_list[-51:-61:-1]).split()

    return render_template('/pi_display/previously.html',
                           list_length=list_length,
                           last_ten=last_ten,
                           next_ten=next_ten,
                           next_ten1=next_ten1,
                           next_ten2=next_ten2,
                           next_ten3=next_ten3,
                           next_ten4=next_ten4,
                           number=60)


##############################################################################
## Gif Party
##############################################################################
@app.route('/gif_party')
def gif_party_welcome():
    #path = 'H:/programming/projects/blog/app/templates/gif_party'
    path = 'E:/programming/projects/blog/app/templates/gif_party'

    filename = 'welcome_urls.txt'

    with open('%s/%s' % (path, filename), 'r') as urls_file:
        urls_list = list(urls_file)

    image_url = random.choice(urls_list)
    image_url = image_url[:image_url.find('\n')]

    return render_template('/gif_party/welcome.html',
                           image_url=image_url)


@app.route('/gif_party_about')
def gif_party_about():
    #path = 'H:/programming/projects/blog/app/templates/gif_party'
    path = 'E:/programming/projects/blog/app/templates/gif_party'

    filename = 'welcome_urls.txt'

    with open('%s/%s' % (path, filename), 'r') as urls_file:
        urls_list = list(urls_file)

    image_url = random.choice(urls_list)
    image_url = image_url[:image_url.find('\n')]

    return render_template('/gif_party/about.html',
                           image_url=image_url)


@app.route('/gif_party_viewer', methods=['GET', 'POST'])
def gif_party():
    form = GifParty()
    #path = 'H:/programming/projects/blog/app/templates/pi_display/logs'
    path = 'E:/programming/projects/blog/app/templates/pi_display/logs'

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

    main_urls_count = len(all_urls_list)
    animals_urls_count = len(animals_urls_list)
    gaming_urls_count = len(gaming_urls_list)
    strange_urls_count = len(strange_urls_list)
    educational_urls_count = len(educational_urls_list)

    return render_template('/gif_party/gif_party.html',
                           form=form,
                           main_urls_count=main_urls_count,
                           animals_urls_count=animals_urls_count,
                           gaming_urls_count=gaming_urls_count,
                           strange_urls_count=strange_urls_count,
                           educational_urls_count=educational_urls_count)


@app.route('/gif_party_json')
def gif_party_json():
    #path = 'H:/programming/projects/blog/app/templates/pi_display/logs'
    path = 'E:/programming/projects/blog/app/templates/pi_display/logs'

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
        "URLs": urls,
        "number": number,
        "delay": delay,
        "category": category
    }

    return jsonify(data)


@app.route('/gif_party_json_all')
def gif_party_json_all():
    session['category'] = 'all'

    data = {
        'category': session['category']
    }

    return jsonify(data)


@app.route('/gif_party_json_animals')
def gif_party_json_animals():
    session['category'] = 'animals'

    data = {
        'category': session['category']
    }

    return jsonify(data)


@app.route('/gif_party_json_gaming')
def gif_party_json_gaming():
    session['category'] = 'gaming'

    data = {
        'category': session['category']
    }

    return jsonify(data)


@app.route('/gif_party_json_strange')
def gif_party_json_strange():
    session['category'] = 'strange'

    data = {
        'category': session['category']
    }

    return jsonify(data)


@app.route('/gif_party_json_educational')
def gif_party_json_educational():
    session['category'] = 'educational'

    data = {
        'category': session['category']
    }

    return jsonify(data)


@app.route('/gif_party_json_5')
def gif_party_json_5():
    session['number'] = 5

    data = {
        "number": session['number']
    }

    return jsonify(data)


@app.route('/gif_party_json_10')
def gif_party_json_10():
    session['number'] = 10

    data = {
        "number": session['number']
    }

    return jsonify(data)


@app.route('/gif_party_json_20')
def gif_party_json_20():
    session['number'] = 20

    data = {
        "number": session['number']
    }

    return jsonify(data)


@app.route('/gif_party_json_delay', methods=['GET', 'POST'])
def gif_party_json_delay():
    delay = request.json
    delay = str(delay) + '000'
    session['delay'] = delay

    data = {
        "delay": session['delay']
    }

    return jsonify(data)


#######################################################################################
#####  CS Tools Apps ##################################################################
class GetClass(object):
    def __init__(self, count, color):
        self.count = count
        self.color = color

    # Simple logic to determine what color (CSS class) the elements will be
    def get_color(self):
        if self.count == 1:
            self.color = 'purple'
        elif self.count == 2:
            self.color = 'blue'
        elif self.count == 3:
            self.color = 'red'
        elif self.count == 4:
            self.color = 'light-purple'
        elif self.count == 5:
            self.color = 'dark-green'
        elif self.count == 6:
            self.color = 'dark-blue'
        elif self.count == 7:
            self.color = 'dark-red'
        elif self.count == 9:
            self.color = 'orange-entry'
            self.count = 1
        self.count += 1

get_class_li = GetClass(1, 'purple')
get_class_well = GetClass(1, 'blue')


@app.route('/cstools')
def cstools():
    return render_template("/cstools/index.html",
                           title="Home")


@app.route('/cstools/datechecker', methods=['GET', 'POST'])
def datechecker():
    form = DateCheckerForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template("/cstools/datechecker.html",
                                   title="222 Form Date Checker",
                                   form=form)
        else:
            try:
                form_date = form.form_date.data
                date_object = datetime.datetime.date(datetime.datetime.strptime(form_date, '%m/%d/%y'))
                form_expiry_date = date_object + datetime.timedelta(days=60)
                form_expiry_date_nice = "%s %s" % (str(form_expiry_date.strftime("%B")), str(form_expiry_date.day))
                days_expired = datetime.date.today() - form_expiry_date
                if form_expiry_date > datetime.date.today():
                    message = "The form is valid until %s,  %s days from now." % \
                              (form_expiry_date_nice, str(abs(days_expired.days)))
                else:
                    message = "The form expired on %s, %s days ago." % \
                              (str(form_expiry_date_nice), str(days_expired.days))

                return render_template("/cstools/datechecker.html",
                                       title="222 Form Date Checker",
                                       form=form,
                                       message=message)
            except ValueError:
                message = "Enter the form's issue date in the format MM/DD/YY."
                return render_template("/cstools/datechecker.html",
                                       title="222 Form Date Checker",
                                       form=form,
                                       message=message)
    elif request.method == 'GET':
        return render_template("/cstools/datechecker.html",
                               title="222 Form Date Checker",
                               form=form)


@app.route('/cstools/backorder', methods=['GET', 'POST'])
def backorder():
    form = BackorderForm()
    get_class_well.get_color()
    color = get_class_well.color

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/cstools/backorder.html",
                                   title="Backorder Template",
                                   form=form,
                                   color=color)
        else:
            email = form.email.data
            subject = "Cayman Chemical Backorder Notification %s" % form.po.data
            body = "Hello %s,\n\nUnfortunately we need to inform you that one "\
                   "of your items is currently not available.  Item # %s is " \
                   "in production with an approximate lead time of %s." % \
                   (form.name.data, form.item_number.data, form.lead_time.data)
            partial = "  Please let me know if you would like to authorize partial shipment for your remaining items." \
                      "  You will only be charged freight once."
            signoff = "\n\nI apologize for the inconvenience.  Let me know if you have any questions." \
                      "\n\nHave a great day,\n\n"
            if form.partial_shipment.data:
                body = body + partial + signoff
            else:
                body += signoff

            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/cstools/backorder.html",
                                   title="Backorder Template",
                                   link=link,
                                   form=form,
                                   color=color)

    elif request.method == 'GET':
        return render_template("/cstools/backorder.html",
                               title="Backorder Template",
                               form=form,
                               color=color)


@app.route('/cstools/application', methods=['GET', 'POST'])
def application():
    form = ApplicationForm()
    get_class_well.get_color()
    color = get_class_well.color

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/cstools/application.html",
                                   title="Account Application Template3",
                                   form=form,
                                   color=color)
        else:
            name = form.name.data
            email = form.email.data
            subject = "Cayman Chemical Account Application"
            body = "Hello %s,\n\nThank you for your interest in Cayman Chemical!  Before you can have your order " \
                   "processed and your items shipped you will need to establish an account with our company.  I have " \
                   "attached our customer account application which has all the instructions you will need, " \
                   "though please don't hesitate to call if you have any questions.\n\n" % name
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/cstools/application.html",
                                   title="Account Application Template1",
                                   link=link,
                                   form=form,
                                   color=color)
    elif request.method == 'GET':
        return render_template("/cstools/application.html",
                               title="Account Application Template2",
                               form=form,
                               color=color)


@app.route('/cstools/dea', methods=['GET', 'POST'])
def dea():
    form = DeaForm()
    get_class_well.get_color()
    color = get_class_well.color

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/cstools/dea.html",
                                   title="DEA Protocol Template",
                                   form=form,
                                   color=color)
        else:
            name = form.name.data
            email = form.email.data
            items = form.dea_items.data
            subject = "Cayman Chemical DEA Scheduled Compounds Protocol"
            body = "Hello %s,\n\nThank you for your order with Cayman Chemical!  This is an email to inform you " \
                   "that the following item(s) are DEA scheduled compounds and as such will require additional " \
                   "paperwork before they can be processed: %s.  Attached please find the Cayman Chemical " \
                   "protocol for ordering scheduled compounds as well as a guide for filling out the required 222 " \
                   "form.\n\nIf you have any questions, please don't hesitate to ask.\n\nThank you,\n\n" % (name, items)
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/cstools/dea.html",
                                   title="DEA Protocol Template",
                                   link=link,
                                   form=form,
                                   color=color)
    elif request.method == 'GET':
        return render_template("/cstools/dea.html",
                               title="DEA Protocol Template",
                               form=form,
                               color=color)


@app.route('/cstools/newaccount', methods=['GET', 'POST'])
def newaccount():
    form = NewAccountForm()
    get_class_well.get_color()
    color = get_class_well.color

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/cstools/newaccount.html",
                                   title="New Account Template",
                                   form=form,
                                   color=color)
        else:
            name = form.name.data
            acct_number = form.acct.data
            email = form.email.data
            subject = "New Account with Cayman Chemical"
            body = "Hello %s,\n\nThank you for your interest in Cayman Chemical!  A prepay account has been " \
                   "established for you.  We accept Visa, MasterCard, Discover, American Express, checks, and bank " \
                   "transfers.  If you would like net 30 terms, please provide bank and trade references.\n\nTo " \
                   "place an order, please contact customer service at one of the following:\n\nPhone:\t\t 800-364-9897" \
                   "\nFax:\t\t    734-971-3640\nEmail:\t\t  orders@caymanchem.com\nWebsite:\thttp://www.caymanchem.com" \
                   "\n\nWhen placing an order please reference customer account number %s.\n\nWe look forward to doing " \
                   "business with you!\n\n" % (name, acct_number)
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/cstools/newaccount.html",
                                   title="New Account Template",
                                   link=link,
                                   form=form,
                                   color=color)
    elif request.method == 'GET':
        return render_template("/cstools/newaccount.html",
                               title="New Account Template",
                               form=form,
                               color=color)


@app.route('/cstools/shadyblurb', methods=['GET', 'POST'])
def shadyblurb():
    form = ShadyForm()
    get_class_well.get_color()
    color = get_class_well.color

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/cstools/shadyblurb.html",
                                   title="Shady Customer Blurb",
                                   form=form,
                                   color=color)
        else:
            email = form.email.data
            order_no = form.order_no.data
            subject = "Cayman Chemical Web Order# %s" % order_no
            body = "To whom it may concern,\n\nCayman Chemical is a biochemical company dedicated to providing " \
                   "quality research grade material to pharmaceutical, academic, and medical institutions.  Our " \
                   "products are manufactured at Cayman Chemical for research purposes only and are not approved by " \
                   "the FDA for over-the-counter use in humans or animals as therapeutic agents.  If you can provide " \
                   "details of the research institution you are affiliated with we may be able to proceed " \
                   "with your order.  We do require that all new customers complete an account application that can " \
                   "be provided to you once we receive the requested information about your institution.\n\nPlease " \
                   "be advised that we do not deliver to residential addresses, P.O. boxes, or warehouses.  Only to " \
                   "businesses and institutions.\n\nThank you for your interest in Cayman Chemical products.  Please " \
                   "feel free to contact me if you have any questions.\n\nBest regards,\n\n"
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/cstools/shadyblurb.html",
                                   title="Shady Customer Blurb",
                                   link=link,
                                   form=form,
                                   color=color)
    elif request.method == 'GET':
        return render_template("/cstools/shadyblurb.html",
                               title="Shady Customer Blurb",
                               form=form,
                               color=color)


@app.route('/cstools/pricediscrepancy', methods=['GET', 'POST'])
def price_discrepancy():
    form = DiscrepancyForm()
    get_class_well.get_color()
    color = get_class_well.color

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/cstools/pricediscrepancy.html",
                                   title="Price Discrepancy Template",
                                   form=form,
                                   color=color)
        else:
            email = form.email.data
            subject = "Cayman Chemical Price Discrepancy %s" % form.po.data
            body = "Hello %s,\n\nWe have received your order but have a pricing discrepancy that needs to be " \
                   "resolved before we can ship any items.  For item #%s you reference a price of $%s but the " \
                   "item's actual cost is $%s.  Please confirm whether we should process or cancel the item.\n\n" \
                   "Please let me know if you have any questions,\n\n" % \
                   (form.name.data, form.item_number.data, form.given_price.data, form.actual_price.data)
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/cstools/pricediscrepancy.html",
                                   title="Price Discrepancy Template",
                                   link=link,
                                   form=form,
                                   color=color)

    elif request.method == 'GET':
        return render_template("/cstools/pricediscrepancy.html",
                               title="Price Discrepancy Template",
                               form=form,
                               color=color)


@app.route('/cstools/stillneed', methods=['GET', 'POST'])
def still_need():
    form = StillNeed()
    get_class_well.get_color()
    color = get_class_well.color

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/cstools/stillneed.html",
                                   title="Still Need Item? Template",
                                   form=form,
                                   color=color)
        else:
            name = form.name.data
            email = form.email.data
            item = form.item_number.data
            order_no = form.order_no.data
            subject = "Regarding your Cayman Chemical Order %s" % order_no
            body = "Hello %s,\n\nYour order for item #%s is now available and ready to ship!  Since the item has " \
                   "been on a lengthy backorder we're sending this email to verify that you still need the item and " \
                   "would like it to be shipped as soon as possible.  Please let me know how you would like " \
                   "to proceed.\n\n" % (name, item)
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/cstools/stillneed.html",
                                   title="Still Need Item? Template",
                                   link=link,
                                   form=form,
                                   color=color)
    elif request.method == 'GET':
        return render_template("/cstools/stillneed.html",
                               title="Still Need Item? Template",
                               form=form,
                               color=color)


@app.route('/cstools/licenseneeded', methods=['GET', 'POST'])
def license_needed():
    form = LicenseNeeded()
    get_class_well.get_color()
    color = get_class_well.color

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/cstools/licenseneeded.html",
                                   title="DEA License Needed Template",
                                   form=form,
                                   color=color)
        else:
            name = form.name.data
            email = form.email.data
            order_no = form.order_no.data
            subject = "DEA License Still Needed Order #%s" % order_no
            body = "Hello %s,\n\nWe have received your 222 form but we still need an updated copy of your DEA " \
                   "registration before the order can be processed.  Unlike the 222 form, the registration does not " \
                   "need to be an original - you can simply scan your license and email it to me.  Please send us " \
                   "your license as soon as possible to ensure prompt delivery of your order.\n\n" % name
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/cstools/licenseneeded.html",
                                   title="DEA License Needed Template",
                                   link=link,
                                   form=form,
                                   color=color)
    elif request.method == 'GET':
        return render_template("/cstools/licenseneeded.html",
                               title="DEA License Needed Template",
                               form=form,
                               color=color)


@app.route('/cstools/deaverify', methods=['GET', 'POST'])
def dea_verify():
    form = DeaVerify()
    get_class_well.get_color()
    color = get_class_well.color

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/cstools/deaverify.html",
                                   title="DEA Documents Verification Template",
                                   form=form,
                                   color=color)
        else:
            email = "Compliance@caymanchem.com; DEAorderprocessing@caymanchem.com"
            order_no = form.order_no.data
            institution = form.institution.data
            subject = "%s / %s" % (order_no, institution)
            body = "Hello,\n\nPlease verify these documents.\n\n"
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/cstools/deaverify.html",
                                   title="DEA Documents Verification Template",
                                   link=link,
                                   form=form,
                                   color=color)
    elif request.method == 'GET':
        return render_template("/cstools/deaverify.html",
                               title="DEA Documents Verification Template",
                               form=form,
                               color=color)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            error = 'You need to log in first.'
            return render_template('/cstools/login.html',
                                   title='Login',
                                   error=error)
    return wrap


@app.route('/cstools/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'cs' or request.form['password'] != 'cayman':
            error = 'Invalid credentials, please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('forms_without_orders'))
    return render_template('/cstools/login.html',
                           title='Login',
                           error=error)


@app.route('/cstools/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
        return redirect(url_for('cstools'))
    else:
        return redirect(url_for('cstools'))


@app.route('/cstools/forms-without-orders', methods=['GET', 'POST'])
@login_required
def forms_without_orders():
    form = DeaForms()
    if request.method == 'POST':
        if not form.validate():
            entries = models.Entry.query.all()
            flash('All fields are required.')
            return render_template("/cstools/forms_without_orders.html",
                                   title="DEA Forms Without Orders",
                                   form=form,
                                   entries=entries,
                                   new_entry=True)
        else:
            get_class_li.get_color()

            color = get_class_li.color
            institution = form.institution.data
            name = form.name.data
            email = form.email.data
            csr_name = form.csr_name.data
            item_numbers = form.item_numbers.data
            notes = form.notes.data
            now = datetime.datetime.utcnow()
            date_nice = now.strftime('%m/%d/%Y')

            entry = models.Entry(institution=institution,
                                 contact_name=name,
                                 contact_email=email,
                                 timestamp=date_nice,
                                 item_numbers=item_numbers,
                                 notes=notes,
                                 csr_name=csr_name,
                                 color=color)

            db.session.add(entry)
            db.session.commit()

            entries = models.Entry.query.all()

            message = 'Successfully added entry for %s.' % institution

            return render_template("/cstools/forms_without_orders.html",
                                   title="DEA Forms Without Orders",
                                   entries=entries,
                                   message=message)
    elif request.method == 'GET':
        entries = models.Entry.query.all()
        return render_template("/cstools/forms_without_orders.html",
                               title="DEA Forms Without Orders",
                               entries=entries)


@app.route('/cstools/forms-without-orders/new-entry')
@login_required
def new_entry():
    form = DeaForms()
    entries = models.Entry.query.all()
    return render_template("/cstools/forms_without_orders.html",
                           title="DEA Forms Without Orders",
                           form=form,
                           entries=entries,
                           new_entry=True)


@app.route('/cstools/forms-without-orders/edit-entry/<id>')
@login_required
def edit_entry(id):
    entry = models.Entry.query.get(id)

    return render_template("/cstools/forms_without_orders_edit.html",
                           title="DEA Forms Without Orders - Edit Entry",
                           entry=entry)


@app.route('/cstools/forms-without-orders/update-entry/<id>', methods=['GET', 'POST'])
@login_required
def update_entry(id):
    form = DeaForms()
    entry = models.Entry.query.get(id)
    if form.validate_on_submit():
        entry.institution = form.institution.data
        entry.contact_name = form.name.data
        entry.contact_email = form.email.data
        entry.csr_name = form.csr_name.data
        entry.item_numbers = form.item_numbers.data
        entry.notes = form.notes.data

        db.session.commit()

        entries = models.Entry.query.all()
        message = 'The entry for %s has been updated.' % entry.institution

        return render_template("/cstools/forms_without_orders.html",
                               title="DEA Forms Without Orders",
                               entries=entries,
                               message=message)

    form.institution.data = entry.institution
    form.name.data = entry.contact_name
    form.email.data = entry.contact_email
    form.item_numbers.data = entry.item_numbers
    form.notes.data = entry.notes
    form.csr_name.data = entry.csr_name

    return render_template("/cstools/forms_without_orders_update.html",
                           title="DEA Forms Without Orders - Update Entry",
                           entry=entry,
                           form=form)


@app.route('/cstools/forms-without-orders/delete-entry/<id>')
@login_required
def delete_entry(id):
    entry = models.Entry.query.get(id)

    db.session.delete(entry)
    db.session.commit()

    entries = models.Entry.query.all()

    message = "Successfully deleted entry for %s." % entry.institution

    return render_template("/cstools/forms_without_orders.html",
                           title="DEA Forms Without Orders",
                           message=message,
                           entries=entries)


##############################################################################
## Reddit Image Scraper
##############################################################################
@app.route('/scrape_reddit', methods=['GET', 'POST'])
def scrape_home():
    form = RedditImageScraper()
    suggestions = ['pugs', 'earthporn', 'kittens', 'gaming', 'pics', 'awww', 'funny', 'adviceanimals', 'gifs',
                   'wallpapers', 'foodporn', 'historyporn', 'photoshopbattles', 'mildlyinteresting', 'woahdude',
                   'oldschoolcool', 'perfecttiming', 'abandonedporn', 'roomporn']
    picks = []
    for number in range(0, 4):
        pick = random.choice(suggestions)
        if pick in picks:
            continue
        else:
            picks.append(pick)

    return render_template('/reddit_scraper/home.html',
                           form=form,
                           picks=picks)


@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    form = RedditImageScraper()
    suggestions = ['pugs', 'earthporn', 'kittens', 'gaming', 'pics', 'awww', 'funny', 'adviceanimals', 'gifs',
                   'wallpapers', 'foodporn', 'historyporn', 'photoshopbattles', 'mildlyinteresting', 'woahdude',
                   'oldschoolcool', 'perfecttiming', 'abandonedporn', 'roomporn']
    picks = []
    for number in range(0, 4):
        pick = random.choice(suggestions)
        if pick in picks:
            continue
        else:
            picks.append(pick)

    if request.method == 'POST':
        if not form.validate():
            return render_template('/reddit_scraper/home.html',
                                   form=form,
                                   picks=picks)
        else:
            form = RedditImageScraper()

            def find_string(sub_string):
                return re.compile(r'\b({0})\b'.format(sub_string), flags=re.IGNORECASE).search

            subreddit = str(form.subreddit_choice.data)

            try:
                min_score = int(form.minimum_score.data)
            except ValueError:
                message = 'Enter a numerical value for minimum score'
                return render_template('/reddit_scraper/home.html',
                                       form=form,
                                       picks=picks,
                                       message=message)

            results_from = int(form.results_from.data)
            number = int(form.number.data)
            good_urls = []
            indirect_urls = []

            r = praw.Reddit(user_agent='reddit scraper by billcrystals')

            if results_from == 1:
                submissions = r.get_subreddit(subreddit).get_hot(limit=number)
                results_from = 'Hot'
            elif results_from == 2:
                submissions = r.get_subreddit(subreddit).get_top_from_all(limit=number)
                results_from = 'All'
            elif results_from == 3:
                submissions = r.get_subreddit(subreddit).get_top_from_year(limit=number)
                results_from = 'Year'
            else:
                submissions = r.get_subreddit(subreddit).get_top_from_month(limit=number)
                results_from = 'Month'

            try:
                for submission in submissions:
                    if submission.score < min_score:
                        print 'Submission (%s) lower than requested min score.' % submission.url
                        continue
                    elif submission.url.startswith('imgur.com/'):
                        endpoint = submission.url.find('.com/')
                        url = 'i.' + submission.url[:endpoint] + '.jpg'
                        good_urls.append([url, submission.short_link, submission.title])
                    elif find_string('/r/')(submission.url):
                        if find_string('imgur')(submission.url):
                            print '/r/ found in %s' % submission.url
                            endpoint = submission.url.rfind('/')
                            url = 'http://i.imgur.com' + submission.url[endpoint:] + '.jpg'
                            good_urls.append([url, submission.short_link, submission.title])
                        else:
                            indirect_urls.append([submission.url, submission.short_link])
                    elif find_string('/gallery/')(submission.url):
                        print 'Submission (%s) is an Imgur album link' % submission.url
                        indirect_urls.append([submission.url, submission.short_link])
                    elif find_string('http://imgur.com/')(submission.url):
                        if find_string('/a/')(submission.url):
                            print 'Submission (%s) is an Imgur album link' % submission.url
                            indirect_urls.append([submission.url, submission.short_link])
                        else:
                            endpoint = submission.url.find('.com/')
                            url = submission.url[endpoint + 5:]
                            new_url = 'http://i.imgur.com/%s.jpg' % url
                            if len(submission.title) > 75:
                                try:
                                    submission.title = str(submission.title[:75]) + '...'
                                    good_urls.append([new_url, submission.short_link, submission.title])
                                except UnicodeError:
                                    continue
                            else:
                                good_urls.append([new_url, submission.short_link, submission.title])
                    elif find_string('qkme')(submission.url):
                        print 'QKME link, adding to indirect_urls...'
                        indirect_urls.append([submission.url, submission.short_link])
                    elif find_string('youtube')(submission.url):
                        print 'Youtube link, adding to indirect_urls...'
                        indirect_urls.append([submission.url, submission.short_link])
                    elif find_string('twitter')(submission.url):
                        print 'Twitter link, adding to indirect_urls...'
                        indirect_urls.append([submission.url, submission.short_link])
                    elif '?' in submission.url:
                        endpoint = submission.url.find('?')
                        url = submission.url[:endpoint]
                        if len(submission.title) > 75:
                            try:
                                submission.title = str(submission.title[:75]) + '...'
                                good_urls.append([url, submission.short_link, submission.title])
                            except UnicodeError:
                                continue
                        else:
                            good_urls.append([url, submission.short_link, submission.title])
                    elif not submission.url.endswith(('.gif', '.png', '.jpg', '.jpeg')):
                        print 'Indirect URL: %s' % submission.url
                        indirect_urls.append([submission.url, submission.short_link])
                    else:
                        if len(submission.title) > 75:
                            try:
                                submission.title = str(submission.title[:75]) + '...'
                                good_urls.append([submission.url, submission.short_link, submission.title])
                            except UnicodeError:
                                continue
                        else:
                            good_urls.append([submission.url, submission.short_link, submission.title])
            except (praw.errors.RedirectException, requests.HTTPError):
                message = 'It looks like /r/%s doesn\'t exist!' % subreddit
                return render_template('/reddit_scraper/home.html',
                                       form=form,
                                       message=message,
                                       picks=picks)

            good_urls_number = len(good_urls)
            indirect_urls_number = len(indirect_urls)

            return render_template('/reddit_scraper/results.html',
                                   good_urls=good_urls,
                                   indirect_urls=indirect_urls,
                                   good_urls_number=good_urls_number,
                                   indirect_urls_number=indirect_urls_number,
                                   subreddit=subreddit,
                                   min_score=min_score,
                                   results_from=results_from,
                                   number=number)
    else:
        return render_template('/reddit_scraper/home.html',
                               form=form)