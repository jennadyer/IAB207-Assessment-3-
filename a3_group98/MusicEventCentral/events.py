from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Booking
from .forms import EventForm, CommentForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

evtbp = Blueprint('event', __name__, url_prefix='/events')


# Route for displaying all events. Filtered by start_date.
@evtbp.route('/listing')
def listing():
    events = db.session.scalars(
        db.select(Event).order_by(Event.start_date.asc())).all()
    return render_template('events/event_listing.html', events=events)


# Route for displaying events by genre. Filtered by start_date.
@ evtbp.route('/<genre>')
def genres(genre):
    events = db.session.scalars(
        db.select(Event).where(Event.genre == genre).order_by(Event.start_date.asc())).all()
    print(len(events))
    return render_template('events/event_listing.html', events=events)


# Route for creating events.
@ evtbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        # call the function that checks and returns image
        db_file_path = check_upload_file(form)
        event = Event(name=form.name.data, start_time=form.start_time.data, end_time=form.end_time.data,
                      start_date=form.start_date.data, end_date=form.end_date.data, location=form.location.data, genre=form.genre.data,
                      total_tickets=form.total_tickets.data, price=form.price.data, description=form.description.data,
                      image=db_file_path)
        # add the object to the db session
        db.session.add(event)
        # commit to the database
        db.session.commit()
        flash('Successfully created new event', 'success')
        # Always end with redirect when form is valid
        # print('Successfully created new event')
        return redirect(url_for('event.create'))
    return render_template('events/event_creation.html', form=form)


def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    filename = fp.filename
    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(
        BASE_PATH, 'static/img', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/img/' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path


# Route for displaying details of selected event.
@ evtbp.route('/details=<id>')
def details(id):
    events = db.session.scalar(db.select(Event).where(Event.id == id))
    # create the comment form
    form = CommentForm()
    # create the booking form
    b_form = BookingForm()
    return render_template('events/event_details.html', event=events, form=form, b_form=b_form)


# Route for booking.
@ evtbp.route('/<id>/booking', methods=['GET', 'POST'])
@login_required
def booking(id):
    form = BookingForm()
    # get the event object associated to the event and the comment
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if form.validate_on_submit():
        # read the booking details from the form
        booking = Booking(num_tickets=form.num_tickets.data, total_cost=form.num_tickets.data * event.price,
                          event_id=event.id, user_id=current_user.id)
        # add the object to the db session
        db.session.add(booking)
        db.session.commit()

        flash('Successfully created booking', 'success')
        # Always end with redirect when form is valid
        # print('Successfully created new event')
        return redirect(url_for('event.details', id=id, show_modal=True))


# Route for comments.
@ evtbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    # get the event object associated to the event and the comment
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if form.validate_on_submit():
        # read the comment from the form
        comment = Comment(text=form.text.data,
                          event_id=event.id, user_id=current_user.id)
        # add the object to the db session
        db.session.add(comment)
        db.session.commit()
        flash('Successfully created comment', 'success')
        # Always end with redirect when form is valid
        # print('Successfully created new event')
        return redirect(url_for('event.details', id=id))
