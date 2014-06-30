from flask import Flask, render_template, request, flash
from forms import DateCheckerForm, BackorderForm, ApplicationForm, DeaForm, NewAccountForm, ShadyForm, DiscrepancyForm,\
    StillNeed, LicenseNeeded, DeaVerify
from urllib import quote
import datetime
import random

app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/home')
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


@app.route('/cstools')
def project2():
    return render_template("/blog/projects/project02.html",
                           title="CSTools")


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


#############################
## Raspberry Pi GIF Display ##
@app.route('/pi_display')
def pi_display():
    file_object = open('e:/programming/projects/blog/app/templates/pi_display/urls.txt', 'r')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/pi_display/pi_display.html",
                           title="Raspberry PI GIF Display",
                           gif_url=gif_url)


@app.route('/pi_display_newest')
def pi_display():
    file_object = open('e:/programming/projects/blog/app/templates/pi_display/urls.txt', 'r')
    urls = list(file_object)
    last_200 = urls[-200:]
    gif_url = random.choice(last_200)
    file_object.close()
    return render_template("/pi_display/pi_display.html",
                           title="Raspberry PI GIF Display - Newest 200 GIFs",
                           gif_url=gif_url)


@app.route('/pi_display_animals')
def pi_display():
    file_object = open('e:/programming/projects/blog/app/templates/pi_display/animals_urls.txt', 'r')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/pi_display/pi_display.html",
                           title="Raspberry PI GIF Display - Animal GIFs",
                           gif_url=gif_url)


@app.route('/pi_display_weird')
def pi_display():
    file_object = open('e:/programming/projects/blog/app/templates/pi_display/pi_display/weird_urls.txt', 'r')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/pi_display/pi_display.html",
                           title="Raspberry PI GIF Display - Weird GIFs",
                           gif_url=gif_url)


@app.route('/pi_display_gaming')
def pi_display():
    file_object = open('e:/programming/projects/blog/app/templates/pi_display/gaming_urls.txt', 'r')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/pi_display/pi_display.html",
                           title="Raspberry PI GIF Display - Gaming GIFs",
                           gif_url=gif_url)


@app.route('/pi_display_educational')
def pi_display():
    file_object = open('e:/programming/projects/blog/app/templates/pi_display/educational_urls.txt', 'r')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/pi_display/pi_display.html",
                           title="Raspberry PI GIF Display - Educational GIFs",
                           gif_url=gif_url)


##########################
#####  CS Tools Apps #####
@app.route('/')
@app.route('/index')
def index():
    return render_template("/CSTools/index.html",
                           title="Home")


@app.route('/datechecker', methods=['GET', 'POST'])
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


@app.route('/backorder', methods=['GET', 'POST'])
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


@app.route('/application', methods=['GET', 'POST'])
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


@app.route('/dea', methods=['GET', 'POST'])
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


@app.route('/newaccount', methods=['GET', 'POST'])
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


@app.route('/shadyblurb', methods=['GET', 'POST'])
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


@app.route('/pricediscrepancy', methods=['GET', 'POST'])
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


@app.route('/stillneed', methods=['GET', 'POST'])
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


@app.route('/licenseneeded', methods=['GET', 'POST'])
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


@app.route('/deaverify', methods=['GET', 'POST'])
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


############################
## Reddit Slideshow Pages ##
@app.route('/reddit_slideshow')
def reddit_slideshow():
    path = 'e:/programming/projects/blog/app/templates/reddit_slideshow/'
    # Path when not at work PC
    #path = 'h:/programming/projects/blog/app/templates/reddit_slideshow/'
    aww_gifs = len(list(open(path + 'aww_gifs_urls.txt', 'r+')))
    highqualitygifs = len(list(open(path + 'highqualitygifs_urls.txt', 'r+')))
    interestinggifs = len(list(open(path + 'interestinggifs_urls.txt', 'r+')))
    naturegifs = len(list(open(path + 'naturegifs_urls.txt', 'r+')))
    perfectloops = len(list(open(path + 'perfectloops_urls.txt', 'r+')))
    spacegifs = len(list(open(path + 'spacegifs_urls.txt', 'r+')))
    surrealgifs = len(list(open(path + 'surrealgifs_urls.txt', 'r+')))
    cinemagraphs = len(list(open(path + 'cinemagraphs_urls.txt', 'r+')))
    return render_template("/reddit_slideshow/home.html",
                           title="Reddit Slideshow",
                           aww_gifs=aww_gifs,
                           highqualitygifs=highqualitygifs,
                           interestinggifs=interestinggifs,
                           naturegifs=naturegifs,
                           perfectloops=perfectloops,
                           spacegifs=spacegifs,
                           surrealgifs=surrealgifs,
                           cinemagraphs=cinemagraphs)


@app.route('/aww_gifs')
def aww_gifs():
    path = 'e:/programming/projects/blog/app/templates/reddit_slideshow/'
    #path = 'h:/programming/projects/blog/app/templates/reddit_slideshow/'
    file_object = open(path + 'aww_gifs_urls.txt', 'r+')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/reddit_slideshow/gif_viewer.html",
                           title="Reddit Slideshow - /r/aww_gifs",
                           gif_url=gif_url)


@app.route('/highqualitygifs')
def highqualitygifs():
    path = 'e:/programming/projects/blog/app/templates/reddit_slideshow/'
    #path = 'h:/programming/projects/blog/app/templates/reddit_slideshow/'
    file_object = open(path + 'highqualitygifs_urls.txt', 'r+')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/reddit_slideshow/gif_viewer.html",
                           title="Reddit Slideshow - /r/highqualitygifs",
                           gif_url=gif_url)


@app.route('/interestinggifs')
def interestinggifs():
    path = 'e:/programming/projects/blog/app/templates/reddit_slideshow/'
    #path = 'h:/programming/projects/blog/app/templates/reddit_slideshow/'
    file_object = open(path + 'interestinggifs_urls.txt', 'r+')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/reddit_slideshow/gif_viewer.html",
                           title="Reddit Slideshow - /r/interestinggifs",
                           gif_url=gif_url)


@app.route('/naturegifs')
def naturegifs():
    path = 'e:/programming/projects/blog/app/templates/reddit_slideshow/'
    #path = 'h:/programming/projects/blog/app/templates/reddit_slideshow/'
    file_object = open(path + 'naturegifs_urls.txt', 'r+')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/reddit_slideshow/gif_viewer.html",
                           title="Reddit Slideshow - /r/naturegifs",
                           gif_url=gif_url)


@app.route('/perfectloops')
def perfectloops():
    path = 'e:/programming/projects/blog/app/templates/reddit_slideshow/'
    #path = 'h:/programming/projects/blog/app/templates/reddit_slideshow/'
    file_object = open(path + 'perfectloops_urls.txt', 'r+')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/reddit_slideshow/gif_viewer.html",
                           title="Reddit Slideshow - /r/perfectloops",
                           gif_url=gif_url)


@app.route('/spacegifs')
def spacegifs():
    path = 'e:/programming/projects/blog/app/templates/reddit_slideshow/'
    #path = 'h:/programming/projects/blog/app/templates/reddit_slideshow/'
    file_object = open(path + 'spacegifs_urls.txt', 'r+')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/reddit_slideshow/gif_viewer.html",
                           title="Reddit Slideshow - /r/spacegifs",
                           gif_url=gif_url)


@app.route('/cinemagraphs')
def cinemagraphs():
    path = 'e:/programming/projects/blog/app/templates/reddit_slideshow/'
    #path = 'h:/programming/projects/blog/app/templates/reddit_slideshow/'
    file_object = open(path + 'cinemagraphs_urls.txt', 'r+')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/reddit_slideshow/gif_viewer.html",
                           title="Reddit Slideshow - /r/cinemagraphs",
                           gif_url=gif_url)


@app.route('/surrealgifs')
def surrealgifs():
    path = 'e:/programming/projects/blog/app/templates/reddit_slideshow/'
    #path = 'h:/programming/projects/blog/app/templates/reddit_slideshow/'
    file_object = open(path + 'surrealgifs_urls.txt', 'r+')
    urls = list(file_object)
    gif_url = random.choice(urls)
    file_object.close()
    return render_template("/reddit_slideshow/gif_viewer.html",
                           title="Reddit Slideshow - /r/surrealgifs",
                           gif_url=gif_url)


if __name__ == '__main__':
    app.run(debug=True)