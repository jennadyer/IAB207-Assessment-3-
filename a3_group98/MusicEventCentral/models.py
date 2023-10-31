from . import db
from datetime import datetime
from flask_login import UserMixin


# --- Events Table ---
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    location = db.Column(db.String(200))
    total_tickets = db.Column(db.Integer)
    tickets_avail = db.Column(db.Integer)
    status = db.Column(db.String(80), default="Open")
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    price = db.Column(db.Numeric(precision=10, scale=2))
    genre = db.Column(db.String(80))

    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # ... Create the Comments db.relationship
    # relation to call event.comments and comment.event
    comments = db.relationship('Comment', backref='events')

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"


# --- Booking Table ---
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now())
    num_tickets = db.Column(db.Integer)
    total_cost = db.Column(db.Float)

    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"


# --- User Table ---
class User(db.Model, UserMixin):
    __tablename__ = 'users'  # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    phoneid = db.Column(db.String(40), index=True, nullable=False)
    # password is never stored in the DB, an encrypted password is stored
    # the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"


# --- Comments Table ---
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # string print method
    def __repr__(self):
        return f"Comment: {self.text}"
