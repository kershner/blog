from app import db


# Model for blog posts
class Post(db.Model):
    __bind_key__ = 'db1'

    id = db.Column(db.Integer, primary_key=True)
    css_class = db.Column(db.String(64), index=True)
    title = db.Column(db.String(128), index=True)
    subtitle = db.Column(db.String(128), index=True)
    icon = db.Column(db.String(128), index=True)
    content = db.Column(db.String(), index=True)
    date = db.Column(db.String(64), index=True)
    month = db.Column(db.String(64), index=True)
    year = db.Column(db.String(32), index=True)

    def __repr__(self):
        return '%d' % self.id


# Model for CSTools Forms DB
class Entry(db.Model):
    __bind_key__ = 'db2'

    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(64), index=True)
    contact_name = db.Column(db.String(128), index=True)
    contact_email = db.Column(db.String(128), index=True)
    csr_name = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.String(64), index=True)
    item_numbers = db.Column(db.String(64), index=True)
    notes = db.Column(db.String(128), index=True)
    color = db.Column(db.String(64), index=True)

    def __repr__(self):
        return 'Entry %r' % self.institution