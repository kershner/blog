from functools import wraps
from flask import jsonify, render_template, request, flash, redirect, url_for, session
from modules import music_files, campaign_logic, reddit_scraper, cstools_logic, gif_party_logic, pi_config, \
    pi_display_logic, cms_logic
from forms import *
import credentials
from app import app, models


##############################################################################
# Blog #######################################################################
@app.route('/')
def index():
    return render_template('/blog/welcome.html',
                           title='Welcome')


@app.route('/blog')
def blog():
    data = cms_logic.get_posts()
    return render_template('/blog/home.html',
                           posts=data['posts'],
                           link=data['link'])


@app.route('/projects')
def projects():
    return render_template('/blog/projects.html',
                           title='Projects')


@app.route('/music')
def music():
    m = music_files.get_songs()
    return render_template('/blog/music.html',
                           title='Music',
                           songs=m['songs'],
                           loops=m['loops'])


@app.route('/about')
def about():
    return render_template('/blog/about.html',
                           title='About Me')


@app.route('/resume')
def resume():
    return render_template('/blog/resume.html',
                            title='Resume')


# Project Pages
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
    data = pi_display_logic.pi_display_main()
    return jsonify(data)


##############################################################################
# Pi Display Config ##########################################################
@app.route('/pi_display_config')
def pi_display_config():
    data = pi_config.pi_config_main()
    return render_template('/pi_display/pi_display_config.html',
                           current_gif=data['current_gif'],
                           main_urls_count=data['main_urls_count'],
                           animals_urls_count=data['animals_urls_count'],
                           gaming_urls_count=data['gaming_urls_count'],
                           strange_urls_count=data['strange_urls_count'],
                           educational_urls_count=data['educational_urls_count'],
                           category=data['category'].title(),
                           delay=data['delay'])


@app.route('/pi-display-config-update')
def pi_display_config_update():
    data = pi_config.pi_config_update()
    return jsonify(data)


@app.route('/pi-display-config-prev')
def pi_display_config_prev():
    data = pi_config.get_prev()
    return jsonify(data)


@app.route('/pi-display-config-auto')
def pi_display_config_auto():
    data = pi_config.set_auto_update()
    return jsonify(data)


@app.route('/pi-display-config-categories')
def pi_display_config_all():
    data = pi_config.set_category()
    return jsonify(data)


@app.route('/pi-display-config-delay')
def pi_display_config_delay():
    data = pi_config.set_delay()
    return jsonify(data)


@app.route('/previous-gifs')
def previous_gifs():
    data = pi_config.get_previous_gifs()
    return jsonify(data)


@app.route('/last-played/<number>')
def last_played(number):
    data = pi_config.get_last_played(number)
    return jsonify(data)


@app.route('/clear-session')
def clear_session():
    data = pi_config.clear()
    return jsonify(data)


@app.route('/email-gifs')
def email_gifs():
    data = pi_config.get_email_link()
    return jsonify(data)


##############################################################################
# Gif Party ##################################################################
@app.route('/gif_party')
def gif_party_welcome():
    return render_template('/gif_party/welcome.html',
                           image_url=gif_party_logic.get_image())


@app.route('/gif_party_about')
def gif_party_about():
    return render_template('/gif_party/about.html')


@app.route('/gif_party_viewer', methods=['GET', 'POST'])
def gif_party():
    form = GifParty()
    data = gif_party_logic.get_image_counts()

    return render_template('/gif_party/gif_party.html',
                           form=form,
                           main_urls_count=data['main_urls_count'],
                           animals_urls_count=data['animals_urls_count'],
                           gaming_urls_count=data['gaming_urls_count'],
                           strange_urls_count=data['strange_urls_count'],
                           educational_urls_count=data['educational_urls_count'])


@app.route('/gif_party_json')
def gif_party_json():
    data = gif_party_logic.gif_party_main()
    return jsonify(data)


@app.route('/gif_party_json_all')
def gif_party_json_all():
    data = gif_party_logic.select_category('all')
    return jsonify(data)


@app.route('/gif_party_json_animals')
def gif_party_json_animals():
    data = gif_party_logic.select_category('animals')
    return jsonify(data)


@app.route('/gif_party_json_gaming')
def gif_party_json_gaming():
    data = gif_party_logic.select_category('gaming')
    return jsonify(data)


@app.route('/gif_party_json_strange')
def gif_party_json_strange():
    data = gif_party_logic.select_category('strange')
    return jsonify(data)


@app.route('/gif_party_json_educational')
def gif_party_json_educational():
    data = gif_party_logic.select_category('educational')
    return jsonify(data)


@app.route('/gif_party_json_5')
def gif_party_json_5():
    data = gif_party_logic.select_number(5)
    return jsonify(data)


@app.route('/gif_party_json_10')
def gif_party_json_10():
    data = gif_party_logic.select_number(10)
    return jsonify(data)


@app.route('/gif_party_json_20')
def gif_party_json_20():
    data = gif_party_logic.select_number(20)
    return jsonify(data)


@app.route('/gif_party_json_delay', methods=['GET', 'POST'])
def gif_party_json_delay():
    data = gif_party_logic.gif_party_delay()
    return jsonify(data)


# ###################################################################################
# #  CS Tools Apps ##################################################################
@app.route('/cstools')
def cstools():
    return render_template('/cstools/temp.html',
                          title='Home')


# @app.route('/cstools/datechecker', methods=['GET', 'POST'])
# def datechecker():
#     form = DateCheckerForm()
#     if request.method == 'POST':
#         if not form.validate():
#             return render_template('/cstools/datechecker.html',
#                                   title='222 Form Date Checker',
#                                   form=form)
#         else:
#             try:
#                 form_date = form.form_date.data
#                 return render_template('/cstools/datechecker.html',
#                                       title="222 Form Date Checker",
#                                       form=form,
#                                       message=cstools_logic.datechecker_logic(form_date))
#             except ValueError:
#                 message = 'Enter the form\'s issue date in the format MM/DD/YY.'
#                 return render_template('/cstools/datechecker.html',
#                                       title='222 Form Date Checker',
#                                       form=form,
#                                       message=message)
#     elif request.method == 'GET':
#         return render_template('/cstools/datechecker.html',
#                               title='222 Form Date Checker',
#                               form=form)


# @app.route('/cstools/backorder', methods=['GET', 'POST'])
# def backorder():
#     form = BackorderForm()
#     if request.method == 'POST':
#         if not form.validate():
#             flash('All fields are required.')
#             return render_template('/cstools/backorder.html',
#                                   title='Backorder Template',
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#         else:
#             email = form.email.data
#             po = form.po.data
#             name = form.name.data
#             item_no = form.item_number.data
#             lead_time = form.lead_time.data
#             link = cstools_logic.backorder_logic(po, email, name, item_no, lead_time)
#             return render_template('/cstools/backorder.html',
#                                   title='Backorder Template',
#                                   link=link,
#                                   form=form,
#                                   color=cstools_logic.get_css_color())

#     elif request.method == 'GET':
#         return render_template('/cstools/backorder.html',
#                               title='Backorder Template',
#                               form=form,
#                               color=cstools_logic.get_css_color())


# @app.route('/cstools/backorder-report', methods=['GET', 'POST'])
# def backorder_report():
#     form = BackorderReport()
#     if request.method == 'POST':
#         if not form.validate():
#             flash('All fields are required.')
#             return render_template('/cstools/backorder-report.html',
#                                   title='Backorder Report Template',
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#         else:
#             name = form.name.data
#             email = form.email.data
#             link = cstools_logic.backorder_report_logic(name, email)
#             return render_template('/cstools/backorder-report.html',
#                                   title='Backorder Report Template',
#                                   link=link,
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#     elif request.method == 'GET':
#         return render_template('/cstools/backorder-report.html',
#                               title='Backorder Report Template',
#                               form=form,
#                               color=cstools_logic.get_css_color())


# @app.route('/cstools/application', methods=['GET', 'POST'])
# def application():
#     form = ApplicationForm()
#     if request.method == 'POST':
#         if not form.validate():
#             flash('All fields are required.')
#             return render_template('/cstools/application.html',
#                                   title='Account Application Template',
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#         else:
#             name = form.name.data
#             email = form.email.data
#             link = cstools_logic.application_logic(name, email)
#             return render_template('/cstools/application.html',
#                                   title='Account Application Template',
#                                   link=link,
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#     elif request.method == 'GET':
#         return render_template('/cstools/application.html',
#                               title='Account Application Template',
#                               form=form,
#                               color=cstools_logic.get_css_color())


# @app.route('/cstools/dea', methods=['GET', 'POST'])
# def dea():
#     form = DeaForm()
#     if request.method == 'POST':
#         if not form.validate():
#             flash('All fields are required.')
#             return render_template('/cstools/dea.html',
#                                   title='DEA Protocol Template',
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#         else:
#             name = form.name.data
#             email = form.email.data
#             items = form.dea_items.data
#             link = cstools_logic.dea_logic(name, email, items)
#             return render_template('/cstools/dea.html',
#                                   title='DEA Protocol Template',
#                                   link=link,
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#     elif request.method == 'GET':
#         return render_template('/cstools/dea.html',
#                               title='DEA Protocol Template',
#                               form=form,
#                               color=cstools_logic.get_css_color())


# @app.route('/cstools/newaccount', methods=['GET', 'POST'])
# def newaccount():
#     form = NewAccountForm()
#     if request.method == 'POST':
#         if not form.validate():
#             flash('All fields are required.')
#             return render_template('/cstools/newaccount.html',
#                                   title='New Account Template',
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#         else:
#             name = form.name.data
#             acct_number = form.acct.data
#             email = form.email.data
#             net30 = form.net30.data
#             link = cstools_logic.newaccount_logic(name, acct_number, email, net30)
#             return render_template('/cstools/newaccount.html',
#                                   title='New Account Template',
#                                   link=link,
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#     elif request.method == 'GET':
#         return render_template('/cstools/newaccount.html',
#                               title='New Account Template',
#                               form=form,
#                               color=cstools_logic.get_css_color())


# @app.route('/cstools/shadyblurb', methods=['GET', 'POST'])
# def shadyblurb():
#     form = ShadyForm()
#     if request.method == 'POST':
#         if not form.validate():
#             flash('All fields are required.')
#             return render_template('/cstools/shadyblurb.html',
#                                   title='Shady Customer Blurb',
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#         else:
#             email = form.email.data
#             order_no = form.order_no.data
#             link = cstools_logic.shadyblurb_logic(email, order_no)
#             return render_template('/cstools/shadyblurb.html',
#                                   title='Shady Customer Blurb',
#                                   link=link,
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#     elif request.method == 'GET':
#         return render_template('/cstools/shadyblurb.html',
#                               title='Shady Customer Blurb',
#                               form=form,
#                               color=cstools_logic.get_css_color())


# @app.route('/cstools/pricediscrepancy', methods=['GET', 'POST'])
# def price_discrepancy():
#     form = DiscrepancyForm()
#     if request.method == 'POST':
#         if not form.validate():
#             flash('All fields are required.')
#             return render_template('/cstools/pricediscrepancy.html',
#                                   title='Price Discrepancy Template',
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#         else:
#             email = form.email.data
#             po = form.po.data
#             name = form.name.data
#             item_no = form.item_number.data
#             given_price = form.given_price.data
#             actual_price = form.actual_price.data
#             link = cstools_logic.price_discrepancy_logic(email, po, name, item_no, given_price, actual_price)
#             return render_template('/cstools/pricediscrepancy.html',
#                                   title='Price Discrepancy Template',
#                                   link=link,
#                                   form=form,
#                                   color=cstools_logic.get_css_color())

#     elif request.method == 'GET':
#         return render_template('/cstools/pricediscrepancy.html',
#                               title='Price Discrepancy Template',
#                               form=form,
#                               color=cstools_logic.get_css_color())


# @app.route('/cstools/stillneed', methods=['GET', 'POST'])
# def still_need():
#     form = StillNeed()
#     if request.method == 'POST':
#         if not form.validate():
#             flash('All fields are required.')
#             return render_template('/cstools/stillneed.html',
#                                   title='Still Need Item? Template',
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#         else:
#             name = form.name.data
#             email = form.email.data
#             item = form.item_number.data
#             order_no = form.order_no.data
#             link = cstools_logic.stillneed_logic(name, email, item, order_no)
#             return render_template('/cstools/stillneed.html',
#                                   title='Still Need Item? Template',
#                                   link=link,
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#     elif request.method == 'GET':
#         return render_template('/cstools/stillneed.html',
#                               title='Still Need Item? Template',
#                               form=form,
#                               color=cstools_logic.get_css_color())


# @app.route('/cstools/licenseneeded', methods=['GET', 'POST'])
# def license_needed():
#     form = LicenseNeeded()
#     if request.method == 'POST':
#         if not form.validate():
#             flash('All fields are required.')
#             return render_template('/cstools/licenseneeded.html',
#                                   title='DEA License Needed Template',
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#         else:
#             name = form.name.data
#             email = form.email.data
#             order_no = form.order_no.data
#             link = cstools_logic.license_needed_logic(name, email, order_no)
#             return render_template('/cstools/licenseneeded.html',
#                                   title='DEA License Needed Template',
#                                   link=link,
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#     elif request.method == 'GET':
#         return render_template('/cstools/licenseneeded.html',
#                               title='DEA License Needed Template',
#                               form=form,
#                               color=cstools_logic.get_css_color())


# @app.route('/cstools/deaverify', methods=['GET', 'POST'])
# def dea_verify():
#     form = DeaVerify()
#     if request.method == 'POST':
#         if not form.validate():
#             flash('All fields are required.')
#             return render_template('/cstools/deaverify.html',
#                                   title='DEA Documents Verification Template',
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#         else:
#             order_no = form.order_no.data
#             institution = form.institution.data
#             link = cstools_logic.dea_verify_logic(order_no, institution)
#             return render_template('/cstools/deaverify.html',
#                                   title='DEA Documents Verification Template',
#                                   link=link,
#                                   form=form,
#                                   color=cstools_logic.get_css_color())
#     elif request.method == 'GET':
#         return render_template('/cstools/deaverify.html',
#                               title='DEA Documents Verification Template',
#                               form=form,
#                               color=cstools_logic.get_css_color())


# def login_required_cstools(test):
#     @wraps(test)
#     def wrap(*args, **kwargs):
#         if 'cstoolslogged_in' in session:
#             return test(*args, **kwargs)
#         else:
#             error = 'You need to log in first.'
#             return render_template('/cstools/login.html',
#                                   title='Login',
#                                   error=error)
#     return wrap


# @app.route('/cstools/login', methods=['GET', 'POST'])
# def cstools_login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != credentials.username or request.form['password'] != credentials.password:
#             error = 'Invalid credentials, please try again.'
#         else:
#             session['cstoolslogged_in'] = True
#             return redirect(url_for('forms_without_orders'))
#     return render_template('/cstools/login.html',
#                           title='Login',
#                           error=error)


# @app.route('/cstools/logout')
# def cstools_logout():
#     if 'logged_in_cstools' in session:
#         session.pop('cstoolslogged_in', None)
#         return redirect(url_for('cstools'))
#     else:
#         return redirect(url_for('cstools'))


# @app.route('/cstools/forms-without-orders', methods=['GET', 'POST'])
# @login_required_cstools
# def forms_without_orders():
#     form = DeaForms()
#     if request.method == 'POST':
#         if not form.validate():
#             entries = models.Entry.query.all()
#             flash('All fields are required.')
#             return render_template('/cstools/forms_without_orders.html',
#                                   title='DEA Forms Without Orders',
#                                   form=form,
#                                   entries=entries,
#                                   new_entry=True)
#         else:
#             institution = form.institution.data
#             name = form.name.data
#             email = form.email.data
#             csr_name = form.csr_name.data
#             item_numbers = form.item_numbers.data
#             notes = form.notes.data
#             d = cstools_logic.add_e(institution, name, email, item_numbers, notes, csr_name)
#             return render_template('/cstools/forms_without_orders.html',
#                                   title='DEA Forms Without Orders',
#                                   entries=d['entries'],
#                                   message=d['message'])
#     elif request.method == 'GET':
#         entries = models.Entry.query.all()
#         return render_template('/cstools/forms_without_orders.html',
#                               title='DEA Forms Without Orders',
#                               entries=entries)


# @app.route('/cstools/forms-without-orders/new-entry')
# @login_required_cstools
# def new_entry():
#     form = DeaForms()
#     entries = models.Entry.query.all()
#     return render_template('/cstools/forms_without_orders.html',
#                           title='DEA Forms Without Orders',
#                           form=form,
#                           entries=entries,
#                           new_entry=True)


# @app.route('/cstools/forms-without-orders/edit-entry/<entry_id>')
# @login_required_cstools
# def edit_entry(entry_id):
#     entry = models.Entry.query.get(entry_id)
#     return render_template('/cstools/forms_without_orders_edit.html',
#                           title='DEA Forms Without Orders - Edit Entry',
#                           entry=entry)


# @app.route('/cstools/forms-without-orders/update-entry/<entry_id>', methods=['GET', 'POST'])
# @login_required_cstools
# def update_entry(entry_id):
#     form = DeaForms()
#     entry = models.Entry.query.get(entry_id)
#     if form.validate_on_submit():
#         institution = form.institution.data
#         contact_name = form.name.data
#         contact_email = form.email.data
#         csr_name = form.csr_name.data
#         item_numbers = form.item_numbers.data
#         notes = form.notes.data
#         d = cstools_logic.edit_e(entry_id, institution, contact_name, contact_email, csr_name, item_numbers, notes)
#         return render_template('/cstools/forms_without_orders.html',
#                               title='DEA Forms Without Orders',
#                               entries=d['entries'],
#                               message=d['message'])

#     form.institution.data = entry.institution
#     form.name.data = entry.contact_name
#     form.email.data = entry.contact_email
#     form.item_numbers.data = entry.item_numbers
#     form.notes.data = entry.notes
#     form.csr_name.data = entry.csr_name

#     return render_template('/cstools/forms_without_orders_update.html',
#                           title='DEA Forms Without Orders - Update Entry',
#                           entry=entry,
#                           form=form)


# @app.route('/cstools/forms-without-orders/delete-entry/<entry_id>')
# @login_required_cstools
# def delete_entry(entry_id):
#     d = cstools_logic.delete_e(entry_id)
#     return render_template('/cstools/forms_without_orders.html',
#                           title='DEA Forms Without Orders',
#                           message=d['message'],
#                           entries=d['entries'])


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


@app.route('/pool')
def pool():
    return render_template('/pool/home.html')