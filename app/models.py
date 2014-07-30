from app import db


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(64), index=True)
    contact_name = db.Column(db.String(128), index=True)
    contact_email = db.Column(db.String(128), index=True)
    csr_name = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.String(64), index=True)
    item_numbers = db.Column(db.String(64), index=True)
    notes = db.Column(db.String(128), index=True)

    def __repr__(self):
        return 'Entry %r' % self.institution