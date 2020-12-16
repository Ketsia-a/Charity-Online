from . import db
from flask_login import UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ngo class
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255),unique = True,nullable = False)
    email  = db.Column(db.String(255),unique = True,nullable = False)
    secure_password = db.Column(db.String(255),nullable = False)


    event = db.relationship('Event', backref='user', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.secure_password,password)


    def __repr__(self):
        return f'User {self.username}'

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255),nullable = False)
    event_pic_path = db.Column(db.String())
    description = db.Column(db.Text(), nullable = False)
    category = db.Column(db.String(255), index = True,nullable = False)
    value = db.Column(db.Integer, nullable = False) 
    time = db.Column(db.DateTime, default = datetime.utcnow)


    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    donor = db.relationship('Donor',backref='event',lazy='dynamic')
   
    @classmethod
    def clear_event(cls):
        Bloc.event.clear()
    
    @classmethod
    def get_events(cls):
        event = Event.query.filter_by(id = id).all()
        return event

    def delete(self, id):
        donors = Donor.query.filter_by(id = id).all()
        for donor in donors:
            db.session.delete(donor)
            db.session.commit()
        db.session.delete(self)
        db.session.commit()    
    
    def __repr__(self):
        return f'Event {self.name}'

        

class Donor(db.Model):
    __tablename__ = 'donors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),unique = True,nullable = False)
    email  = db.Column(db.String(255),unique = True,nullable = False)
    amount = db.Column(db.Integer, nullable = False)

    event_id = db.Column(db.Integer,db.ForeignKey('events.id'))


    @classmethod
    def clear_comment(self):
        Donor.donors.clear()

    @classmethod
    def get_donors(cls, id):
        donors = Donor.query.filter_by(event_id = id).all()
        return donors   

     
    def __repr__(self):
        return f'Donor {self.name}'