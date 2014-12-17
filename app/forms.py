from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import Required, Optional, DataRequired

#############################################
# CSTools Forms


class BackorderForm(Form):
    email = StringField("Contact's Email Address", [Required("Please enter the contact's Email address.")])
    po = StringField("Purchase Order or Sales Order", [Required("Please enter the PO or Sales Order Number.")])
    name = StringField("Contact Name", [Required("Please enter the contact's name.")])
    item_number = StringField("Item Number", [Required("Please enter the item's number.")])
    lead_time = StringField("Lead Time", [Required("Please the estimated lead time.")])
    submit = SubmitField("Submit")


class DateCheckerForm(Form):
    form_date = StringField("Form Date", [Required("Enter the form's issue date in the format MM/DD/YY.")])
    submit = SubmitField("Submit")


class ApplicationForm(Form):
    name = StringField("Contact Name", [Required("Please enter the contact's name.")])
    email = StringField("Contact's Email Address", [Required("Please enter the contact's Email address.")])
    submit = SubmitField("Submit")


class NewAccountForm(Form):
    name = StringField("Contact Name", [Required("Please enter the contact's name.")])
    acct = StringField("Customer Account Number", [Required("Please enter the customer's account number.")])
    email = StringField("Contact's Email Address", [Required("Please enter the contact's Email address.")])
    net30 = BooleanField(default=False)
    submit = SubmitField("Submit")


class DeaForm(Form):
    name = StringField("Contact Name", [Required("Please enter the contact's name.")])
    email = StringField("Contact's Email Address", [Required("Please enter the contact's Email address.")])
    dea_items = StringField("Regulated Items", [Required("Please enter the regulated item(s).")])
    submit = SubmitField("Submit")


class ShadyForm(Form):
    email = StringField("Contact's Email Address", [Required("Please enter the contact's Email address.")])
    order_no = StringField("Sales Order Number", [Required("Please enter the sales order number.")])
    submit = SubmitField("Submit")


class DiscrepancyForm(Form):
    name = StringField("Contact Name", [Required("Please enter the contact's name.")])
    email = StringField("Contact's Email Address", [Required("Please enter the contact's Email address.")])
    po = StringField("Purchase Order or Sales Order", [Required("Please enter the PO or Sales Order Number.")])
    item_number = StringField("Item Number", [Required("Please enter the item's number.")])
    given_price = StringField("Customer's Given Price", [Required("Please enter the price given by the "
                                                                           "customer.")])
    actual_price = StringField("Actual Price", [Required("Please enter the item's actual price.")])
    submit = SubmitField("Submit")


class StillNeed(Form):
    name = StringField("Contact's Name", [Required("Please enter the contact's name.")])
    email = StringField("Contact's Email Address", [Required("Please enter the contact's Email address.")])
    item_number = StringField("Item Number", [Required("Please enter the item's number.")])
    order_no = StringField("Sales Order Number", [Required("Please enter the sales order number.")])
    submit = SubmitField("Submit")


class LicenseNeeded(Form):
    name = StringField("Contact's Name", [Required("Please enter the contact's name.")])
    email = StringField("Contact's Email Address", [Required("Please enter the contact's Email address.")])
    order_no = StringField("Sales Order Number", [Required("Please enter the sales order number.")])
    submit = SubmitField("Submit")


class DeaVerify(Form):
    order_no = StringField("Sales Order Number", [Required("Please enter the sales order number.")])
    institution = StringField("Institution", [Required("Please enter the institution's name.")])
    submit = SubmitField("Submit")


class DeaForms(Form):
    institution = StringField("Institution", [Required("Enter the name of the institution.")])
    name = StringField("Contact's Name", [Required("Enter the contact's name.")])
    email = StringField("Contact's Email", [Required("Enter the contact's email.")])
    item_numbers = StringField("Item #s.", [Required("Enter the item numbers from the 222 form.")])
    notes = TextAreaField("Notes.")
    csr_name = StringField("Your name.", [Required("Enter your name.")])
    submit = SubmitField("Submit")


class BackorderReport(Form):
    name = StringField("Contact's Name", [Required("Please enter the contact's name.")])
    email = StringField("Contact's Email Address", [Required("Please enter the contact's Email address.")])
    submit = SubmitField("Submit")

#############################################
# Raspberry Pi GIF Display forms


class SlideshowDelay(Form):
    delay = StringField("", [Required("Please enter a valid time (in seconds).")])
    submit = SubmitField("Submit")


#############################################
# GIF Party forms


class GifParty(Form):
    delay = StringField("", [Required("Please enter a valid time (in seconds).")])
    submit = SubmitField("Submit")

#############################################
# Reddit Scraper forms


class RedditImageScraper(Form):
    subreddit_choice = StringField('Subreddit Choice', validators=[DataRequired('Please enter a subreddit.')])
    minimum_score = StringField('Minimum Score', validators=[DataRequired('Please enter a minimum score.')])
    results_from = SelectField('Results From', choices=[('1', 'Hot'), ('4', 'Month'), ('3', 'Year'), ('2', 'All')])
    number = SelectField('Number of Submissions to Scrape', choices=[('5', '5'), ('10', '10'), ('20', '20'),
                                                                                 ('50', '50'), ('100', '100')])
    submit = SubmitField('Go!')


#############################################
# CMS Forms
class LoginForm(Form):
    username = StringField('Username', [Required('Enter Your Username')])
    password = PasswordField('Password', [Required('Enter Your Password')])
    submit = SubmitField('Submit')


class DatabaseForm(Form):
    color = StringField('Color', [Required('Please choose a background-color.')])
    title = StringField('Title', [Required('Please enter a title.')])
    icon = StringField('Icon', [Required('Please choose an icon.')])
    subtitle = StringField('Subtitle', [Required('Please enter a subtitle.')])
    content = TextAreaField('Content', [Required('Please type your content.')])
    hidden_date = StringField('Hidden Date Field', [Optional()])
    month = StringField('Month Field', [Optional()])
    year = StringField('Year Field', [Optional()])
    submit = SubmitField('Submit')