from flask import jsonify, render_template, request, flash, redirect, url_for, session, Markup
from forms import *
from urllib import quote
from functools import wraps
from markdown import markdown
from datetime import datetime, timedelta
from modules import music_files, campaign_logic, reddit_scraper, cstools_logic
import bleach
import random
import calendar
import json
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
    else:
        link = ''

    return render_template('/blog/home.html',
                           current_month_posts=current_month_posts,
                           last_month_posts=last_month_posts,
                           two_months_ago_posts=two_months_ago_posts,
                           link=link)


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


@app.route('/screenbloom-project')
def screenbloom_project():
    return render_template('/blog/projects/project09.html',
                           title='ScreenBloom')


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
# Pi Display #################################################################
@app.route('/pi_display')
def pi_display():
    return render_template('/pi_display/pi_display.html')


@app.route('/pi_display_json')
def pi_display_json():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    # Open config file, grab variables from it
    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config = list(config_file)

    category = config[0][:config[0].find('\n')]
    delay = config[2][:config[2].find('\n')]
    filename = category + '_urls.txt'
    toplay_filename = category + '_urls_to_play.txt'

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

    # Choose random URL from to_play list, writing to config file
    gif_url = random.choice(urls_toplay_list)
    with open('%s/pi_display_config.txt' % path, 'w+') as config_file:
        config_file.write(config[0])
        config_file.write('%s' % gif_url)
        config_file.write(config[2])

    # Open/close to_play_urls.txt (taking advantage of side effect to erase contents)
    open('%s/%s' % (path, toplay_filename), 'w').close()

    # Rewrite to_play.txt without current gif URL (won't play twice)
    with open('%s/%s' % (path, toplay_filename), 'a+') as urls_to_play:
        for entry in urls_toplay_list:
            if entry == gif_url:
                print gif_url
                print entry
                continue
            else:
                urls_to_play.write(entry)

    # Add currently playing GIF to last_played file
    with open('%s/last_played.txt' % path, 'a+') as f:
        f.write(gif_url)

    delay = str(delay) + '000'

    data = {
        "URL": gif_url,
        "delay": delay
    }

    return jsonify(data)


##############################################################################
# Pi Display Config ##########################################################
@app.route('/pi_display_config')
def pi_display_config():
    session['prev'] = -1
    session['prev_stop'] = -2
    session['prev_start'] = 3
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

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config = list(config_file)

    main_urls_count = len(main_urls_list)
    animals_urls_count = len(animals_urls_list)
    gaming_urls_count = len(gaming_urls_list)
    strange_urls_count = len(strange_urls_list)
    educational_urls_count = len(educational_urls_list)
    category = config[0][:config[0].find('\n')]
    current_gif = config[1][:config[1].find('\n')]
    delay = config[2][:config[2].find('\n')]

    return render_template('/pi_display/pi_display_config.html',
                           current_gif=current_gif,
                           main_urls_count=main_urls_count,
                           animals_urls_count=animals_urls_count,
                           gaming_urls_count=gaming_urls_count,
                           strange_urls_count=strange_urls_count,
                           educational_urls_count=educational_urls_count,
                           category=category.title(),
                           delay=delay)


@app.route('/pi-display-config-update')
def pi_display_config_update():
    session['prev'] = -1
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config = list(config_file)
        current_gif = config[1][:config[1].find('\n')]
        message = 'Currently Playing GIF'
        data = {
            'current_gif': current_gif,
            'message': message
        }

        return jsonify(data)


@app.route('/pi-display-config-prev')
def pi_display_config_prev():
    session['prev'] -= 1
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/last_played.txt' % path, 'a+') as f:
        last_played_list = list(f)
        gifs = last_played_list[int('%d' % session['prev'])][:last_played_list[int('%d' % session['prev'])].find('\n')]
        message = 'Previous GIF'
        data = {
            'last_played': gifs,
            'message': message
        }

        return jsonify(data)


@app.route('/pi-display-config-auto')
def pi_display_config_auto():
    path = '/home/tylerkershner/app/templates/pi_display/logs'

    with open('%s/pi_display_config.txt' % path, 'r') as config_file:
        config = list(config_file)
        delay = config[2][:config[2].find('\n')]
        data = {
            'delay': delay + '000'
        }

        return jsonify(data)


@app.route('/pi-display-config-categories')
def pi_display_config_all():
    path = '/home/tylerkershner/app/templates/pi_display/logs'
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

        return jsonify(data)


@app.route('/pi-display-config-delay')
def pi_display_config_delay():
    path = '/home/tylerkershner/app/templates/pi_display/logs'
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

        return jsonify(data)


@app.route('/previous-gifs')
def previous_gifs():
    path = '/home/tylerkershner/app/templates/pi_display/logs'
    session['prev_stop'] -= 5
    session['prev_start'] -= 5

    with open('%s/last_played.txt' % path, 'a+') as f:
        last_played_list = list(f)
        prev_5 = ''.join(last_played_list[session['prev_start']:session['prev_stop']:-1]).split()
        data = {
            'prev_5': prev_5,
            'id': session['prev_start']
        }

        return jsonify(data)


@app.route('/last-played/<number>')
def last_played(number):
    path = '/home/tylerkershner/app/templates/pi_display/logs'
    number = 0 - int(number)

    with open('%s/last_played.txt' % path, 'r') as f:
        last_played_list = list(f)
        gifs = ''.join(last_played_list[-2:number - 2:-1]).split()
        data = {
            'gifs': gifs
        }

        return jsonify(data)


@app.route('/clear-session')
def clear_session():
    session['prev_stop'] = -2
    session['prev_start'] = 3
    message = 'Session cleared'
    data = {
        'message': message
    }

    return jsonify(data)


@app.route('/email-gifs')
def email_gifs():
    email = request.args.get('email', 0, type=str)
    gifs = json.loads(request.args.get('images', 0, type=str))
    subject = 'Your Saved GIFs'
    gifs = '\n'.join(gifs)
    body = '%s' % gifs
    link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
    data = {
        'link': link
    }

    return jsonify(data)


##############################################################################
# Gif Party ##################################################################
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
        'URLs': urls,
        'number': number,
        'delay': delay,
        'category': category
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
        'number': session['number']
    }

    return jsonify(data)


@app.route('/gif_party_json_10')
def gif_party_json_10():
    session['number'] = 10

    data = {
        'number': session['number']
    }

    return jsonify(data)


@app.route('/gif_party_json_20')
def gif_party_json_20():
    session['number'] = 20

    data = {
        'number': session['number']
    }

    return jsonify(data)


@app.route('/gif_party_json_delay', methods=['GET', 'POST'])
def gif_party_json_delay():
    delay = request.json
    delay = str(delay) + '000'
    session['delay'] = delay

    data = {
        'delay': session['delay']
    }

    return jsonify(data)


###################################################################################
#  CS Tools Apps ##################################################################
@app.route('/cstools')
def cstools():
    return render_template('/cstools/index.html',
                           title='Home')


@app.route('/cstools/datechecker', methods=['GET', 'POST'])
def datechecker():
    form = DateCheckerForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('/cstools/datechecker.html',
                                   title='222 Form Date Checker',
                                   form=form)
        else:
            try:
                form_date = form.form_date.data
                return render_template('/cstools/datechecker.html',
                                       title="222 Form Date Checker",
                                       form=form,
                                       message=cstools_logic.datechecker_logic(form_date))
            except ValueError:
                message = 'Enter the form\'s issue date in the format MM/DD/YY.'
                return render_template('/cstools/datechecker.html',
                                       title='222 Form Date Checker',
                                       form=form,
                                       message=message)
    elif request.method == 'GET':
        return render_template('/cstools/datechecker.html',
                               title='222 Form Date Checker',
                               form=form)


@app.route('/cstools/backorder', methods=['GET', 'POST'])
def backorder():
    form = BackorderForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('/cstools/backorder.html',
                                   title='Backorder Template',
                                   form=form,
                                   color=cstools_logic.get_css_color())
        else:
            email = form.email.data
            po = form.po.data
            name = form.name.data
            item_no = form.item_number.data
            lead_time = form.lead_time.data
            link = cstools_logic.backorder_logic(po, email, name, item_no, lead_time)
            return render_template('/cstools/backorder.html',
                                   title='Backorder Template',
                                   link=link,
                                   form=form,
                                   color=cstools_logic.get_css_color())

    elif request.method == 'GET':
        return render_template('/cstools/backorder.html',
                               title='Backorder Template',
                               form=form,
                               color=cstools_logic.get_css_color())


@app.route('/cstools/backorder-report', methods=['GET', 'POST'])
def backorder_report():
    form = BackorderReport()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('/cstools/backorder-report.html',
                                   title='Backorder Report Template',
                                   form=form,
                                   color=cstools_logic.get_css_color())
        else:
            name = form.name.data
            email = form.email.data
            link = cstools_logic.backorder_report_logic(name, email)
            return render_template('/cstools/backorder-report.html',
                                   title='Backorder Report Template',
                                   link=link,
                                   form=form,
                                   color=cstools_logic.get_css_color())
    elif request.method == 'GET':
        return render_template('/cstools/backorder-report.html',
                               title='Backorder Report Template',
                               form=form,
                               color=cstools_logic.get_css_color())


@app.route('/cstools/application', methods=['GET', 'POST'])
def application():
    form = ApplicationForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('/cstools/application.html',
                                   title='Account Application Template',
                                   form=form,
                                   color=cstools_logic.get_css_color())
        else:
            name = form.name.data
            email = form.email.data
            link = cstools_logic.application_logic(name, email)
            return render_template('/cstools/application.html',
                                   title='Account Application Template',
                                   link=link,
                                   form=form,
                                   color=cstools_logic.get_css_color())
    elif request.method == 'GET':
        return render_template('/cstools/application.html',
                               title='Account Application Template',
                               form=form,
                               color=cstools_logic.get_css_color())


@app.route('/cstools/dea', methods=['GET', 'POST'])
def dea():
    form = DeaForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('/cstools/dea.html',
                                   title='DEA Protocol Template',
                                   form=form,
                                   color=cstools_logic.get_css_color())
        else:
            name = form.name.data
            email = form.email.data
            items = form.dea_items.data
            link = cstools_logic.dea_logic(name, email, items)
            return render_template('/cstools/dea.html',
                                   title='DEA Protocol Template',
                                   link=link,
                                   form=form,
                                   color=cstools_logic.get_css_color())
    elif request.method == 'GET':
        return render_template('/cstools/dea.html',
                               title='DEA Protocol Template',
                               form=form,
                               color=cstools_logic.get_css_color())


@app.route('/cstools/newaccount', methods=['GET', 'POST'])
def newaccount():
    form = NewAccountForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('/cstools/newaccount.html',
                                   title='New Account Template',
                                   form=form,
                                   color=cstools_logic.get_css_color())
        else:
            name = form.name.data
            acct_number = form.acct.data
            email = form.email.data
            net30 = form.net30.data
            link = cstools_logic.newaccount_logic(name, acct_number, email, net30)
            return render_template('/cstools/newaccount.html',
                                   title='New Account Template',
                                   link=link,
                                   form=form,
                                   color=cstools_logic.get_css_color())
    elif request.method == 'GET':
        return render_template('/cstools/newaccount.html',
                               title='New Account Template',
                               form=form,
                               color=cstools_logic.get_css_color())


@app.route('/cstools/shadyblurb', methods=['GET', 'POST'])
def shadyblurb():
    form = ShadyForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('/cstools/shadyblurb.html',
                                   title='Shady Customer Blurb',
                                   form=form,
                                   color=cstools_logic.get_css_color())
        else:
            email = form.email.data
            order_no = form.order_no.data
            link = cstools_logic.shadyblurb_logic(email, order_no)
            return render_template('/cstools/shadyblurb.html',
                                   title='Shady Customer Blurb',
                                   link=link,
                                   form=form,
                                   color=cstools_logic.get_css_color())
    elif request.method == 'GET':
        return render_template('/cstools/shadyblurb.html',
                               title='Shady Customer Blurb',
                               form=form,
                               color=cstools_logic.get_css_color())


@app.route('/cstools/pricediscrepancy', methods=['GET', 'POST'])
def price_discrepancy():
    form = DiscrepancyForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('/cstools/pricediscrepancy.html',
                                   title='Price Discrepancy Template',
                                   form=form,
                                   color=cstools_logic.get_css_color())
        else:
            email = form.email.data
            po = form.po.data
            name = form.name.data
            item_no = form.item_number.data
            given_price = form.given_price.data
            actual_price = form.actual_price.data
            link = cstools_logic.price_discrepancy_logic(email, po, name, item_no, given_price, actual_price)
            return render_template('/cstools/pricediscrepancy.html',
                                   title='Price Discrepancy Template',
                                   link=link,
                                   form=form,
                                   color=cstools_logic.get_css_color())

    elif request.method == 'GET':
        return render_template('/cstools/pricediscrepancy.html',
                               title='Price Discrepancy Template',
                               form=form,
                               color=cstools_logic.get_css_color())


@app.route('/cstools/stillneed', methods=['GET', 'POST'])
def still_need():
    form = StillNeed()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('/cstools/stillneed.html',
                                   title='Still Need Item? Template',
                                   form=form,
                                   color=cstools_logic.get_css_color())
        else:
            name = form.name.data
            email = form.email.data
            item = form.item_number.data
            order_no = form.order_no.data
            link = cstools_logic.stillneed_logic(name, email, item, order_no)
            return render_template('/cstools/stillneed.html',
                                   title='Still Need Item? Template',
                                   link=link,
                                   form=form,
                                   color=cstools_logic.get_css_color())
    elif request.method == 'GET':
        return render_template('/cstools/stillneed.html',
                               title='Still Need Item? Template',
                               form=form,
                               color=cstools_logic.get_css_color())


@app.route('/cstools/licenseneeded', methods=['GET', 'POST'])
def license_needed():
    form = LicenseNeeded()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('/cstools/licenseneeded.html',
                                   title='DEA License Needed Template',
                                   form=form,
                                   color=cstools_logic.get_css_color())
        else:
            name = form.name.data
            email = form.email.data
            order_no = form.order_no.data
            link = cstools_logic.license_needed_logic(name, email, order_no)
            return render_template('/cstools/licenseneeded.html',
                                   title='DEA License Needed Template',
                                   link=link,
                                   form=form,
                                   color=cstools_logic.get_css_color())
    elif request.method == 'GET':
        return render_template('/cstools/licenseneeded.html',
                               title='DEA License Needed Template',
                               form=form,
                               color=cstools_logic.get_css_color())


@app.route('/cstools/deaverify', methods=['GET', 'POST'])
def dea_verify():
    form = DeaVerify()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('/cstools/deaverify.html',
                                   title='DEA Documents Verification Template',
                                   form=form,
                                   color=cstools_logic.get_css_color())
        else:
            order_no = form.order_no.data
            institution = form.institution.data
            link = cstools_logic.dea_verify_logic(order_no, institution)
            return render_template('/cstools/deaverify.html',
                                   title='DEA Documents Verification Template',
                                   link=link,
                                   form=form,
                                   color=cstools_logic.get_css_color())
    elif request.method == 'GET':
        return render_template('/cstools/deaverify.html',
                               title='DEA Documents Verification Template',
                               form=form,
                               color=cstools_logic.get_css_color())


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
            return render_template('/cstools/forms_without_orders.html',
                                   title='DEA Forms Without Orders',
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
            d = cstools_logic.add_e(institution, name, email, item_numbers, notes, csr_name)
            return render_template('/cstools/forms_without_orders.html',
                                   title='DEA Forms Without Orders',
                                   entries=d['entries'],
                                   message=d['message'])
    elif request.method == 'GET':
        entries = models.Entry.query.all()
        return render_template('/cstools/forms_without_orders.html',
                               title='DEA Forms Without Orders',
                               entries=entries)


@app.route('/cstools/forms-without-orders/new-entry')
@login_required_cstools
def new_entry():
    form = DeaForms()
    entries = models.Entry.query.all()
    return render_template('/cstools/forms_without_orders.html',
                           title='DEA Forms Without Orders',
                           form=form,
                           entries=entries,
                           new_entry=True)


@app.route('/cstools/forms-without-orders/edit-entry/<entry_id>')
@login_required_cstools
def edit_entry(entry_id):
    entry = models.Entry.query.get(entry_id)
    return render_template('/cstools/forms_without_orders_edit.html',
                           title='DEA Forms Without Orders - Edit Entry',
                           entry=entry)


@app.route('/cstools/forms-without-orders/update-entry/<entry_id>', methods=['GET', 'POST'])
@login_required_cstools
def update_entry(entry_id):
    form = DeaForms()
    entry = models.Entry.query.get(entry_id)
    if form.validate_on_submit():
        institution = form.institution.data
        contact_name = form.name.data
        contact_email = form.email.data
        csr_name = form.csr_name.data
        item_numbers = form.item_numbers.data
        notes = form.notes.data
        d = cstools_logic.edit_e(entry_id, institution, contact_name, contact_email, csr_name, item_numbers, notes)
        return render_template('/cstools/forms_without_orders.html',
                               title='DEA Forms Without Orders',
                               entries=d['entries'],
                               message=d['message'])

    form.institution.data = entry.institution
    form.name.data = entry.contact_name
    form.email.data = entry.contact_email
    form.item_numbers.data = entry.item_numbers
    form.notes.data = entry.notes
    form.csr_name.data = entry.csr_name

    return render_template('/cstools/forms_without_orders_update.html',
                           title='DEA Forms Without Orders - Update Entry',
                           entry=entry,
                           form=form)


@app.route('/cstools/forms-without-orders/delete-entry/<entry_id>')
@login_required_cstools
def delete_entry(entry_id):
    d = cstools_logic.delete_e(entry_id)
    return render_template('/cstools/forms_without_orders.html',
                           title='DEA Forms Without Orders',
                           message=d['message'],
                           entries=d['entries'])


##############################################################################
# Reddit Image Scraper ######################################################
@app.route('/scrape', methods=['GET', 'POST'])
def scrape_home():
    form = RedditImageScraper()
    return render_template('/reddit_scraper/home.html',
                           form=form,
                           picks=reddit_scraper.picks())


@app.route('/scrape-reddit', methods=['GET', 'POST'])
def scrape():
    form = RedditImageScraper()
    if request.method == 'POST':
        if not form.validate():
            return render_template('/reddit_scraper/home.html',
                                   form=form,
                                   picks=reddit_scraper.picks())
        else:
            form = RedditImageScraper()
            subreddit = str(form.subreddit_choice.data)
            results_from = int(form.results_from.data)
            number = int(form.number.data)
            try:
                min_score = int(form.minimum_score.data)
            except ValueError:
                message = 'Enter a numerical value for minimum score'
                return render_template('/reddit_scraper/home.html',
                                       form=form,
                                       picks=reddit_scraper.picks(),
                                       message=message)

            s = reddit_scraper.scrape_reddit(subreddit, results_from, number, min_score)
            if s == 'no subreddit':
                message = 'It looks like /r/%s doesn\'t exist!' % subreddit
                return render_template('/reddit_scraper/home.html',
                                       form=RedditImageScraper(),
                                       message=message,
                                       picks=reddit_scraper.picks())
            else:
                return render_template('/reddit_scraper/results.html',
                                       good_urls=s['good_urls'],
                                       indirect_urls=s['indirect_urls'],
                                       good_urls_number=s['good_urls_number'],
                                       indirect_urls_number=s['indirect_urls_number'],
                                       subreddit=subreddit,
                                       min_score=min_score,
                                       results_from=s['results_from'],
                                       number=number)
    else:
        return render_template('/reddit_scraper/home.html',
                               form=form)


##############################################################################
# YCS Campaign Site ##########################################################
@app.route('/campaign')
def campaign():
    return render_template('/campaign/home.html')


@app.route('/slogan')
def slogan():
    d = campaign_logic.slogan()
    return jsonify(d)


@app.route('/article')
def article():
    d = campaign_logic.article()
    return jsonify(d)


@app.route('/article2')
def article2():
    d = campaign_logic.article2()
    return jsonify(d)


@app.route('/candidates')
def candidates():
    return render_template('/campaign/candidates.html')


@app.route('/contact')
def contact():
    return render_template('/campaign/contact.html')


@app.route('/press')
def press():
    return render_template('/campaign/press.html')


@app.route('/music')
def music():
    m = music_files.get_songs()
    return render_template('/blog/music.html',
                           title='Music',
                           songs=m['songs'],
                           loops=m['loops'])


@app.route('/welcome')
def welcome():
    return render_template('/blog/welcome.html',
                           title='Welcome')