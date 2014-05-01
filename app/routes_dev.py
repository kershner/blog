from flask import Flask, render_template, request, flash
from forms import ContactForm, DateCheckerForm, ApplicationForm
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
    form = ContactForm()
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
                   "you have any questions.\n\nHave a great day," % \
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
                   "though please don't hesitate to call if you have any questions." % name
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
    form = ApplicationForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template("dea.html",
                                   title="DEA Protocol Template",
                                   form=form)
        else:
            name = form.name.data
            email = form.email.data
            subject = "Cayman Chemical DEA Scheduled Compounds Protocol"
            body = "Hello %s,\n\nThank you for your order with Cayman Chemical!  This is an email to inform you " \
                   "that some or all of the items on your order are DEA scheduled compounds and as such will require " \
                   "additional paperwork before they can be processed.  Attached please  find the Cayman Chemical " \
                   "protocol for ordering scheduled compounds as well as a guide for filling out the required 222 " \
                   "form.\n\nIf ou have any questions, please don't hesitate to ask.\n\nThank you," % name
            link = "mailto:%s?subject=%s&body=%s" % (quote(email), quote(subject), quote(body))
            return render_template("dea.html",
                                   title="DEA Protocol Template",
                                   link=link,
                                   form=form)
    elif request.method == 'GET':
        return render_template("dea.html",
                               title="DEA Protocol Template",
                               form=form)


if __name__ == '__main__':
    app.run(debug=True)