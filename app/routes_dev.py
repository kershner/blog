from flask import Flask, render_template, request, flash
from forms import DateCheckerForm, BackorderForm, ApplicationForm, DeaForm, NewAccountForm, ShadyForm, DiscrepancyForm,\
    StillNeed, LicenseNeeded
from urllib import quote
import datetime

app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/home')
def home():
    return render_template("home.html",
                           title="Home")


@app.route('/about')
def about():
    return render_template("about.html",
                           title="About Me")


@app.route('/projects')
def projects():
    return render_template("projects.html",
                           title="Projects")


##########################
#####  CS Tools Apps #####
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
                           title="Home")


@app.route('/datechecker', methods=['GET', 'POST'])
def datechecker():
    form = DateCheckerForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template("datechecker.html",
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

                return render_template("datechecker.html",
                                       title="222 Form Date Checker",
                                       form=form,
                                       message=message)
            except ValueError:
                message = "Enter the form's issue date in the format MM/DD/YY."
                return render_template("datechecker.html",
                                       title="222 Form Date Checker",
                                       form=form,
                                       message=message)
    elif request.method == 'GET':
        return render_template("datechecker.html",
                               title="222 Form Date Checker",
                               form=form)


@app.route('/backorder', methods=['GET', 'POST'])
def backorder():
    form = BackorderForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("backorder.html",
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
            return render_template("backorder.html",
                                   title="Backorder Template",
                                   link=link,
                                   form=form)

    elif request.method == 'GET':
        return render_template("backorder.html",
                               title="Backorder Template",
                               form=form)


@app.route('/application', methods=['GET', 'POST'])
def application():
    form = ApplicationForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("application.html",
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
            return render_template("application.html",
                                   title="Account Application Template1",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("application.html",
                               title="Account Application Template2",
                               form=form)


@app.route('/dea', methods=['GET', 'POST'])
def dea():
    form = DeaForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("dea.html",
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
            return render_template("dea.html",
                                   title="DEA Protocol Template",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("dea.html",
                               title="DEA Protocol Template",
                               form=form)


@app.route('/newaccount', methods=['GET', 'POST'])
def newaccount():
    form = NewAccountForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("newaccount.html",
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
            return render_template("newaccount.html",
                                   title="New Account Template",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("newaccount.html",
                               title="New Account Template",
                               form=form)


@app.route('/shadyblurb', methods=['GET', 'POST'])
def shadyblurb():
    form = ShadyForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("shadyblurb.html",
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
            return render_template("shadyblurb.html",
                                   title="Shady Customer Blurb",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("shadyblurb.html",
                               title="Shady Customer Blurb",
                               form=form)


@app.route('/pricediscrepancy', methods=['GET', 'POST'])
def price_discrepancy():
    form = DiscrepancyForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("pricediscrepancy.html",
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
            return render_template("pricediscrepancy.html",
                                   title="Price Discrepancy Template",
                                   link=link,
                                   form=form)

    elif request.method == 'GET':
        return render_template("pricediscrepancy.html",
                               title="Price Discrepancy Template",
                               form=form)


@app.route('/stillneed', methods=['GET', 'POST'])
def still_need():
    form = StillNeed()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("stillneed.html",
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
            return render_template("stillneed.html",
                                   title="Still Need Item? Template",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("stillneed.html",
                               title="Still Need Item? Template",
                               form=form)


@app.route('/licenseneeded', methods=['GET', 'POST'])
def license_needed():
    form = LicenseNeeded()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("licenseneeded.html",
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
            return render_template("licenseneeded.html",
                                   title="DEA License Needed Template",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("licenseneeded.html",
                               title="DEA License Needed Template",
                               form=form)


if __name__ == '__main__':
    app.run(debug=True)