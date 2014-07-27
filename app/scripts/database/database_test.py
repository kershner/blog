from app import db, models
from datetime import datetime

entry1 = models.Entry(institution="Texas Labs",
                      contact_name='Tyler',
                      contact_email='tyler@tyler.biz',
                      timestamp=datetime.utcnow(),
                      image_url='http://bizzness.dobis')

entry2 = models.Entry(institution="Tammany Tickler",
                      contact_name='Shareeza',
                      contact_email='shar@tyler.biz',
                      timestamp=datetime.utcnow(),
                      image_url='http://timmy.dobis')

entry3 = models.Entry(institution="Caltech",
                      contact_name='Bacon',
                      contact_email='bacon@tyler.biz',
                      timestamp=datetime.utcnow(),
                      image_url='http://steph.dobis')

# db.session.add(entry1)
# db.session.add(entry2)
# db.session.add(entry3)
#
# db.session.commit()

entries = models.Entry.query.all()

print entries[0].id