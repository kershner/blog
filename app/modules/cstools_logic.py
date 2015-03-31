from datetime import datetime, timedelta
from app import db, models
from urllib import quote
import random


# Overly complex code get a random color
class GetClass(object):
    def __init__(self, count, color):
        self.count = count
        self.color = color

    # Logic to determine what color (CSS class) the elements will be
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


def get_css_color():
    get_class_li = GetClass(1, 'purple')
    get_class_li.count = random.randint(1, 9)
    get_class_li.get_color()
    color = get_class_li.color

    return color

##############
# CSTools apps
def datechecker_logic(form_date):
    date_object = datetime.date(datetime.strptime(form_date, '%m/%d/%y'))
    form_expiry_date = date_object + timedelta(days=60)
    form_expiry_date_nice = '%s %s' % (str(form_expiry_date.strftime('%B')), str(form_expiry_date.day))
    days_expired = datetime.today().date() - form_expiry_date
    if form_expiry_date > datetime.today().date():
        message = 'The form is valid until %s,  %s days from now.' % \
                  (form_expiry_date_nice, str(abs(days_expired.days)))
    else:
        message = 'The form expired on %s, %s days ago.' % \
                  (str(form_expiry_date_nice), str(days_expired.days))
    return message


def backorder_logic(po, email, name, item_no, lead_time):
    subject = 'Cayman Chemical Backorder Notification %s' % po
    body = 'Hello %s,\n\nUnfortunately we need to inform you that one '\
           'of your items is currently not available.  Item # %s is ' \
           'in production with an approximate lead time of %s.' % \
           (name, item_no, lead_time)
    signoff = '\n\nI apologize for the inconvenience.  Let me know if you have any questions.' \
              '\n\nHave a great day,\n\n'
    body += signoff

    link = 'mailto:%s?subject=%s&body=%s' % (quote(email), quote(subject), quote(body))

    return link


def backorder_report_logic(name, email):
    subject = 'Cayman Chemical Backorder Report'
    body = 'Hello %s,\n\nAttached find an updated copy of your institution\'s backorder report.\n\n' \
           'Please let me know if you have any questions.\n\n' % name
    link = 'mailto:%s?subject=%s&body=%s' % (quote(email), quote(subject), quote(body))

    return link


def application_logic(name, email):
    subject = 'Cayman Chemical Account Application'
    body = 'Hello %s,\n\nThank you for your interest in Cayman Chemical!  Before you can have your order ' \
           'processed and your items shipped you will need to establish an account with our company.  I have ' \
           'attached our customer account application which has all the instructions you will need, ' \
           'though please don\'t hesitate to call if you have any questions.\n\n' % name
    link = 'mailto:%s?subject=%s&body=%s' % (quote(email), quote(subject), quote(body))

    return link


def dea_logic(name, email, items):
    subject = 'Cayman Chemical DEA Scheduled Compounds Protocol'
    body = 'Hello %s,\n\nThank you for your order with Cayman Chemical!  This is an email to inform you ' \
           'that the following item(s) are DEA scheduled compounds and as such will require additional ' \
           'paperwork before they can be processed: %s.  Attached please find the Cayman Chemical ' \
           'protocol for ordering scheduled compounds as well as a guide for filling out the required 222 ' \
           'form.\n\nIf you have any questions, please don\'t hesitate to ask.\n\nThank you,\n\n' % \
           (name, items)
    link = 'mailto:%s?subject=%s&body=%s' % (quote(email), quote(subject), quote(body))

    return link


def newaccount_logic(name, acct_number, email, net30):
    subject = 'New Account with Cayman Chemical'
    if net30:
        body = 'Hello %s,\n\nThank you for your interest in Cayman Chemical!  A net 30 term account has been ' \
               'established for you.  We accept Purchase Orders, Visa, MasterCard, Discover, American Express, checks, and bank ' \
               'transfers.\n\nTo place an order, please contact customer service at one of the following:\n\nPhone:\t\t 800-364-9897' \
               '\nFax:\t\t    734-971-3640\nEmail:\t\t  orders@caymanchem.com\nWebsite:\thttp://www.caymanchem.com' \
               '\n\nWhen placing an order please reference customer account number %s.\n\nWe look forward to doing ' \
               'business with you!\n\n' % (name, acct_number)
    else:
        body = 'Hello %s,\n\nThank you for your interest in Cayman Chemical!  A prepay account has been ' \
               'established for you.  We accept Visa, MasterCard, Discover, American Express, checks, and bank ' \
               'transfers.  If you would like net 30 terms, please provide bank and trade references.\n\nTo ' \
               'place an order, please contact customer service at one of the following:\n\nPhone:\t\t 800-364-9897' \
               '\nFax:\t\t    734-971-3640\nEmail:\t\t  orders@caymanchem.com\nWebsite:\thttp://www.caymanchem.com' \
               '\n\nWhen placing an order please reference customer account number %s.\n\nWe look forward to doing ' \
               'business with you!\n\n' % (name, acct_number)

    link = 'mailto:%s?subject=%s&body=%s' % (quote(email), quote(subject), quote(body))

    return link


def shadyblurb_logic(email, order_no):
    subject = 'Cayman Chemical Web Order# %s' % order_no
    body = 'To whom it may concern,\n\nCayman Chemical is a biochemical company dedicated to providing ' \
           'quality research grade material to pharmaceutical, academic, and medical institutions.  Our ' \
           'products are manufactured at Cayman Chemical for research purposes only and are not approved by ' \
           'the FDA for over-the-counter use in humans or animals as therapeutic agents.  If you can provide ' \
           'details of the research institution you are affiliated with we may be able to proceed ' \
           'with your order.  We do require that all new customers complete an account application that can ' \
           'be provided to you once we receive the requested information about your institution.\n\nPlease ' \
           'be advised that we do not deliver to residential addresses, P.O. boxes, or warehouses.  Only to ' \
           'businesses and institutions.\n\nThank you for your interest in Cayman Chemical products.  Please ' \
           'feel free to contact me if you have any questions.\n\nBest regards,\n\n'
    link = 'mailto:%s?subject=%s&body=%s' % (quote(email), quote(subject), quote(body))

    return link


def price_discrepancy_logic(email, po, name, item_no, given_price, actual_price):
    subject = 'Cayman Chemical Price Discrepancy %s' % po
    body = 'Hello %s,\n\nWe have received your order but have a pricing discrepancy that needs to be ' \
           'resolved before we can ship any items.  For item #%s you reference a price of $%s but the ' \
           'item\'s actual cost is $%s.  Please confirm whether we should process or cancel the item.\n\n' \
           'Please let me know if you have any questions,\n\n' % \
           (name, item_no, given_price, actual_price)
    link = 'mailto:%s?subject=%s&body=%s' % (quote(email), quote(subject), quote(body))

    return link


def stillneed_logic(name, email, item, order_no):
    subject = 'Regarding your Cayman Chemical Order %s' % order_no
    body = 'Hello %s,\n\nYour order for item #%s is now available and ready to ship!  Since the item has ' \
           'been on a lengthy backorder we\'re sending this email to verify that you still need the item and ' \
           'would like it to be shipped as soon as possible.  Please let me know how you would like ' \
           'to proceed.\n\n' % (name, item)
    link = 'mailto:%s?subject=%s&body=%s' % (quote(email), quote(subject), quote(body))

    return link


def license_needed_logic(name, email, order_no):
    subject = 'DEA License Still Needed Order #%s' % order_no
    body = 'Hello %s,\n\nWe have received your 222 form but we still need an updated copy of your DEA ' \
           'registration before the order can be processed.  Unlike the 222 form, the registration does not ' \
           'need to be an original - you can simply scan your license and email it to me.  Please send us ' \
           'your license as soon as possible to ensure prompt delivery of your order.\n\n' % name
    link = 'mailto:%s?subject=%s&body=%s' % (quote(email), quote(subject), quote(body))

    return link


def dea_verify_logic(order_no, institution):
    email = 'Compliance@caymanchem.com; DEAorderprocessing@caymanchem.com'
    subject = '%s / %s' % (order_no, institution)
    body = 'Hello,\n\nPlease verify these documents.\n\n'
    link = 'mailto:%s?subject=%s&body=%s' % (quote(email), quote(subject), quote(body))

    return link

#########################################
# Forms Without Orders Database Functions
def add_e(institution, name, email, item_numbers, notes, csr_name):
    color = get_css_color()
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

    data = {
        'entries': entries,
        'message': message
    }

    return data


def edit_e(entry_id, institution, name, email, csr_name, item_numbers, notes):
    entry = models.Entry.query.get(entry_id)
    entry.institution = institution
    entry.contact_name = name
    entry.contact_email = email
    entry.csr_name = csr_name
    entry.item_numbers = item_numbers
    entry.notes = notes

    db.session.commit()

    entries = models.Entry.query.all()
    message = 'The entry for %s has been updated.' % entry.institution

    data = {
        'entries': entries,
        'message': message
    }

    return data


def delete_e(entry_id):
    entry = models.Entry.query.get(entry_id)
    db.session.delete(entry)
    db.session.commit()
    entries = models.Entry.query.all()
    message = 'Successfully deleted entry for %s.' % entry.institution

    data = {
        'message': message,
        'entries': entries
    }

    return data