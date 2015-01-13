from flask import jsonify, render_template, request, flash, redirect, url_for, session, Markup
from forms import *
from urllib import quote
import bleach
from datetime import datetime, timedelta
import random
import calendar
import re
import praw
import requests
from functools import wraps
from markdown import markdown
import cms_functions
from app import app, db, models


# Filter to render markdown in templates
@app.template_filter('markdown')
def render_markdown(markdown_text):
    return Markup(markdown(markdown_text))


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in first.')
            return redirect(url_for('login'))

    return wrap


##############################################################################
# Blog #######################################################################
@app.route('/')
def index():
    # Sorting by ID (descending order)
    posts = models.Post.query.order_by(models.Post.id.desc()).all()
    current_month_posts = []
    last_month_posts = []
    two_months_ago_posts = []

    for post in posts:
        status = cms_functions.get_recent_posts(post)
        if status == 'Current Month':
            current_month_posts.append(post)
        elif status == 'Last Month':
            last_month_posts.append(post)
        elif status == 'Two Months Ago':
            two_months_ago_posts.append(post)

    if 'logged_in' in session:
        link = '/cms'
        text = 'CMS'
    else:
        link = '/login'
        text = 'Login'

    return render_template('/blog/home.html',
                           current_month_posts=current_month_posts,
                           last_month_posts=last_month_posts,
                           two_months_ago_posts=two_months_ago_posts,
                           link=link,
                           text=text)


@app.route('/archive')
def archive():
    posts = models.Post.query.order_by(models.Post.id.desc()).all()
    month_strings = []
    month_year = []
    month_list = []

    for post in posts:
        try:
            date_string = '%s %s' % (str(calendar.month_name[int(post.month)]), str(post.year))
            if date_string not in month_strings:
                month_strings.append(date_string)
                month_year.append([post.month, post.year])
        except TypeError:
            continue

    counter = 0
    numbers = [10, 11, 12]
    for entry in month_strings:
        year = month_year[counter][1]
        month = month_year[counter][0]
        # Pre-pending a 0 to month if needed
        if int(month) in numbers:
            month = '%s' % str(month)
        else:
            month = '0%s' % str(month)
        year_month = '%s%s' % (str(year), month)

        month_list.append([entry, month, year, int(year_month)])
        counter += 1

    # Sorting by third index - year + month
    month_list.sort(key=lambda x: x[3], reverse=True)
    return render_template('/blog/archive.html',
                           title='Archive',
                           months=month_list)


@app.route('/archive/<year>/<month>')
def archive_viewer(year, month):
    posts = models.Post.query.order_by(models.Post.id.desc()).all()
    selected_posts = []
    month_string = calendar.month_name[int(month)]

    for post in posts:
        try:
            if int(post.month) == int(month) and int(post.year) == int(year):
                selected_posts.append(post)
        except TypeError:
            continue

    return render_template('/blog/cms/archive_viewer.html',
                           title='Archive - %s %d' % (month_string, int(year)),
                           selected_posts=selected_posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        verify = cms_functions.password_validate(username, password)

        if not verify[0]:
            print 'Did not verify'
            flash(verify[1])
            return redirect(url_for('login'))
        else:
            session['logged_in'] = True
            return redirect(url_for('cms'))
    else:
        return render_template('/blog/cms/login.html',
                               form=form,
                               title='CMS Login')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/cms', methods=['GET', 'POST'])
@login_required
def cms():
    posts = models.Post.query.order_by(models.Post.id.desc()).all()
    link = '/logout'
    text = 'Logout'
    needs_approval = cms_functions.approval_notification()

    if posts:
        current_month = datetime.today().strftime('%B %Y')
        last_month = (datetime.today() - timedelta(weeks=4)).strftime('%B %Y')
        two_months_ago = (datetime.today() - timedelta(weeks=8)).strftime('%B %Y')
        current_month_posts = []
        last_month_posts = []
        two_months_ago_posts = []
        older_posts = []
        statistics = cms_functions.stats(posts, 0)

        for post in posts:
            if cms_functions.get_recent_posts(post) == 'Current Month':
                current_month_posts.append(post)
            elif cms_functions.get_recent_posts(post) == 'Last Month':
                last_month_posts.append(post)
            elif cms_functions.get_recent_posts(post) == 'Two Months Ago':
                two_months_ago_posts.append(post)
            else:
                older_posts.append(post)

    # Placeholder code to be used in case of a blank DB
    else:
        current_month_posts = ''
        last_month_posts = ''
        two_months_ago_posts = ''
        older_posts = ''
        current_month = ''
        last_month = ''
        two_months_ago = ''
        statistics = ''

    return render_template('/blog/cms/cms.html',
                           icons=cms_functions.dog_icons(),
                           form=DatabaseForm(),
                           current_month_posts=current_month_posts,
                           last_month_posts=last_month_posts,
                           two_months_ago_posts=two_months_ago_posts,
                           older_posts=older_posts,
                           current_month=current_month,
                           last_month=last_month,
                           two_months_ago=two_months_ago,
                           stats=statistics,
                           link=link,
                           text=text,
                           needs_approval=needs_approval,
                           title='CMS')


@app.route('/new-post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = DatabaseForm()
    form.month.data = datetime.today().month
    form.year.data = datetime.today().year
    form.hidden_date.data = datetime.today().strftime('%A %B %d, %Y')
    # Grabbing most recent entry's primary key to determine next CSS class
    latest_id = models.Post.query.all()[-1].id + 1
    form.color.data = cms_functions.get_color(latest_id)
    link = '/cms'
    text = 'CMS'

    return render_template('/blog/cms/new-post.html',
                           form=form,
                           icons=cms_functions.dog_icons(),
                           link=link,
                           text=text,
                           title='New Post')


@app.route('/cms-submit', methods=['GET', 'POST'])
@login_required
def cms_submit():
    form = DatabaseForm()
    if not form.validate_on_submit():
        return render_template('/blog/cms/new-post.html',
                               icons=cms_functions.dog_icons(),
                               form=form)
    else:
        css_class = cms_functions.get_theme(form.color.data)
        title = bleach.clean(form.title.data)
        icon = form.icon.data
        subtitle = bleach.clean(form.subtitle.data)
        content = cms_functions.generate_markdown(form.content.data, True)
        date_string = form.hidden_date.data
        month = form.month.data
        year = form.year.data

        post = models.Post(css_class=css_class,
                           title=title,
                           icon=icon,
                           subtitle=subtitle,
                           date=date_string,
                           month=month,
                           content=content,
                           year=year)

        db.session.add(post)
        db.session.commit()

        flash('Your post titled %s has been added to the database!' % title)
        return redirect(url_for('cms'))


@app.route('/preview')
def preview():
    color = request.args.get('color', 0, type=str)
    title = bleach.clean(request.args.get('title', 0, type=str))
    icon = request.args.get('icon', 0, type=str)
    hidden_date = bleach.clean(request.args.get('hidden_date', 0, type=str))
    subtitle = bleach.clean(request.args.get('subtitle', 0, type=str))
    content = cms_functions.generate_markdown(request.args.get('content', 0, type=str), False)
    div_class = cms_functions.get_theme(color)
    date = hidden_date
    author = bleach.clean(request.args.get('author', 0, type=str))
    if author:
        author = author
    else:
        author = 'Tyler Kershner'

    html = '''
        <div class="dynamic %s" style="padding-top: 15px;">
            <div>
                <img src="%s"><span class="ba">%s</span>
                    <h2>%s</h2>
                    <h4 class="bd">%s</h4>
                    <span class="post-date">%s</span>
                    <hr style="width: 90%%">
                    %s
            </div>
            <script>
                initSlick();
            </script>
        </div>
    ''' % (div_class, icon, author, title, subtitle, date, content)

    data = {
        'html': html,
        'content': content
    }

    return jsonify(data)


@app.route('/edit-post/<unique_id>', methods=['GET', 'POST'])
@login_required
def cms_edit(unique_id):
    form = DatabaseForm()
    post = models.Post.query.get(unique_id)
    link = '/cms'
    text = 'CMS'

    form.color.data = post.css_class
    form.icon.data = post.icon
    form.title.data = post.title
    form.subtitle.data = post.subtitle
    form.content.data = cms_functions.generate_markdown(post.content, True)
    form.hidden_date.data = post.date
    form.month.data = post.month
    form.year.data = post.year

    return render_template('/blog/cms/edit-post.html',
                           post=post,
                           form=form,
                           icons=cms_functions.dog_icons(),
                           link=link,
                           text=text,
                           title='Edit Post')


@app.route('/update-post/<unique_id>', methods=['GET', 'POST'])
@login_required
def cms_update(unique_id):
    form = DatabaseForm()
    post = models.Post.query.get(unique_id)

    if form.validate_on_submit():
        post.css_class = cms_functions.get_theme(form.color.data)
        post.title = bleach.clean(form.title.data)
        post.icon = form.icon.data
        post.subtitle = bleach.clean(form.subtitle.data)
        post.content = cms_functions.generate_markdown(form.content.data, True)
        post.month = form.month.data
        post.year = form.year.data
        db.session.commit()

        flash('The post titled %s has been updated!' % post.title)
        return redirect(url_for('cms'))

    form.color.data = post.css_class
    form.title.data = post.title
    form.icon.data = post.icon
    form.subtitle.data = post.subtitle
    form.content.data = post.content

    return render_template('/blog/cms/edit-post.html',
                           form=form,
                           post=post,
                           icons=cms_functions.dog_icons())


@app.route('/delete-post/<unique_id>')
@login_required
def cms_delete(unique_id):
    post = models.Post.query.get(unique_id)

    db.session.delete(post)
    db.session.commit()

    flash("Successfully deleted post titled %s." % post.title)
    return redirect(url_for('cms'))


##############################################################################
# Public CMS #################################################################
@app.route('/public')
def public():
    posts = models.PublicPost.query.order_by(models.PublicPost.pub_id.desc()).all()
    approved_posts = []
    for post in posts:
        if post.approved:
            approved_posts.append(post)

    return render_template('/blog/public-cms/public.html',
                           posts=approved_posts)


@app.route('/public-cms')
def public_cms():
    posts = models.PublicPost.query.order_by(models.PublicPost.pub_id.desc()).all()
    approved_posts = []
    for post in posts:
        if post.approved:
            approved_posts.append(post)
    statistics = cms_functions.stats(approved_posts, 1)

    return render_template('/blog/public-cms/public-cms.html',
                           posts=approved_posts,
                           stats=statistics,
                           title='Public CMS')


@app.route('/public-new-post')
def public_new_post():
    form = PublicDatabaseForm()
    form.month.data = datetime.today().month
    form.year.data = datetime.today().year
    form.hidden_date.data = datetime.today().strftime('%A %B %d, %Y')
    # Grabbing most recent entry's primary key to determine next CSS class
    latest_id = models.PublicPost.query.all()[-1].pub_id + 1
    form.color.data = cms_functions.get_color(latest_id)

    return render_template('/blog/public-cms/public-new-post.html',
                           form=form,
                           icons=cms_functions.dog_icons(),
                           title='New Public Post')


@app.route('/public-cms-submit', methods=['GET', 'POST'])
def public_cms_submit():
    form = PublicDatabaseForm()
    if not form.validate_on_submit():
        return render_template('/blog/public-cms/public-new-post.html',
                               icons=cms_functions.dog_icons(),
                               form=form)
    else:
        css_class = cms_functions.get_theme(form.color.data)
        title = bleach.clean(form.title.data)
        author = bleach.clean(form.author.data)
        icon = form.icon.data
        subtitle = bleach.clean(form.subtitle.data)
        content = cms_functions.generate_markdown(form.content.data, True)
        date_string = form.hidden_date.data
        month = form.month.data
        year = form.year.data

        post = models.PublicPost(approved=0,
                                 pub_css_class=css_class,
                                 pub_title=title,
                                 author=author,
                                 pub_icon=icon,
                                 pub_subtitle=subtitle,
                                 pub_date=date_string,
                                 pub_month=month,
                                 pub_content=content,
                                 pub_year=year)

        db.session.add(post)
        db.session.commit()

        flash('Your post titled %s has been submitted for approval!' % title)
        if 'logged_in' in session:
            return redirect(url_for('need_approval'))
        else:
            return redirect(url_for('public_cms'))


@app.route('/need-approval')
@login_required
def need_approval():
    posts = models.PublicPost.query.order_by(models.PublicPost.pub_id.desc()).all()
    to_be_approved = []
    approved = []
    for post in posts:
        if not post.approved:
            to_be_approved.append(post)
        else:
            approved.append(post)

    return render_template('/blog/public-cms/posts-to-approve.html',
                           posts=to_be_approved,
                           approved=approved,
                           title='Posts to Be Approved')


@app.route('/public-edit-post/<unique_id>', methods=['GET', 'POST'])
@login_required
def public_cms_edit(unique_id):
    form = PublicDatabaseForm()
    post = models.PublicPost.query.get(unique_id)
    approved = post.approved

    form.color.data = post.pub_css_class
    form.icon.data = post.pub_icon
    form.title.data = post.pub_title
    form.author.data = post.author
    form.subtitle.data = post.pub_subtitle
    form.content.data = cms_functions.generate_markdown(post.pub_content, True)
    form.hidden_date.data = post.pub_date
    form.month.data = post.pub_month
    form.year.data = post.pub_year

    return render_template('/blog/public-cms/public-edit-post.html',
                           post=post,
                           approved=approved,
                           form=form,
                           icons=cms_functions.dog_icons(),
                           title='Edit Public Post')


@app.route('/public-update-post/<unique_id>', methods=['GET', 'POST'])
@login_required
def public_cms_update(unique_id):
    form = PublicDatabaseForm()
    post = models.PublicPost.query.get(unique_id)

    if form.validate_on_submit():
        post.pub_css_class = cms_functions.get_theme(form.color.data)
        post.pub_title = bleach.clean(form.title.data)
        post.author = bleach.clean(form.author.data)
        post.pub_icon = form.icon.data
        post.pub_subtitle = bleach.clean(form.subtitle.data)
        post.pub_content = cms_functions.generate_markdown(form.content.data, True)
        post.pub_month = form.month.data
        post.pub_year = form.year.data
        db.session.commit()

        flash('The post titled %s has been updated!' % post.pub_title)
        if 'logged_in' in session:
            return redirect(url_for('need_approval'))
        else:
            return redirect(url_for('public_cms'))

    form.color.data = post.pub_css_class
    form.title.data = post.pub_title
    form.author.data = post.author
    form.icon.data = post.pub_icon
    form.subtitle.data = post.pub_subtitle
    form.content.data = post.pub_content

    return render_template('/blog/public-cms/public-edit-post.html',
                           form=form,
                           post=post,
                           icons=cms_functions.dog_icons())


@app.route('/approve-public-post/<unique_id>')
@login_required
def approve_public_post(unique_id):
    post = models.PublicPost.query.get(unique_id)
    post.approved = 1

    db.session.commit()
    flash('The post titled %s has been approved!' % post.pub_title)
    return redirect(url_for('need_approval'))


@app.route('/public-delete-post/<unique_id>')
@login_required
def public_cms_delete(unique_id):
    post = models.PublicPost.query.get(unique_id)

    db.session.delete(post)
    db.session.commit()

    flash("Successfully deleted post titled %s." % post.pub_title)
    if 'logged_in' in session:
            return redirect(url_for('need_approval'))
    else:
        return redirect(url_for('public_cms'))


@app.route('/about')
def about():
    return render_template('/blog/about.html',
                           title='About Me')


@app.route('/projects')
def projects():
    return render_template('/blog/projects.html',
                           title='Projects')


@app.route('/pta')
def project1():
    return render_template('/blog/projects/project01.html',
                           title='Python Text Adventure')


@app.route('/cstools-project')
def project2():
    return render_template('/blog/projects/project02.html',
                           title='CSTools')


@app.route('/gif_display')
def gif_display():
    return render_template('/blog/projects/project03.html',
                           title='Raspberry Pi GIF Display')


@app.route('/gif-party')
def gif_party_project():
    return render_template('/blog/projects/project04.html',
                           title='Gif Party!')


@app.route('/reddit-scraper')
def reddit_scraper_project():
    return render_template('/blog/projects/project05.html',
                           title='Reddit Scraper')


@app.route('/ycs-campaign')
def ycs_campaign():
    return render_template('/blog/projects/project06.html',
                           title='YCS Re-election Website')


@app.route('/steamtime-project')
def steamtime_project():
    return render_template('/blog/projects/project07.html',
                           title='SteamTime')


@app.route('/cms-project')
def cms_project():
    return render_template('/blog/projects/project08.html',
                           title='CMS')


@app.route('/cstoolswriteup-part1')
def project2writeup1():
    return render_template('/blog/writeups/project02-part1.html',
                           title='CSTools Writeup')


@app.route('/cstoolswriteup-part2')
def project2writeup2():
    return render_template('/blog/writeups/project02-part2.html',
                           title='CSTools Writeup')


@app.route('/piproject1')
def piproject1():
    return render_template('/blog/writeups/project03-part1.html',
                           title='GIF Picture Frame Writeup Part 1')


@app.route('/piproject2')
def piproject2():
    return render_template('/blog/writeups/project03-part2.html',
                           title='GIF Picture Frame Writeup Part 2')


@app.route('/warning')
def warning():
    return render_template('/blog/warning.html',
                           title='Warning')


##############################################################################
# Pi Display
##############################################################################
@app.route('/pi_display')
def pi_display():
    return render_template('/pi_display/pi_display.html')


@app.route('/pi_display_json')
def pi_display_json():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

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
@app.route('/pi_display_config', methods=['GET', 'POST'])
def pi_display_config():
    form = SlideshowDelay()
    path = '/home/tylerkershner/app/templates/pi_display/logs'

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
# Gif Party
@app.route('/gif_party')
def gif_party_welcome():
    path = '/home/tylerkershner/app/templates/gif_party'

    filename = 'welcome_urls.txt'

    with open('%s/%s' % (path, filename), 'r') as urls_file:
        urls_list = list(urls_file)

    image_url = random.choice(urls_list)
    image_url = image_url[:image_url.find('\n')]

    return render_template('/gif_party/welcome.html',
                           image_url=image_url)


@app.route('/gif_party_about')
def gif_party_about():
    path = '/home/tylerkershner/app/templates/gif_party'

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


###################################################################################
#  CS Tools Apps ##################################################################
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
                date_object = datetime.date(datetime.strptime(form_date, '%m/%d/%y'))
                form_expiry_date = date_object + timedelta(days=60)
                form_expiry_date_nice = "%s %s" % (str(form_expiry_date.strftime("%B")), str(form_expiry_date.day))
                days_expired = datetime.today().date() - form_expiry_date
                if form_expiry_date > datetime.today().date():
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
            signoff = "\n\nI apologize for the inconvenience.  Let me know if you have any questions." \
                      "\n\nHave a great day,\n\n"
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


@app.route('/cstools/backorder-report', methods=['GET', 'POST'])
def backorder_report():
    form = BackorderReport()
    get_class_well.get_color()
    color = get_class_well.color

    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("/cstools/backorder-report.html",
                                   title="Backorder Report Template",
                                   form=form,
                                   color=color)
        else:
            name = form.name.data
            email = form.email.data
            subject = "Cayman Chemical Backorder Report"
            body = "Hello %s,\n\nAttached find an updated copy of your institution's backorder report.\n\n" \
                   "Please let me know if you have any questions.\n\n" % name
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("/cstools/backorder-report.html",
                                   title="Backorder Report Template",
                                   link=link,
                                   form=form,
                                   color=color)
    elif request.method == 'GET':
        return render_template("/cstools/backorder-report.html",
                               title="Backorder Report Template",
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
                                   title="Account Application Template",
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
                                   title="Account Application Template",
                                   link=link,
                                   form=form,
                                   color=color)
    elif request.method == 'GET':
        return render_template("/cstools/application.html",
                               title="Account Application Template",
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

            if form.net30.data:
                body = "Hello %s,\n\nThank you for your interest in Cayman Chemical!  A net 30 term account has been " \
                       "established for you.  We accept Purchase Orders, Visa, MasterCard, Discover, American Express, checks, and bank " \
                       "transfers.\n\nTo place an order, please contact customer service at one of the following:\n\nPhone:\t\t 800-364-9897" \
                       "\nFax:\t\t    734-971-3640\nEmail:\t\t  orders@caymanchem.com\nWebsite:\thttp://www.caymanchem.com" \
                       "\n\nWhen placing an order please reference customer account number %s.\n\nWe look forward to doing " \
                       "business with you!\n\n" % (name, acct_number)
            else:
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


def login_required_cstools(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'cstoolslogged_in' in session:
            return test(*args, **kwargs)
        else:
            error = 'You need to log in first.'
            return render_template('/cstools/login.html',
                                   title='Login',
                                   error=error)
    return wrap


@app.route('/cstools/login', methods=['GET', 'POST'])
def cstools_login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'cs' or request.form['password'] != 'cayman':
            error = 'Invalid credentials, please try again.'
        else:
            session['cstoolslogged_in'] = True
            return redirect(url_for('forms_without_orders'))
    return render_template('/cstools/login.html',
                           title='Login',
                           error=error)


@app.route('/cstools/logout')
def cstools_logout():
    if 'logged_in_cstools' in session:
        session.pop('cstoolslogged_in', None)
        return redirect(url_for('cstools'))
    else:
        return redirect(url_for('cstools'))


@app.route('/cstools/forms-without-orders', methods=['GET', 'POST'])
@login_required_cstools
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
            now = datetime.utcnow()
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
@login_required_cstools
def new_entry():
    form = DeaForms()
    entries = models.Entry.query.all()
    return render_template("/cstools/forms_without_orders.html",
                           title="DEA Forms Without Orders",
                           form=form,
                           entries=entries,
                           new_entry=True)


@app.route('/cstools/forms-without-orders/edit-entry/<entry_id>')
@login_required_cstools
def edit_entry(entry_id):
    entry = models.Entry.query.get(entry_id)

    return render_template("/cstools/forms_without_orders_edit.html",
                           title="DEA Forms Without Orders - Edit Entry",
                           entry=entry)


@app.route('/cstools/forms-without-orders/update-entry/<entry_id>', methods=['GET', 'POST'])
@login_required_cstools
def update_entry(entry_id):
    form = DeaForms()
    entry = models.Entry.query.get(entry_id)
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


@app.route('/cstools/forms-without-orders/delete-entry/<entry_id>')
@login_required_cstools
def delete_entry(entry_id):
    entry = models.Entry.query.get(entry_id)

    db.session.delete(entry)
    db.session.commit()

    entries = models.Entry.query.all()

    message = "Successfully deleted entry for %s." % entry.institution

    return render_template("/cstools/forms_without_orders.html",
                           title="DEA Forms Without Orders",
                           message=message,
                           entries=entries)


##############################################################################
# Reddit Image Scraper
@app.route('/scrape', methods=['GET', 'POST'])
def scrape_home():
    form = RedditImageScraper()
    suggestions = ['pugs', 'earthporn', 'kittens', 'gaming', 'pics', 'awww', 'funny', 'adviceanimals', 'gifs',
                   'wallpapers', 'foodporn', 'historyporn', 'photoshopbattles', 'mildlyinteresting', 'woahdude',
                   'oldschoolcool', 'perfecttiming', 'abandonedporn', 'roomporn']
    picks = []
    for number in range(0, 3):
        pick = random.choice(suggestions)
        if pick in picks:
            continue
        else:
            picks.append(pick)

    return render_template('/reddit_scraper/home.html',
                           form=form,
                           picks=picks)


@app.route('/scrape-reddit', methods=['GET', 'POST'])
def scrape():
    form = RedditImageScraper()
    suggestions = ['pugs', 'earthporn', 'kittens', 'gaming', 'pics', 'awww', 'funny', 'adviceanimals', 'gifs',
                   'wallpapers', 'foodporn', 'historyporn', 'photoshopbattles', 'mildlyinteresting', 'woahdude',
                   'oldschoolcool', 'perfecttiming', 'abandonedporn', 'roomporn']
    picks = []
    for number in range(0, 3):
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
                            indirect_urls.append([submission.url, submission.short_link, submission.title])
                    elif find_string('/gallery/')(submission.url):
                        print 'Submission (%s) is an Imgur album link' % submission.url
                        indirect_urls.append([submission.url, submission.short_link, submission.title])
                    elif find_string('http://imgur.com/')(submission.url):
                        if find_string('/a/')(submission.url):
                            print 'Submission (%s) is an Imgur album link' % submission.url
                            indirect_urls.append([submission.url, submission.short_link, submission.title])
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
                        indirect_urls.append([submission.url, submission.short_link, submission.title])
                    elif find_string('youtube')(submission.url):
                        print 'Youtube link, adding to indirect_urls...'
                        indirect_urls.append([submission.url, submission.short_link, submission.title])
                    elif find_string('twitter')(submission.url):
                        print 'Twitter link, adding to indirect_urls...'
                        indirect_urls.append([submission.url, submission.short_link, submission.title])
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
                        indirect_urls.append([submission.url, submission.short_link, submission.title])
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


##############################################################################
# Campaign Demo Site
@app.route('/campaign')
def campaign():
    return render_template('/campaign/home.html')


@app.route('/slogan')
def slogan():
    slogans = ['student success', 'fiscal stability', 'student achievement', 'community satisfaction']
    variable = random.choice(slogans)

    data = {
        "variable": variable
    }

    return jsonify(data)


@app.route('/article')
def article():
    articles = [
        ['"Ypsilanti Community Schools graduates inaugural senior class."',
         'http://www.mlive.com/news/ann-arbor/index.ssf/2014/06/ypsilanti_community_schools_gr.html',
         '- Amy Biolchini', 'MLive | 6/03/2014', '61'],
        ['"Ypsilanti schools to pursue college scholarship program similar to Kalamazoo Promise."',
         'http://www.annarbor.com/news/ypsilanti/ypsilanti-community-schools-to-pursue-college-scholarship-program-'
         'similar-to-kalamazoo-promise/',
         '- Danielle Arndt', 'The Ann Arbor News | 7/25/2013', '85'],
        ['"Ypsilanti New Tech High School sends off its inaugural graduating class."',
         'http://www.heritage.com/articles/2014/05/23/ypsilanti_courier/news/doc537f84b324c9c781733383.txt',
         '- Krystal Elliott', 'The Ypsilanti Courier | 5/23/2014', '74'],
        ['"State Superintendent Mike Flanagan says school district deficits \'reducing\' overall."',
         'http://www.mlive.com/lansing-news/index.ssf/2014/06/flanagan_deficit_districts.html',
         '- Brian Smith', 'MLive | 6/08/2014', '86'],
        ['"Ypsilanti schools authorizes restructuring $18.8M debt to no longer be a deficit district."',
         'http://www.annarbor.com/news/ypsilanti/ypsilanti-schools-authorizes-restructuring-its-188m-debt-to-no-'
         'longer-be-a-deficit-district/',
         '- Danielle Arndt', 'The Ann Arbor News | 6/26/2013', '92'],
    ]

    article_snip = random.choice(articles)

    data = {
        "title": article_snip[0],
        "link": article_snip[1],
        "author": article_snip[2],
        "journal": article_snip[3],
        "length": article_snip[4]
    }

    return jsonify(data)


@app.route('/article2')
def article2():
    articles = [
        ['"Year-round school? Ypsilanti schools considering expanding use of balanced calendar."',
         'http://www.mlive.com/news/ann-arbor/index.ssf/2014/08/ypsilanti_schools_to_consider.html',
         '- Amy Biolchini', 'MLive | 8/09/2014', '86'],
        ['"Holmes Elementary School starts off strong as first to pilot balanced calendar in Ypsilanti Community '
         'Schools."',
         'http://www.heritage.com/articles/2014/08/21/ypsilanti_courier/news/doc53f61a1be160f522813720.txt',
         '- Krystal Elliott', 'The Ypsilanti Courier | 8/21/2014', '112'],
        ['"City officials propose stationing police officer at Ypsilanti Community Middle School."',
         'http://www.heritage.com/articles/2014/06/17/ypsilanti_courier/news/doc53a054c6786f5399518913.txt',
         '- Krystal Elliott', 'The Ypsilanti Courier | 6/17/2014', '88'],
        ['"Ypsilanti teachers, district \'satisfied\' overall with union contract despite some concerns over '
         'salaries."',
         'http://www.heritage.com/articles/2014/09/17/ypsilanti_courier/news/doc541221141ab45551957933.txt',
         '- Krystal Elliott', 'The Ypsilanti Courier | 9/17/2014', '106'],
        ['"Ypsilanti Community Schools Adopts Elementary Reconfiguration Plan."',
         'http://wemu.org/post/ypsilanti-community-schools-adopts-elementary-reconfiguration-plan',
         '- Bob Eccles', 'WEMU 89.1 | 4/22/2014', '68']
    ]

    article_snip = random.choice(articles)

    data = {
        "title": article_snip[0],
        "link": article_snip[1],
        "author": article_snip[2],
        "journal": article_snip[3],
        "length": article_snip[4]
    }

    return jsonify(data)


@app.route('/candidates')
def candidates():
    return render_template('/campaign/candidates.html')


@app.route('/contact')
def contact():
    return render_template('/campaign/contact.html')


@app.route('/press')
def press():
    return render_template('/campaign/press.html')
