from flask.ext.wtf import Form, TextField, SubmitField, validators


class BackorderForm(Form):
    email = TextField("Contact's Email Address", [validators.Required("Please enter the contact's Email address.")])
    po = TextField("Purchase Order or Sales Order", [validators.Required("Please enter the PO or Sales Order Number.")])
    name = TextField("Contact Name", [validators.Required("Please enter the contact's name.")])
    item_number = TextField("Item Number", [validators.Required("Please enter the item's number.")])
    lead_time = TextField("Lead Time", [validators.Required("Please the estimated lead time.")])
    submit = SubmitField("Submit")


class DateCheckerForm(Form):
    form_date = TextField("Form Date", [validators.Required("Enter the form's issue date in the format MM/DD/YY.")])
    submit = SubmitField("Submit")


class ApplicationForm(Form):
    name = TextField("Contact Name", [validators.Required("Please enter the contact's name.")])
    email = TextField("Contact's Email Address", [validators.Required("Please enter the contact's Email address.")])
    submit = SubmitField("Submit")


class NewAccountForm(Form):
    name = TextField("Contact Name", [validators.Required("Please enter the contact's name.")])
    acct = TextField("Customer Account Number", [validators.Required("Please enter the customer's account number.")])
    email = TextField("Contact's Email Address", [validators.Required("Please enter the contact's Email address.")])
    submit = SubmitField("Submit")


class DeaForm(Form):
    name = TextField("Contact Name", [validators.Required("Please enter the contact's name.")])
    email = TextField("Contact's Email Address", [validators.Required("Please enter the contact's Email address.")])
    dea_items = TextField("Regulated Items", [validators.Required("Please enter the regulated item(s).")])
    submit = SubmitField("Submit")


class ShadyForm(Form):
    email = TextField("Contact's Email Address", [validators.Required("Please enter the contact's Email address.")])
    order_no = TextField("Sales Order Number", [validators.Required("Please enter the sales order number.")])
    submit = SubmitField("Submit")


class DiscrepancyForm(Form):
    name = TextField("Contact Name", [validators.Required("Please enter the contact's name.")])
    email = TextField("Contact's Email Address", [validators.Required("Please enter the contact's Email address.")])
    po = TextField("Purchase Order or Sales Order", [validators.Required("Please enter the PO or Sales Order Number.")])
    item_number = TextField("Item Number", [validators.Required("Please enter the item's number.")])
    given_price = TextField("Customer's Given Price", [validators.Required("Please enter the price given by the customer.")])
    actual_price = TextField("Actual Price", [validators.Required("Please enter the item's actual price.")])
    submit = SubmitField("Submit")


class StillNeed(Form):
    name = TextField("Contact's Name", [validators.Required("Please enter the contact's name.")])
    email = TextField("Contact's Email Address", [validators.Required("Please enter the contact's Email address.")])
    item_number = TextField("Item Number", [validators.Required("Please enter the item's number.")])
    order_no = TextField("Sales Order Number", [validators.Required("Please enter the sales order number.")])
    submit = SubmitField("Submit")


class LicenseNeeded(Form):
    name = TextField("Contact's Name", [validators.Required("Please enter the contact's name.")])
    email = TextField("Contact's Email Address", [validators.Required("Please enter the contact's Email address.")])
    order_no = TextField("Sales Order Number", [validators.Required("Please enter the sales order number.")])
    submit = SubmitField("Submit")