from app import db


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(64), index=True)
    contact = db.Column(db.String(128), index=True)
    date = db.Column(db.String(64), index=True)
    image_url = db.Column(db.String(128), index=True)

    def __repr__(self):
        return 'Entry %r' % self.institution