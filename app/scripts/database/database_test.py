from app import db, models
from datetime import datetime

now = datetime.utcnow()
date_nice = now.strftime('%m/%d/%Y')


entry1 = models.Entry(institution="Texas Labs",
                      contact_name='Tyler',
                      contact_email='tyler@tyler.biz',
                      timestamp=date_nice,
                      csr_name='Tyler')

entry2 = models.Entry(institution="Tammany Tickler",
                      contact_name='Shareeza',
                      contact_email='shar@tyler.biz',
                      timestamp=date_nice,
                      csr_name='Miranda')

entry3 = models.Entry(institution="Caltech",
                      contact_name='Bacon',
                      contact_email='bacon@tyler.biz',
                      timestamp=date_nice,
                      csr_name='Tyler')

db.session.add(entry1)
db.session.add(entry2)
db.session.add(entry3)

db.session.commit()