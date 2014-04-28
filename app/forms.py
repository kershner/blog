from flask.ext.wtf import Form, TextField, SubmitField, validators


class ContactForm(Form):
    email = TextField("Contact's Email Address", [validators.Required("Please enter the contact's Email address.")])
    po = TextField("Purchase Order or Sales Order", [validators.Required("Please enter the PO or Sales Order Number.")])
    name = TextField("Contact Name", [validators.Required("Please enter the contact's name.")])
    item_number = TextField("Item Number", [validators.Required("Please enter the item's number.")])
    lead_time = TextField("Lead Time", [validators.Required("Please the estimated lead time.")])
    submit = SubmitField("Submit")


class DateCheckerForm(Form):
    form_date = TextField("Form Date", [validators.Required("Enter the form's issue date in the format MM/DD/YY.")])
    submit = SubmitField("Submit")