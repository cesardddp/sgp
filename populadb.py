import csv
with open('sgp_real.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))

from models import Projeto
def db_load_example_data(app, db):
    admin = Projeto('admin', 'test')
    guest = Projeto('guest', 'test')
    with app.app_context():
        db.session.add(admin)
        db.session.add(guest)
        db.commit()