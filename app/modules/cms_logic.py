from flask import flash, render_template, redirect, session, url_for, request, jsonify, Markup, abort
from app import app, models, db, forms
from datetime import datetime, timedelta
from markdown import markdown
from functools import wraps
import calendar
import bleach
import collections
import os


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            abort(401)
    return wrap


# Filter to render markdown in templates
@app.template_filter('markdown')
def render_markdown(markdown_text):
    return Markup(markdown(markdown_text))


def get_posts():
    # Sorting by ID (descending order)
    posts = models.Post.query.order_by(models.Post.id.desc()).all()
    posts_to_display = []

    counter = 0
    for post in posts:
        if counter == 5:
            break
        else:
            posts_to_display.append(post)
        counter += 1

    if 'logged_in' in session:
        link = '/cms'
    else:
        link = ''

    data = {
        'posts': posts_to_display,
        'link': link
    }

    return data


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
    tags = ['pre', 'code', 'iframe', 'red', 'blue', 'yellow', 'green',
            'purple', 'div', 'a', 'img', 'br']

    attrs = {
        'code': ['data-language', 'class'],
        'iframe': ['class', 'width', 'height', 'src', 'frameborder', 'allowfullscreen'],
        'div': ['class'],
        'a': ['href'],
        'img': ['src', 'class'],
        'br': ['class']
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
def stats(posts, public):
    word_list = []
    total_posts = 0
    filter_list = ['class="rounded-images"', 'the', 'to', 'it', 'on', 'a',
                   'and', 'of', 'I']
    for post in posts:
        if not public:
            words_1 = (str(post.title).split())
            words_2 = (str(post.subtitle).split())
            words_3 = (str(post.content).split())
        else:
            words_1 = (str(post.pub_title).split())
            words_2 = (str(post.pub_subtitle).split())
            words_3 = (str(post.pub_content).split())
        for word in words_1:
            if word not in filter_list:
                word_list.append(word)
        for word in words_2:
            if word not in filter_list:
                word_list.append(word)
        for word in words_3:
            if word not in filter_list:
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


# Return CSS class based on previous entry's primary ID
def get_color(post_id):
    if post_id % 2 == 0:
        return 'grey'
    else:
        return 'white'


# Legacy code for themes, might still re-implement
def get_theme(color):
    if color == 'rgb(232, 234, 246)' or color == 'blue-grey':
        return 'blue-grey'
    elif color == 'rgb(245, 245, 245)' or color == 'grey':
        return 'grey'
    elif color == 'rgb(255, 255, 255)' or color == 'white':
        return 'white'
    elif color == 'rgb(227, 242, 253)' or color == 'blue':
        return 'blue'
    else:
        return


# Return True if there are posts requiring approval
def approval_notification():
    posts = models.PublicPost.query.order_by(models.PublicPost.pub_id.desc()).all()
    to_be_approved = []
    for post in posts:
        if not post.approved:
            to_be_approved.append(post)

    if to_be_approved:
        return True
    else:
        return False


##############################################################################
# CMS ########################################################################
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
    form = forms.LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        verify = password_validate(username, password)

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
    needs_approval = approval_notification()

    if posts:
        current_month = datetime.today().strftime('%B %Y')
        last_month = (datetime.today() - timedelta(weeks=4)).strftime('%B %Y')
        two_months_ago = (datetime.today() - timedelta(weeks=8)).strftime('%B %Y')
        current_month_posts = []
        last_month_posts = []
        two_months_ago_posts = []
        older_posts = []
        statistics = stats(posts, 0)

        for post in posts:
            if get_recent_posts(post) == 'Current Month':
                current_month_posts.append(post)
            elif get_recent_posts(post) == 'Last Month':
                last_month_posts.append(post)
            elif get_recent_posts(post) == 'Two Months Ago':
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
                           icons=dog_icons(),
                           form=forms.DatabaseForm(),
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
    form = forms.DatabaseForm()
    form.month.data = datetime.today().month
    form.year.data = datetime.today().year
    form.hidden_date.data = datetime.today().strftime('%A %B %d, %Y')
    # Grabbing most recent entry's primary key to determine next CSS class
    latest_id = models.Post.query.all()[-1].id + 1
    form.color.data = get_color(latest_id)
    link = '/cms'
    text = 'CMS'

    return render_template('/blog/cms/new-post.html',
                           form=form,
                           icons=dog_icons(),
                           link=link,
                           text=text,
                           title='New Post')


@app.route('/cms-submit', methods=['GET', 'POST'])
@login_required
def cms_submit():
    form = forms.DatabaseForm()
    if not form.validate_on_submit():
        return render_template('/blog/cms/new-post.html',
                               icons=dog_icons(),
                               form=form)
    else:
        css_class = get_theme(form.color.data)
        title = bleach.clean(form.title.data)
        icon = form.icon.data
        subtitle = bleach.clean(form.subtitle.data)
        content = generate_markdown(form.content.data, True)
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
    content = generate_markdown(request.args.get('content', 0, type=str), False)
    div_class = get_theme(color)
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
    form = forms.DatabaseForm()
    post = models.Post.query.get(unique_id)
    link = '/cms'
    text = 'CMS'

    form.color.data = post.css_class
    form.icon.data = post.icon
    form.title.data = post.title
    form.subtitle.data = post.subtitle
    form.content.data = generate_markdown(post.content, True)
    form.hidden_date.data = post.date
    form.month.data = post.month
    form.year.data = post.year

    return render_template('/blog/cms/edit-post.html',
                           post=post,
                           form=form,
                           icons=dog_icons(),
                           link=link,
                           text=text,
                           title='Edit Post')


@app.route('/update-post/<unique_id>', methods=['GET', 'POST'])
@login_required
def cms_update(unique_id):
    form = forms.DatabaseForm()
    post = models.Post.query.get(unique_id)

    if form.validate_on_submit():
        post.css_class = get_theme(form.color.data)
        post.title = bleach.clean(form.title.data)
        post.icon = form.icon.data
        post.subtitle = bleach.clean(form.subtitle.data)
        post.content = generate_markdown(form.content.data, True)
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
                           icons=dog_icons())


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
    statistics = stats(approved_posts, 1)

    return render_template('/blog/public-cms/public-cms.html',
                           posts=approved_posts,
                           stats=statistics,
                           title='Public CMS')


@app.route('/public-new-post')
def public_new_post():
    form = forms.PublicDatabaseForm()
    form.month.data = datetime.today().month
    form.year.data = datetime.today().year
    form.hidden_date.data = datetime.today().strftime('%A %B %d, %Y')
    # Grabbing most recent entry's primary key to determine next CSS class
    latest_id = models.PublicPost.query.all()[-1].pub_id + 1
    form.color.data = get_color(latest_id)

    return render_template('/blog/public-cms/public-new-post.html',
                           form=form,
                           icons=dog_icons(),
                           title='New Public Post')


@app.route('/public-cms-submit', methods=['GET', 'POST'])
def public_cms_submit():
    form = forms.PublicDatabaseForm()
    if not form.validate_on_submit():
        return render_template('/blog/public-cms/public-new-post.html',
                               icons=dog_icons(),
                               form=form)
    else:
        css_class = get_theme(form.color.data)
        title = bleach.clean(form.title.data)
        author = bleach.clean(form.author.data)
        icon = form.icon.data
        subtitle = bleach.clean(form.subtitle.data)
        content = generate_markdown(form.content.data, True)
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
    form = forms.PublicDatabaseForm()
    post = models.PublicPost.query.get(unique_id)
    approved = post.approved

    form.color.data = post.pub_css_class
    form.icon.data = post.pub_icon
    form.title.data = post.pub_title
    form.author.data = post.author
    form.subtitle.data = post.pub_subtitle
    form.content.data = generate_markdown(post.pub_content, True)
    form.hidden_date.data = post.pub_date
    form.month.data = post.pub_month
    form.year.data = post.pub_year

    return render_template('/blog/public-cms/public-edit-post.html',
                           post=post,
                           approved=approved,
                           form=form,
                           icons=dog_icons(),
                           title='Edit Public Post')


@app.route('/public-update-post/<unique_id>', methods=['GET', 'POST'])
@login_required
def public_cms_update(unique_id):
    form = forms.PublicDatabaseForm()
    post = models.PublicPost.query.get(unique_id)

    if form.validate_on_submit():
        post.pub_css_class = get_theme(form.color.data)
        post.pub_title = bleach.clean(form.title.data)
        post.author = bleach.clean(form.author.data)
        post.pub_icon = form.icon.data
        post.pub_subtitle = bleach.clean(form.subtitle.data)
        post.pub_content = generate_markdown(form.content.data, True)
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
                           icons=dog_icons())


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