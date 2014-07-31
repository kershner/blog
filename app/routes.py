from flask import Flask, render_template, request, flash, redirect, url_for, session
from forms import DateCheckerForm, BackorderForm, ApplicationForm, DeaForm, NewAccountForm, ShadyForm, DiscrepancyForm,\
    StillNeed, LicenseNeeded, DeaVerify, DeaForms, SlideshowDelay
from urllib import quote
import datetime
import random
from functools import wraps
from app import app, db, models

##############################################################################
## Blog ######################################################################
@app.route('/')
def home():
    return render_template("/blog/home.html",
                           title="Home")


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
## Raspberry Pi GIF Display ##################################################
@app.route('/pi_display')
def pi_display():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    # Will use these later for general purpose GIF display site
    # gif_width = config_file_list[0][config_file_list[0].find('=') + 2:config_file_list[0].find('x')]
    # gif_height = config_file_list[0][config_file_list[0].find('x') + 1:config_file_list[0].find('\n')]

    category = config_file_list[1][config_file_list[1].find('=') + 2:config_file_list[1].find('\n')]
    delay = config_file_list[3][config_file_list[3].find('=') + 2:config_file_list[3].find('\n')]

    if category == 'all':
        filename = 'urls.txt'
        toplay_filename = 'urls_to_play.txt'
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

    # Opening/closing urls.txt (taking advantage of side effect to erase contents)
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

    return render_template("/pi_display/pi_display.html",
                           title="Raspberry PI GIF Display",
                           gif_url=gif_url,
                           delay=delay)


@app.route('/pi_display_config', methods=['GET', 'POST'])
def pi_display_config():
    form = SlideshowDelay()
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/urls.txt' % path, 'r') as urls_file:
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
                               title="Raspberry Pi GIF Display Configuration",
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
    path = '/home/tylerkershner/app/templates/pi_display/logs'

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
    path = '/home/tylerkershner/app/templates/pi_display/logs'

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
    path = '/home/tylerkershner/app/templates/pi_display/logs'

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
    path = '/home/tylerkershner/app/templates/pi_display/logs'

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
    path = '/home/tylerkershner/app/templates/pi_display/logs'

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
    path = '/home/tylerkershner/app/templates/pi_display/logs'

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
    path = '/home/tylerkershner/app/templates/pi_display/logs'

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
    path = '/home/tylerkershner/app/templates/pi_display/logs'

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
## Gif Party #################################################################
@app.route('/gif_party')
def gif_party():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/gif_party_config.txt' % path, 'r') as config:
            config_file_list = list(config)

    category = config_file_list[0][config_file_list[0].find('=') + 2:config_file_list[0].find('\n')]
    delay = config_file_list[1][config_file_list[1].find('=') + 2:config_file_list[1].find('\n')]
    number = int(config_file_list[2][config_file_list[2].find('=') + 2:config_file_list[2].find('\n')])
    randomize = config_file_list[3][config_file_list[3].find('=') + 2:config_file_list[3].find('\n')]

    if category == 'all':
        filename = 'urls.txt'
    elif category == 'animals':
        filename = 'animals_urls.txt'
    elif category == 'gaming':
        filename = 'gaming_urls.txt'
    elif category == 'strange':
        filename = 'strange_urls.txt'
    elif category == 'educational':
        filename = 'educational_urls.txt'

    with open('%s/%s' % (path, filename), 'r') as urls_file:
        urls_list = list(urls_file)

    with open('%s/urls.txt' % path, 'r') as last_played_file:
        all_urls_list = list(last_played_file)

    with open('%s/last_played.txt' % path, 'r') as last_played_file:
        last_played_list = list(last_played_file)

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

    if number == 5:
        if randomize == 'yes':
            gif_url_1 = random.choice(urls_list)
            urls_list.remove(gif_url_1)
            gif_url_2 = random.choice(urls_list)
            urls_list.remove(gif_url_2)
            gif_url_3 = random.choice(urls_list)
            urls_list.remove(gif_url_3)
            gif_url_4 = random.choice(urls_list)
            urls_list.remove(gif_url_4)
            gif_url_5 = random.choice(urls_list)
            urls_list.remove(gif_url_5)
        else:
            gif_url_1 = last_played_list[-21][:last_played_list[-21].find('\n')]
            gif_url_2 = last_played_list[-20][:last_played_list[-20].find('\n')]
            gif_url_3 = last_played_list[-19][:last_played_list[-19].find('\n')]
            gif_url_4 = last_played_list[-18][:last_played_list[-18].find('\n')]
            gif_url_5 = last_played_list[-17][:last_played_list[-17].find('\n')]

        return render_template('/pi_display/gif_party.html',
                               urls_count=main_urls_count,
                               animals_urls_count=animals_urls_count,
                               gaming_urls_count=gaming_urls_count,
                               strange_urls_count=strange_urls_count,
                               educational_urls_count=educational_urls_count,
                               category=category,
                               randomize=randomize,
                               gif_url_1=gif_url_1,
                               gif_url_2=gif_url_2,
                               gif_url_3=gif_url_3,
                               gif_url_4=gif_url_4,
                               gif_url_5=gif_url_5,
                               number=number)
    elif number == 10:
        if randomize == 'yes':
            gif_url_1 = random.choice(urls_list)
            urls_list.remove(gif_url_1)
            gif_url_2 = random.choice(urls_list)
            urls_list.remove(gif_url_2)
            gif_url_3 = random.choice(urls_list)
            urls_list.remove(gif_url_3)
            gif_url_4 = random.choice(urls_list)
            urls_list.remove(gif_url_4)
            gif_url_5 = random.choice(urls_list)
            urls_list.remove(gif_url_5)
            gif_url_6 = random.choice(urls_list)
            urls_list.remove(gif_url_6)
            gif_url_7 = random.choice(urls_list)
            urls_list.remove(gif_url_7)
            gif_url_8 = random.choice(urls_list)
            urls_list.remove(gif_url_8)
            gif_url_9 = random.choice(urls_list)
            urls_list.remove(gif_url_9)
            gif_url_10 = random.choice(urls_list)
            urls_list.remove(gif_url_10)
        else:
            gif_url_1 = last_played_list[-21][:last_played_list[-21].find('\n')]
            gif_url_2 = last_played_list[-20][:last_played_list[-20].find('\n')]
            gif_url_3 = last_played_list[-19][:last_played_list[-19].find('\n')]
            gif_url_4 = last_played_list[-18][:last_played_list[-18].find('\n')]
            gif_url_5 = last_played_list[-17][:last_played_list[-17].find('\n')]
            gif_url_6 = last_played_list[-16][:last_played_list[-16].find('\n')]
            gif_url_7 = last_played_list[-15][:last_played_list[-15].find('\n')]
            gif_url_8 = last_played_list[-14][:last_played_list[-14].find('\n')]
            gif_url_9 = last_played_list[-13][:last_played_list[-13].find('\n')]
            gif_url_10 = last_played_list[-12][:last_played_list[-12].find('\n')]

        return render_template('/pi_display/gif_party.html',
                               urls_count=main_urls_count,
                               animals_urls_count=animals_urls_count,
                               gaming_urls_count=gaming_urls_count,
                               strange_urls_count=strange_urls_count,
                               educational_urls_count=educational_urls_count,
                               category=category,
                               randomize=randomize,
                               gif_url_1=gif_url_1,
                               gif_url_2=gif_url_2,
                               gif_url_3=gif_url_3,
                               gif_url_4=gif_url_4,
                               gif_url_5=gif_url_5,
                               gif_url_6=gif_url_6,
                               gif_url_7=gif_url_7,
                               gif_url_8=gif_url_8,
                               gif_url_9=gif_url_9,
                               gif_url_10=gif_url_10,
                               number=number)
    elif number == 20:
        if randomize == 'yes':
            gif_url_1 = random.choice(urls_list)
            urls_list.remove(gif_url_1)
            gif_url_2 = random.choice(urls_list)
            urls_list.remove(gif_url_2)
            gif_url_3 = random.choice(urls_list)
            urls_list.remove(gif_url_3)
            gif_url_4 = random.choice(urls_list)
            urls_list.remove(gif_url_4)
            gif_url_5 = random.choice(urls_list)
            urls_list.remove(gif_url_5)
            gif_url_6 = random.choice(urls_list)
            urls_list.remove(gif_url_6)
            gif_url_7 = random.choice(urls_list)
            urls_list.remove(gif_url_7)
            gif_url_8 = random.choice(urls_list)
            urls_list.remove(gif_url_8)
            gif_url_9 = random.choice(urls_list)
            urls_list.remove(gif_url_9)
            gif_url_10 = random.choice(urls_list)
            urls_list.remove(gif_url_10)
            gif_url_11 = random.choice(urls_list)
            urls_list.remove(gif_url_11)
            gif_url_12 = random.choice(urls_list)
            urls_list.remove(gif_url_12)
            gif_url_13 = random.choice(urls_list)
            urls_list.remove(gif_url_13)
            gif_url_14 = random.choice(urls_list)
            urls_list.remove(gif_url_14)
            gif_url_15 = random.choice(urls_list)
            urls_list.remove(gif_url_15)
            gif_url_16 = random.choice(urls_list)
            urls_list.remove(gif_url_16)
            gif_url_17 = random.choice(urls_list)
            urls_list.remove(gif_url_17)
            gif_url_18 = random.choice(urls_list)
            urls_list.remove(gif_url_18)
            gif_url_19 = random.choice(urls_list)
            urls_list.remove(gif_url_19)
            gif_url_20 = random.choice(urls_list)
            urls_list.remove(gif_url_20)
        else:
            gif_url_1 = last_played_list[-21][:last_played_list[-21].find('\n')]
            gif_url_2 = last_played_list[-20][:last_played_list[-20].find('\n')]
            gif_url_3 = last_played_list[-19][:last_played_list[-19].find('\n')]
            gif_url_4 = last_played_list[-18][:last_played_list[-18].find('\n')]
            gif_url_5 = last_played_list[-17][:last_played_list[-17].find('\n')]
            gif_url_6 = last_played_list[-16][:last_played_list[-16].find('\n')]
            gif_url_7 = last_played_list[-15][:last_played_list[-15].find('\n')]
            gif_url_8 = last_played_list[-14][:last_played_list[-14].find('\n')]
            gif_url_9 = last_played_list[-13][:last_played_list[-13].find('\n')]
            gif_url_10 = last_played_list[-12][:last_played_list[-12].find('\n')]
            gif_url_11 = last_played_list[-11][:last_played_list[-11].find('\n')]
            gif_url_12 = last_played_list[-10][:last_played_list[-10].find('\n')]
            gif_url_13 = last_played_list[-9][:last_played_list[-9].find('\n')]
            gif_url_14 = last_played_list[-8][:last_played_list[-8].find('\n')]
            gif_url_15 = last_played_list[-7][:last_played_list[-7].find('\n')]
            gif_url_16 = last_played_list[-6][:last_played_list[-6].find('\n')]
            gif_url_17 = last_played_list[-5][:last_played_list[-5].find('\n')]
            gif_url_18 = last_played_list[-4][:last_played_list[-4].find('\n')]
            gif_url_19 = last_played_list[-3][:last_played_list[-3].find('\n')]
            gif_url_20 = last_played_list[-2][:last_played_list[-2].find('\n')]

        return render_template('/pi_display/gif_party.html',
                               urls_count=main_urls_count,
                               animals_urls_count=animals_urls_count,
                               gaming_urls_count=gaming_urls_count,
                               strange_urls_count=strange_urls_count,
                               educational_urls_count=educational_urls_count,
                               category=category,
                               randomize=randomize,
                               gif_url_1=gif_url_1,
                               gif_url_2=gif_url_2,
                               gif_url_3=gif_url_3,
                               gif_url_4=gif_url_4,
                               gif_url_5=gif_url_5,
                               gif_url_6=gif_url_6,
                               gif_url_7=gif_url_7,
                               gif_url_8=gif_url_8,
                               gif_url_9=gif_url_9,
                               gif_url_10=gif_url_10,
                               gif_url_11=gif_url_11,
                               gif_url_12=gif_url_12,
                               gif_url_13=gif_url_13,
                               gif_url_14=gif_url_14,
                               gif_url_15=gif_url_15,
                               gif_url_16=gif_url_16,
                               gif_url_17=gif_url_17,
                               gif_url_18=gif_url_18,
                               gif_url_19=gif_url_19,
                               gif_url_20=gif_url_20,
                               number=number)


@app.route('/gif_party_all')
def gif_party_all():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/gif_party_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/gif_party_config.txt' % path, 'w+') as config_file:
        config_file.write('CATEGORY = all' + '\n')
        config_file.write(config_file_list[1])
        config_file.write(config_file_list[2])
        config_file.write(config_file_list[3])

    return redirect(url_for('gif_party'))


@app.route('/gif_party_animals')
def gif_party_animals():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/gif_party_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/gif_party_config.txt' % path, 'w+') as config_file:
        config_file.write('CATEGORY = animals' + '\n')
        config_file.write(config_file_list[1])
        config_file.write(config_file_list[2])
        config_file.write(config_file_list[3])

    return redirect(url_for('gif_party'))


@app.route('/gif_party_gaming')
def gif_party_gaming():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/gif_party_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/gif_party_config.txt' % path, 'w+') as config_file:
        config_file.write('CATEGORY = gaming' + '\n')
        config_file.write(config_file_list[1])
        config_file.write(config_file_list[2])
        config_file.write(config_file_list[3])

    return redirect(url_for('gif_party'))


@app.route('/gif_party_strange')
def gif_party_strange():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/gif_party_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/gif_party_config.txt' % path, 'w+') as config_file:
        config_file.write('CATEGORY = strange' + '\n')
        config_file.write(config_file_list[1])
        config_file.write(config_file_list[2])
        config_file.write(config_file_list[3])

    return redirect(url_for('gif_party'))


@app.route('/gif_party_educational')
def gif_party_educational():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/gif_party_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/gif_party_config.txt' % path, 'w+') as config_file:
        config_file.write('CATEGORY = educational' + '\n')
        config_file.write(config_file_list[1])
        config_file.write(config_file_list[2])
        config_file.write(config_file_list[3])

    return redirect(url_for('gif_party'))


@app.route('/gif_party_5')
def gif_party_5():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/gif_party_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/gif_party_config.txt' % path, 'w+') as config_file:
        config_file.write(config_file_list[0])
        config_file.write(config_file_list[1])
        config_file.write('NUMBER = 5' + '\n')
        config_file.write(config_file_list[3])

    return redirect(url_for('gif_party'))


@app.route('/gif_party_10')
def gif_party_10():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/gif_party_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/gif_party_config.txt' % path, 'w+') as config_file:
        config_file.write(config_file_list[0])
        config_file.write(config_file_list[1])
        config_file.write('NUMBER = 10' + '\n')
        config_file.write(config_file_list[3])

    return redirect(url_for('gif_party'))


@app.route('/gif_party_20')
def gif_party_20():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/gif_party_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/gif_party_config.txt' % path, 'w+') as config_file:
        config_file.write(config_file_list[0])
        config_file.write(config_file_list[1])
        config_file.write('NUMBER = 20' + '\n')
        config_file.write(config_file_list[3])

    return redirect(url_for('gif_party'))


@app.route('/gif_party_randomize')
def gif_party_randomize():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/gif_party_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/gif_party_config.txt' % path, 'w+') as config_file:
        config_file.write(config_file_list[0])
        config_file.write(config_file_list[1])
        config_file.write(config_file_list[2])
        config_file.write('RANDOMIZE = yes' + '\n')

    return redirect(url_for('gif_party'))


@app.route('/gif_party_feed')
def gif_party_feed():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/gif_party_config.txt' % path, 'r') as config_file:
        config_file_list = list(config_file)

    with open('%s/gif_party_config.txt' % path, 'w+') as config_file:
        config_file.write(config_file_list[0])
        config_file.write(config_file_list[1])
        config_file.write(config_file_list[2])
        config_file.write('RANDOMIZE = no' + '\n')

    return redirect(url_for('gif_party'))


#######################################################################################
#####  CS Tools Apps ##################################################################
@app.route('/cstools')
@app.route('/cstools/index')
def index():
    return render_template("/CSTools/index.html",
                           title="Home")


@app.route('/cstools/datechecker', methods=['GET', 'POST'])
def datechecker():
    form = DateCheckerForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template("/CSTools/datechecker.html",
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

                return render_template("/CSTools/datechecker.html",
                                       title="222 Form Date Checker",
                                       form=form,
                                       message=message)
            except ValueError:
                message = "Enter the form's issue date in the format MM/DD/YY."
                return render_template("/CSTools/datechecker.html",
                                       title="222 Form Date Checker",
                                       form=form,
                                       message=message)
    elif request.method == 'GET':
        return render_template("/CSTools/datechecker.html",
                               title="222 Form Date Checker",
                               form=form)


@app.route('/cstools/backorder', methods=['GET', 'POST'])
def backorder():
    form = BackorderForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/CSTools/backorder.html",
                                   title="Backorder Template",
                                   form=form)
        else:
            email = form.email.data
            subject = "Cayman Chemical Backorder Notification %s" % form.po.data
            body = "Hello %s,\n\nUnfortunately we need to inform you that one "\
                   "of your items is currently not available.  Item # %s is " \
                   "in production with an approximate lead time of %s.\n\nI " \
                   "apologize for the inconvenience.  Please let me know if " \
                   "you have any questions.\n\nHave a great day,\n\n" % \
                   (form.name.data, form.item_number.data, form.lead_time.data)
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/CSTools/backorder.html",
                                   title="Backorder Template",
                                   link=link,
                                   form=form)

    elif request.method == 'GET':
        return render_template("/CSTools/backorder.html",
                               title="Backorder Template",
                               form=form)


@app.route('/cstools/application', methods=['GET', 'POST'])
def application():
    form = ApplicationForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/CSTools/application.html",
                                   title="Account Application Template3",
                                   form=form)
        else:
            name = form.name.data
            email = form.email.data
            subject = "Cayman Chemical Account Application"
            body = "Hello %s,\n\nThank you for your interest in Cayman Chemical!  Before you can have your order " \
                   "processed and your items shipped you will need to establish an account with our company.  I have " \
                   "attached our customer account application which has all the instructions you will need, " \
                   "though please don't hesitate to call if you have any questions.\n\n" % name
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/CSTools/application.html",
                                   title="Account Application Template1",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("/CSTools/application.html",
                               title="Account Application Template2",
                               form=form)


@app.route('/cstools/dea', methods=['GET', 'POST'])
def dea():
    form = DeaForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/CSTools/dea.html",
                                   title="DEA Protocol Template",
                                   form=form)
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
            return render_template("/CSTools/dea.html",
                                   title="DEA Protocol Template",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("/CSTools/dea.html",
                               title="DEA Protocol Template",
                               form=form)


@app.route('/cstools/newaccount', methods=['GET', 'POST'])
def newaccount():
    form = NewAccountForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/CSTools/newaccount.html",
                                   title="New Account Template",
                                   form=form)
        else:
            name = form.name.data
            acct_number = form.acct.data
            email = form.email.data
            subject = "New Account with Cayman Chemical"
            body = "Hello %s,\n\nThank you for your interest in Cayman Chemical!  A prepay account has been " \
                   "established for you.  We accept Visa, MasterCard, Discover, American Express, checks, and bank " \
                   "transfers.  If you would like net 30 terms, please provide trade references.\n\nTo place an " \
                   "order, please contact customer service at one of the following:\n\nPhone:\t\t\t 800-364-9897\n" \
                   "Fax:order please reference customer account number %s.\n\nWe look forward to doing business with " \
                   "you!\n\n" % (name, acct_number)
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/CSTools/newaccount.html",
                                   title="New Account Template",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("/CSTools/newaccount.html",
                               title="New Account Template",
                               form=form)


@app.route('/cstools/shadyblurb', methods=['GET', 'POST'])
def shadyblurb():
    form = ShadyForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/CSTools/shadyblurb.html",
                                   title="Shady Customer Blurb",
                                   form=form)
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
            return render_template("/CSTools/shadyblurb.html",
                                   title="Shady Customer Blurb",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("/CSTools/shadyblurb.html",
                               title="Shady Customer Blurb",
                               form=form)


@app.route('/cstools/pricediscrepancy', methods=['GET', 'POST'])
def price_discrepancy():
    form = DiscrepancyForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/CSTools/pricediscrepancy.html",
                                   title="Price Discrepancy Template",
                                   form=form)
        else:
            email = form.email.data
            subject = "Cayman Chemical Price Discrepancy %s" % form.po.data
            body = "Hello %s,\n\nWe have received your order but have a pricing discrepancy that needs to be " \
                   "resolved before we can ship any items.  For item #%s you reference a price of $%s but the " \
                   "item's actual cost is $%s.  Please confirm whether we should process or cancel the item.\n\n" \
                   "Please let me know if you have any questions,\n\n" % \
                   (form.name.data, form.item_number.data, form.given_price.data, form.actual_price.data)
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/CSTools/pricediscrepancy.html",
                                   title="Price Discrepancy Template",
                                   link=link,
                                   form=form)

    elif request.method == 'GET':
        return render_template("/CSTools/pricediscrepancy.html",
                               title="Price Discrepancy Template",
                               form=form)


@app.route('/cstools/stillneed', methods=['GET', 'POST'])
def still_need():
    form = StillNeed()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/CSTools/stillneed.html",
                                   title="Still Need Item? Template",
                                   form=form)
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
            return render_template("/CSTools/stillneed.html",
                                   title="Still Need Item? Template",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("/CSTools/stillneed.html",
                               title="Still Need Item? Template",
                               form=form)


@app.route('/cstools/licenseneeded', methods=['GET', 'POST'])
def license_needed():
    form = LicenseNeeded()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/CSTools/licenseneeded.html",
                                   title="DEA License Needed Template",
                                   form=form)
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
            return render_template("/CSTools/licenseneeded.html",
                                   title="DEA License Needed Template",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("/CSTools/licenseneeded.html",
                               title="DEA License Needed Template",
                               form=form)


@app.route('/cstools/deaverify', methods=['GET', 'POST'])
def dea_verify():
    form = DeaVerify()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/CSTools/deaverify.html",
                                   title="DEA Documents Verification Template",
                                   form=form)
        else:
            email = "Compliance@caymanchem.com; DEAorderprocessing@caymanchem.com"
            order_no = form.order_no.data
            institution = form.institution.data
            subject = "%s / %s" % (order_no, institution)
            body = "Hello,\n\nPlease verify these documents.\n\n"
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/CSTools/deaverify.html",
                                   title="DEA Documents Verification Template",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("/CSTools/deaverify.html",
                               title="DEA Documents Verification Template",
                               form=form)


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            error = 'You need to log in first.'
            return render_template('/CSTools/login.html',
                                   title='Login',
                                   error=error)
    return wrap


@app.route('/cstools/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'cs'or request.form['password'] != 'cayman':
            error = 'Invalid credentials, please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('forms_without_orders'))
    return render_template('/CSTools/login.html',
                           title='Login',
                           error=error)

@app.route('/cstools/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/cstools/forms-without-orders', methods=['GET', 'POST'])
@login_required
def forms_without_orders():
    form = DeaForms()
    if request.method == 'POST':
        if not form.validate():
            entries = models.Entry.query.all()
            flash('All fields are required.')
            return render_template("/CSTools/forms_without_orders.html",
                                   title="DEA Forms Without Orders",
                                   form=form,
                                   entries=entries,
                                   new_entry=True)
        else:
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
                                 csr_name=csr_name)

            db.session.add(entry)
            db.session.commit()

            entries = models.Entry.query.all()

            message = 'Successfully added entry for %s.' % institution

            return render_template("/CSTools/forms_without_orders.html",
                                   title="DEA Forms Without Orders",
                                   entries=entries,
                                   message=message)
    elif request.method == 'GET':
        entries = models.Entry.query.all()
        return render_template("/CSTools/forms_without_orders.html",
                               title="DEA Forms Without Orders",
                               entries=entries)


@app.route('/cstools/forms-without-orders/new-entry')
@login_required
def new_entry():
    form = DeaForms()
    entries = models.Entry.query.all()
    return render_template("/CSTools/forms_without_orders.html",
                           title="DEA Forms Without Orders",
                           form=form,
                           entries=entries,
                           new_entry=True)


@app.route('/cstools/forms-without-orders/edit-entry/<id>')
@login_required
def edit_entry(id):
    entry = models.Entry.query.get(id)

    return render_template("/CSTools/forms_without_orders_delete.html",
                           title="DEA Forms Without Orders - Edit Entry",
                           entry=entry)


@app.route('/cstools/forms-without-orders/delete-entry/<id>')
@login_required
def delete_entry(id):
    entry = models.Entry.query.get(id)

    db.session.delete(entry)
    db.session.commit()

    entries = models.Entry.query.all()

    message = "Successfully deleted entry for %s." % entry.institution

    return render_template("/CSTools/forms_without_orders.html",
                                   title="DEA Forms Without Orders",
                                   message=message,
                                   entries=entries)