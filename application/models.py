from application import app, db, login_manager
from sqlalchemy import Column, Integer, Float, String, DateTime, Date, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from passlib.hash import sha256_crypt
from flask_login import UserMixin

# For storing the User object currently logged in
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# For creating the tables in the database
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Created!')

# For dropping the tables in the database
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database Dropped!')

# For seeding the database
@app.cli.command('db_seed')
def db_seed():
    user1 = User(user_login_id='reception',
                 password=sha256_crypt.hash('reCep!2345'),
                 timestamp=datetime.utcnow())

    db.session.add(user1)
    db.session.commit()

    user2 = User(user_login_id='pharmacy',
                 password=sha256_crypt.hash('p#@rMA6789'),
                 timestamp=datetime.utcnow())

    db.session.add(user2)
    db.session.commit()

    user3 = User(user_login_id='diagnosis',
                 password=sha256_crypt.hash('d!@gn0$!s1'),
                 timestamp=datetime.utcnow())

    db.session.add(user3)
    db.session.commit()

    patient_ = Patient(ws_pat_id=100000001,
                       ws_ssn=123456789,
                       ws_pat_name='Dev Kumar Bose',
                       ws_age=22,
                       ws_doj=datetime.utcnow().date(),
                       ws_rtype='Semi Room',
                       ws_adrs='110, New Town Area',
                       patient_city='Kolkata',
                       patient_state='West Bengal',
                       patient_status='Active')

    patient1 = Patient(ws_ssn='123556789',
                       ws_pat_name='Ambar Chatterjee',
                       ws_age=22,
                       ws_doj=datetime.utcnow().date(),
                       ws_rtype='Semi Room',
                       ws_adrs='108, Chinar Park',
                       patient_city='Kolkata',
                       patient_state='West Bengal',
                       patient_status='Active')

    patient2 = Patient(ws_ssn='768556789',
                       ws_pat_name='Supriyo Jana',
                       ws_age=24,
                       ws_doj=datetime.utcnow().date(),
                       ws_rtype='Semi Room',
                       ws_adrs='69, Pabitra Road',
                       patient_city='Kolkata',
                       patient_state='West Bengal',
                       patient_status='Active')

    patient3 = Patient(ws_ssn='394860212',
                       ws_pat_name='John Doe',
                       ws_age=28,
                       ws_doj=datetime.utcnow().date(),
                       ws_rtype='Single Room',
                       ws_adrs='99, Brooklyn Drive',
                       patient_city='New York',
                       patient_state='New York State',
                       patient_status='Active')

    db.session.add(patient_)
    db.session.add(patient1)
    db.session.add(patient2)
    db.session.add(patient3)
    db.session.commit()

    medicine1 = Medicine(ws_med_name='Honitus',
                         ws_qty_avbl=1200,
                         ws_med_rate=210)

    medicine2 = Medicine(ws_med_name='Pudin Hara',
                         ws_qty_avbl=1420,
                         ws_med_rate=60)

    medicine3 = Medicine(ws_med_name='Burnol',
                         ws_qty_avbl=580,
                         ws_med_rate=70)

    medicine4 = Medicine(ws_med_name='Calpol',
                         ws_qty_avbl=2000,
                         ws_med_rate=20)

    db.session.add(medicine1)
    db.session.add(medicine2)
    db.session.add(medicine3)
    db.session.add(medicine4)
    db.session.commit()

    diagnostic1 = Diagnostic(ws_diagn='X-Ray',
                             ws_test_charge=150)

    diagnostic2 = Diagnostic(ws_diagn='CT Scan',
                             ws_test_charge=700)

    diagnostic3 = Diagnostic(ws_diagn='USG',
                             ws_test_charge=910)

    diagnostic4 = Diagnostic(ws_diagn='Blood Test',
                             ws_test_charge=80)

    db.session.add(diagnostic1)
    db.session.add(diagnostic2)
    db.session.add(diagnostic3)
    db.session.add(diagnostic4)
    db.session.commit()

    med_issue1 = MedsIssue(qty_issued=10, issueMed=medicine3, patient=patient1)
    db.session.add(med_issue1)
    db.session.commit()

    med_issue2 = MedsIssue(qty_issued=1, issueMed=medicine4, patient=patient1)
    db.session.add(med_issue2)
    db.session.commit()

    med_issue3 = MedsIssue(qty_issued=6, issueMed=medicine1, patient=patient2)
    db.session.add(med_issue3)
    db.session.commit()

    diag_issue1 = DiagsIssue(issueDiag=diagnostic1, patient=patient1)
    db.session.add(diag_issue1)
    db.session.commit()

    diag_issue2 = DiagsIssue(issueDiag=diagnostic3, patient=patient3)
    db.session.add(diag_issue2)
    db.session.commit()

    diag_issue3 = DiagsIssue(issueDiag=diagnostic1, patient=patient1)
    db.session.add(diag_issue3)
    db.session.commit()

    print('Database Seeded!')


# Database Models

class MedsIssue(db.Model):
    __tablename__ = 'medsissue'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ws_pat_id = Column(Integer, db.ForeignKey('patient.ws_pat_id'))
    ws_med_id = Column(Integer, db.ForeignKey('medicine.ws_med_id'))
    qty_issued = Column(Integer)


class DiagsIssue(db.Model):
    __tablename__ = 'diagsissue'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ws_pat_id = Column(Integer, db.ForeignKey('patient.ws_pat_id'))
    ws_test_id = Column(Integer, db.ForeignKey('diagnostic.ws_test_id'))


class User(db.Model, UserMixin):
    __tablename__ = 'userstore'
    id = Column(Integer, primary_key=True)
    user_login_id = Column(String, unique=True)
    password = Column(String)
    timestamp = Column(DateTime)


class State(db.Model):
    stateid = db.Column(db.String(2), primary_key=True)
    statename = db.Column(db.String(50))


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stateid = db.Column(db.String(2))
    cityname = db.Column(db.String(50))


class Patient(db.Model):
    __tablename__ = 'patient'
    ws_pat_id = Column(Integer, primary_key=True)
    ws_ssn = Column(Integer, unique=True)
    ws_pat_name = Column(String)
    ws_age = Column(Integer)
    ws_doj = Column(Date)
    ws_rtype = Column(String)
    ws_adrs = Column(String)
    patient_city = Column(String)
    patient_state = Column(String)
    patient_status = Column(String)

    medicines = db.relationship(
      "MedsIssue",
      backref="patient",
      cascade="all, save-update, merge, delete, delete-orphan"
      )

    diagnostics = db.relationship(
      "DiagsIssue",
      backref="patient",
      cascade="all, save-update, merge, delete, delete-orphan"
      )


class Medicine(db.Model):
    __tablename__ = 'medicine'
    ws_med_id = Column(Integer, primary_key=True)
    ws_med_name = Column(String, unique=True)
    ws_qty_avbl = Column(Integer)
    ws_med_rate = Column(Float)
    medicine_issued = db.relationship(
      "MedsIssue",
      backref="issueMed",
      cascade="all, save-update, merge, delete, delete-orphan"
      )


class Diagnostic(db.Model):
    __tablename__ = 'diagnostic'
    ws_test_id = Column(Integer, primary_key=True)
    ws_diagn = Column(String, unique=True)
    ws_test_charge = Column(Integer)
    diagnostic_issued = db.relationship(
      "DiagsIssue",
      backref="issueDiag",
      cascade="all, save-update, merge, delete, delete-orphan"
      )
