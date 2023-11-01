from flask import Blueprint, render_template, request, redirect, url_for, abort
from .models import Event
from . import db
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    for event in events:
        update_status(event.id)
    return render_template('index.html', events=events)

def update_status(id):
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    
    if event is None:
        # Handle the case where the event with the given ID is not found.
        return

    if event.end_date < datetime.now().date():
        print("inactive")
        event.status = "Inactive"
        db.session.commit()

    if event.tickets_avail is not None and event.tickets_avail < 1:
        event.status = "Sold Out"
        db.session.commit()


# Custom 404 (Not Found) error handler
@bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

# Custom exception handler for a specific exception
class CustomException(Exception):
    pass

@bp.errorhandler(CustomException)
def custom_exception_handler(error):
    return render_template('errors/custom_error.html'), 500

# Search route with error handling
@bp.route('/search')
def search():
    if 'search' in request.args and request.args['search']:
        query = "%" + request.args['search'] + "%"
        events = db.session.scalars(
            db.select(Event).where(
                (Event.name.like(query)) |
                (Event.genre.like(query)) |
                (Event.start_date.like(query))
            )
        )
        return render_template('events/event_listing.html', events=events)
    else:
        # Raise a 404 error when the search query is empty
        abort(404)
