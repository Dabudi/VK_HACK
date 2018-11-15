from app import db

class User(db.Model):
    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    vk_id = db.Column(db.Integer)
    target = db.Column(db.PickleType)
    Role = db.Column(db.String(50))

class Event(db.Model):
    __tablename__ = 'events_event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(240))
    data = db.Column(db.String(50))
    photo = db.Column(db.String(100))
    link = db.Column(db.String(100))
    vector = db.Column(db.PickleType)
    resident_id = db.Column(db.Integer)

class UserEvnet(db.Model):
    __tablename__ = 'users_events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'), nullable=False)
    events_id = db.Column(db.PickleType)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(250))
