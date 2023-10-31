from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Booking
from .forms import EventForm, CommentForm, BookingForm, UpdateForm
from wtforms.validators import ValidationError
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime

evtbp = Blueprint('event', __name__, url_prefix='/events')


def update_status(id):
    events = db.session.scalar(db.select(Event).where(Event.id == id))
    if events.end_date < datetime.now().date():
        print("inactive")
        events.status = "Inactive"
        db.session.commit()

    if events.tickets_avail < 1:
        events.status = "Sold Out"
        db.session.commit()


# Route for displaying all events. Filtered by start_date.
@evtbp.route('/listing')
def listing():
    events = db.session.scalars(
        db.select(Event).order_by(Event.status.asc())).all()
    for event in events:
        update_status(event.id)

    return render_template('events/event_listing.html', events=events)


# Route for displaying events by genre. Filtered by start_date.
@ evtbp.route('/<genre>')
def genres(genre):
    events = db.session.scalars(
        db.select(Event).where(Event.genre == genre).order_by(Event.start_date.asc())).all()
    print(len(events))
    for event in events:
        update_status(event.id)
    return render_template('events/event_listing.html', events=events, genre=genre, genre_sort=True)


# Route for creating events.
@evtbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        event = Event(
            name=form.name.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            location=form.location.data,
            genre=form.genre.data,
            total_tickets=form.total_tickets.data,
            price=form.price.data,
            description=form.description.data,
            image=db_file_path,
            user_id=current_user.id  # Set the user_id here
        )
        event.tickets_avail = event.total_tickets

        db.session.add(event)
        db.session.commit()
        flash('Successfully created new event', 'success')
        return redirect(url_for('event.listing'))
    return render_template('events/event_creation.html', form=form)


# Route for displaying events created by user.
@evtbp.route('/user_events')
@login_required
def user_events():
    events = db.session.scalars(
        db.select(Event).where(Event.user_id == current_user.id)).all()

    for event in events:
        update_status(event.id)

    return render_template('events/events_created.html', events=events)


# # Route for updating events.
@evtbp.route('/update=<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UpdateForm()
    events = db.session.scalar(db.select(Event).where(Event.id == id))
    booked_tickets_num = events.total_tickets - events.tickets_avail
    # print(events.image)
    if request.method == 'GET':
        form.name.data = events.name
        form.start_time.data = events.start_time
        form.end_time.data = events.end_time
        form.start_date.data = events.start_date
        form.end_date.data = events.end_date
        form.location.data = events.location
        form.genre.data = events.genre
        form.total_tickets.data = events.total_tickets
        form.price.data = events.price
        form.description.data = events.description
        # form.cancel.data = events.status
    if form.validate_on_submit():
        events.name = form.name.data
        events.start_time = form.start_time.data
        events.end_time = form.end_time.data
        events.start_date = form.start_date.data
        events.end_date = form.end_date.data
        events.location = form.location.data
        events.genre = form.genre.data
        events.total_tickets = form.total_tickets.data
        events.price = form.price.data
        events.description = form.description.data
        events.tickets_avail = events.total_tickets - booked_tickets_num
        if form.cancel.data == True:
            events.status = "Cancelled"
        else:
            events.status = "Open"
        db.session.commit()
        print("updated")
        flash('Successfully updated event', 'success')
        return redirect(url_for('event.user_events'))
    return render_template('events/event_creation.html', u_form=form, update_event=True)


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
    # update_status(events.id)
    # create the comment form
    form = CommentForm()
    # create the booking form
    b_form = BookingForm()
    return render_template('events/event_details.html', event=events, form=form, b_form=b_form)


# Route for booking event.
@evtbp.route('/<id>/booking', methods=['GET', 'POST'])
@login_required
def booking(id):
    form = BookingForm()
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    # update_status(event.id)
    # Debugging: Print the event and user details
    print("Event User ID:", event.user_id)
    print("Current User ID:", current_user.id)

    if form.validate_on_submit():
        # Debugging: Check if form validation is successful
        print("Form is validated")

        # Ensure the user making the booking is the current user (if not, handle as needed)
        # if event.user_id != current_user.id:
        #     print("You are not authorized to make this booking")
        #     flash('You are not authorized to make this booking.', 'danger')
        #     return redirect(url_for('event.details', id=id))

        # Read the booking details from the form
        booking = Booking(
            num_tickets=form.num_tickets.data,
            total_cost=form.num_tickets.data * event.price,
            event_id=event.id,
            user_id=current_user.id
        )
        event.tickets_avail = event.tickets_avail - booking.num_tickets
        if event.tickets_avail < 0:
            flash('Booking Failed. Your booking exceeds the allocated ticket range.')
            return redirect(url_for('event.details', id=id))
        print(event.tickets_avail)
        db.session.add(booking)
        db.session.commit()

        # Debugging: Check if the booking is created and committed to the database
        print("Booking created and committed")

        flash('Successfully created booking', 'success')

        # Redirect to booking history
        return redirect(url_for('event.booking_history'))

    return render_template('events/booking_history.html', event=event, form=form)


# Route for viewing booking history.
@evtbp.route('/booking_history')
@login_required
def booking_history():
    # Retrieve the user's booking history and related event data
    user_bookings = db.session.query(Booking, Event).\
        join(Event, Booking.event_id == Event.id).\
        filter(Booking.user_id == current_user.id).order_by(
            Booking.date.asc()).all()

    return render_template('events/booking_history.html', user_bookings=user_bookings)


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
        # Always end with redirect when form is valid
        # print('Successfully created new event')
        return redirect(url_for('event.details', id=id))
